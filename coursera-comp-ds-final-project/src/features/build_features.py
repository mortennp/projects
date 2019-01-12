import pandas as pd
from src.features import COLUMNS

def rollup_sales(sales):    
    rolled_up = sales.groupby(COLUMNS.KEYS_AND_TIME).aggregate({'item_cnt_day': 'sum'}).reset_index().sort_values(COLUMNS.KEYS_AND_TIME)
    rolled_up = rolled_up.rename(columns={'item_cnt_day' : 'item_cnt_month'})
    return rolled_up

def enrich_sales(sales, shops, items, categories):
    return sales.merge(
        shops, on=['shop_id'], how='left').merge(
        items, on=['item_id'], how='left').merge(
        categories, on=['item_category_id'], how='left')

def add_super_category(categories):
    super_categories = pd.DataFrame(
        list(enumerate(sorted(list(set(categories.item_category_name.apply(lambda s: s.split(' ')[0])))))),
        columns=['super_category_id', 'super_category_name'])
    return categories.assign(super_category_name = lambda c: c.item_category_name.apply(lambda s: s.split(' ')[0])).merge(super_categories, on=['super_category_name'], how='left')

def add_super_shop(shops):
    super_shops = pd.DataFrame(
        list(enumerate(sorted(list(set(shops.shop_name.apply(lambda s: s.split(' ')[0])))))),
        columns=['super_shop_id', 'super_shop_name'])
    return shops.assign(super_shop_name = lambda c: c.shop_name.apply(lambda s: s.split(' ')[0])).merge(super_shops, on=['super_shop_name'], how='left')