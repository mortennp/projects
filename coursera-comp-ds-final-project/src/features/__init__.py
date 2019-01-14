class COLUMNS :
    KEYS = ['shop_id','item_id']
    KEYS_AND_TIME = ['date_block_num'] + KEYS
    DERIVED_KEYS = ['super_shop_id', 'item_category_id', 'super_category_id']    