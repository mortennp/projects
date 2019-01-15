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
    rolled_up = sales.groupby(COLUMNS.KEYS_AND_TIME).aggregate({'item_cnt_day': 'sum'}).reset_index().sort_values(COLUMNS.KEYS_AND_TIME)
    rolled_up = rolled_up.rename(columns={'item_cnt_day' : 'item_cnt_month'})
    rolled_up.item_cnt_month.clip(0,20, inplace=True)
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


def create_grid(sales, shops, items, categories, index_cols, progress_iter): 
    from itertools import product

    # For every month we create a grid from all shops/items combinations from that month
    grid = [] 
    for block_num in progress_iter(sales['date_block_num'].unique()):
        cur_shops = sales.loc[sales['date_block_num'] == block_num, 'shop_id'].unique()
        cur_items = sales.loc[sales['date_block_num'] == block_num, 'item_id'].unique()
        grid.append(np.array(list(product(*[[block_num], cur_shops, cur_items])),dtype='int32'))

    # Turn the grid into a dataframe
    grid = pd.DataFrame(np.vstack(grid), columns = index_cols,dtype=np.int32)

    # Join it to the grid    
    all_data = pd.merge(grid, sales, how='left', on=index_cols).fillna(0)

    # Enrich    
    all_data = enrich(
        all_data, 
        add_super_shop(shops),
        items,
        add_super_category(categories)).drop(columns=['shop_name', 'super_shop_name', 'item_name', 'item_category_name', 'super_category_name'])

    # Shop-month aggregates
    gb = all_data.groupby(['shop_id', 'date_block_num'],as_index=False).agg({'target':{'target_shop':'sum'}})
    gb.columns = [col[0] if col[-1]=='' else col[-1] for col in gb.columns.values]
    all_data = pd.merge(all_data, gb, how='left', on=['shop_id', 'date_block_num']).fillna(0)

    # Super-shop-month aggregates
    gb = all_data.groupby(['super_shop_id', 'date_block_num'],as_index=False).agg({'target':{'target_super_shop':'sum'}})
    gb.columns = [col[0] if col[-1]=='' else col[-1] for col in gb.columns.values]
    all_data = pd.merge(all_data, gb, how='left', on=['super_shop_id', 'date_block_num']).fillna(0)

    # Item-month aggregates
    gb = all_data.groupby(['item_id', 'date_block_num'],as_index=False).agg({'target':{'target_item':'sum'}})
    gb.columns = [col[0] if col[-1] == '' else col[-1] for col in gb.columns.values]
    all_data = pd.merge(all_data, gb, how='left', on=['item_id', 'date_block_num']).fillna(0)

    # Category-month aggregates
    gb = all_data.groupby(['item_category_id', 'date_block_num'],as_index=False).agg({'target':{'target_category':'sum'}})
    gb.columns = [col[0] if col[-1] == '' else col[-1] for col in gb.columns.values]
    all_data = pd.merge(all_data, gb, how='left', on=['item_category_id', 'date_block_num']).fillna(0)

    # Super-category-month aggregates
    gb = all_data.groupby(['super_category_id', 'date_block_num'],as_index=False).agg({'target':{'target_super_category':'sum'}})
    gb.columns = [col[0] if col[-1] == '' else col[-1] for col in gb.columns.values]
    all_data = pd.merge(all_data, gb, how='left', on=['super_category_id', 'date_block_num']).fillna(0)    

    # Downcast dtypes from 64 to 32 bit to save memory
    all_data = downcast_dtypes(all_data)
    del grid, gb 
    gc.collect();
    
    return all_data


def create_lags(all_data, index_cols, progress_iter, shift_range = [1, 2, 3, 4, 5, 12]):
   
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
    from sklearn_pandas import DataFrameMapper, gen_features

    categorial_maps = gen_features(
        columns=[[feature] for feature in categorical_features],
        classes=[{'class': OneHotEncoder, 'dtype': np.int32, 'sparse':False, 'handle_unknown':'ignore'}])
    numeric_maps = gen_features(
        columns=[[feature] for feature in numeric_features],
        classes=[StandardScaler])
    return DataFrameMapper(categorial_maps + numeric_maps, default=None)
