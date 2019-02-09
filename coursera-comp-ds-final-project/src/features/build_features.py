import gc
import numpy as np
import pandas as pd
from src.features.common import *

def rollup_and_clip_sales(sales):    
    rolled_up = sales.groupby(COLUMNS.KEYS_AND_TIME).agg(
        {'item_cnt_day':{'item_cnt_month':'sum'}}).reset_index().sort_values(COLUMNS.KEYS_AND_TIME) #, 'num_sales_month':'count'
    rolled_up.columns = [col[0] if col[-1]=='' else col[-1] for col in rolled_up.columns.values]
    rolled_up.item_cnt_month = rolled_up.item_cnt_month.clip(0,20)
    return downcast_dtypes(rolled_up)


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