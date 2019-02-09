import pandas as pd
from src.features.common import downcast_dtypes

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


def enrich(sales, shops, items, categories):
    return downcast_dtypes(
        sales.merge(
            shops, on=['shop_id'], how='left').merge(
            items, on=['item_id'], how='left').merge(
            categories, on=['item_category_id'], how='left'))
