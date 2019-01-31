import gc
import numpy as np
import pandas as pd

from src.features import COLUMNS

def add_super_category(categories):
    super_categories = pd.DataFrame(
        list(enumerate(sorted(list(set(categories.item_category_name.apply(lambda s: s.split(' ')[0])))))),
        columns=['super_category_id', 'super_category_name'])
    return downcast_dtypes(
        categories.assign(super_category_name = lambda c: c.item_category_name.apply(lambda s: s.split(' ')[0]))\
        .merge(super_categories, on=['super_category_name'], how='left'))        


def add_super_shop(shops):
    super_shops = pd.DataFrame(
        list(enumerate(sorted(list(set(shops.shop_name.apply(lambda s: s.split(' ')[0])))))),
        columns=['super_shop_id', 'super_shop_name'])
    return downcast_dtypes(
        shops.assign(super_shop_name = lambda c: c.shop_name.apply(lambda s: s.split(' ')[0])).\
        merge(super_shops, on=['super_shop_name'], how='left'))


def rollup_and_clip_sales(sales):    
    rolled_up = sales.groupby(COLUMNS.KEYS_AND_TIME).agg(
        {'item_cnt_day':{'item_cnt_month':'sum'}}).reset_index().sort_values(COLUMNS.KEYS_AND_TIME) #, 'num_sales_month':'count'
    rolled_up.columns = [col[0] if col[-1]=='' else col[-1] for col in rolled_up.columns.values]
    rolled_up.item_cnt_month = rolled_up.item_cnt_month.clip(0,20)
    return downcast_dtypes(rolled_up)


def enrich(sales, shops, items, categories):
    return downcast_dtypes(
        sales.merge(
            shops, on=['shop_id'], how='left').merge(
            items, on=['item_id'], how='left').merge(
            categories, on=['item_category_id'], how='left'))


def downcast_dtypes(df):
    '''
        Changes column types in the dataframe: 
                
                `float64` type to `float32`
                `int64`   type to `int32`
    '''
    
    # Select columns to downcast
    float_cols = [c for c in df if df[c].dtype == "float64"]
    int_cols =   [c for c in df if df[c].dtype == "int64"]
    
    # Downcast
    df[float_cols] = df[float_cols].astype(np.float32)
    df[int_cols]   = df[int_cols].astype(np.int32)
    
    return df


def create_grid(sales, index_cols, progress_iter): 
    from itertools import product

    # For every month we create a grid from all shops/items combinations from that month
    grid = [] 
    for block_num in progress_iter(sales['date_block_num'].unique()):
        cur_shops = sales.loc[sales['date_block_num'] == block_num, 'shop_id'].unique()
        cur_items = sales.loc[sales['date_block_num'] == block_num, 'item_id'].unique()
        grid.append(np.array(list(product(*[[block_num], cur_shops, cur_items])),dtype='int32'))

    # Turn the grid into a dataframe
    grid = pd.DataFrame(np.vstack(grid), columns=index_cols, dtype=np.int32)

    # Join it to the grid    
    sales_grid = pd.merge(grid, sales, how='left', on=index_cols).fillna(0)

    del grid
    gc.collect()
    return sales_grid

def mean_encode_target_by_month_and_features(enriched, feature_names):
    from scipy.stats import iqr
    
    # 'feature_name'/month aggregates
    gb_keys = list(feature_names) + ['date_block_num']
    mean_encoded_name = '_'.join(gb_keys[:-1])
    gb = enriched.groupby(gb_keys, as_index=False).agg({
        'target':{'mean_target_{}'.format(mean_encoded_name):'mean',
        'median_target_{}'.format(mean_encoded_name):'median',
        'iqr_target_{}'.format(mean_encoded_name):iqr,
        'num_target_{}'.format(mean_encoded_name):'count'}})
    gb.columns = [col[0] if col[-1]=='' else col[-1] for col in gb.columns.values]
    enriched = pd.merge(enriched, gb, how='left', on=gb_keys).fillna(0)

    del gb 
    gc.collect();
    return enriched


def mean_encode(enriched):
     # Feature/month aggregates
    enriched = mean_encode_target_by_month_and_features(enriched, ['shop_id', 'item_category_id'])
    #enriched = mean_encode_target_by_month_and_features(enriched, 'shop_id')
    #enriched = mean_encode_target_by_month_and_features(enriched, 'super_shop_id')
    #enriched = mean_encode_target_by_month_and_features(enriched, 'item_id')
    #enriched = mean_encode_target_by_month_and_features(enriched, 'item_category_id')
    #enriched = mean_encode_target_by_month_and_features(enriched, 'super_category_id')

    # Downcast dtypes from 64 to 32 bit to save memory
    return downcast_dtypes(enriched)
    

def create_lags(all_data, index_cols, shift_range, progress_iter):
   
    lagged_data = all_data.copy()
    
    # List of columns that we will use to create lags
    cols_to_rename = list(lagged_data.columns.difference(index_cols))    

    for month_shift in progress_iter(shift_range):
        train_shift = lagged_data[index_cols + cols_to_rename].copy()

        train_shift['date_block_num'] = train_shift['date_block_num'] + month_shift

        foo = lambda x: '{}_lag_{}'.format(x, month_shift) if x in cols_to_rename else x
        train_shift = train_shift.rename(columns=foo)

        lagged_data = pd.merge(lagged_data, train_shift, on=index_cols, how='left').fillna(0)

    # List of all lagged features
    fit_cols = [col for col in lagged_data.columns if col[-1] in [str(item) for item in shift_range]]  
    # We will drop these at fitting stage
    to_drop_cols = list(set(list(lagged_data.columns)) - (set(fit_cols)|set(index_cols))) + ['date_block_num'] 
    
    lagged_data = downcast_dtypes(lagged_data)
    del train_shift
    gc.collect();
    
    return lagged_data, to_drop_cols    


def create_mapper(categorical_features, numeric_features):
    from sklearn.preprocessing import OneHotEncoder, StandardScaler #, SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    return ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(dtype=np.int32, sparse=False, handle_unknown='error'), categorical_features)
        ],
        remainder='passthrough',
        n_jobs=-1
    )


def create_mapper_sklearn_pandas_contrib(categorical_features, numeric_features):
    from sklearn.preprocessing import OneHotEncoder, StandardScaler #, SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn_pandas import DataFrameMapper, gen_features

    categorial_maps = gen_features(
        columns=[[feature] for feature in categorical_features],
        classes=[{'class': OneHotEncoder, 'dtype': np.float32, 'sparse':False, 'handle_unknown':'ignore'}])
    numeric_maps = gen_features(
        columns=[[feature] for feature in numeric_features],
        classes=[StandardScaler])
    return DataFrameMapper(categorial_maps + numeric_maps, default=None)