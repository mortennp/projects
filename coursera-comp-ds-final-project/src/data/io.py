import os
import pandas as pd
import numpy as np
import h5py

_DATASET_KEY = 'dataset_1'

def read_raw(folder):
    sales = pd.read_csv(os.path.join(folder, 'sales_train.csv.gz'))
    test = pd.read_csv(os.path.join(folder, 'test.csv.gz'))
    items = pd.read_csv(os.path.join(folder, 'items.csv'))
    categories = pd.read_csv(os.path.join(folder, 'item_categories.csv'))
    shops = pd.read_csv(os.path.join(folder, 'shops.csv'))    
    return sales, test, items, categories, shops

def save_data(folder, filename, data):
    print('Saving ' + filename)
    path = os.path.join(folder, filename)
    if isinstance(data, pd.DataFrame):
        path += '.parquet'
        data.to_parquet(path, engine='pyarrow')
    elif isinstance(data, np.ndarray):
        path += '.h5'
        with h5py.File(path, 'w') as f:
            f.create_dataset(_DATASET_KEY, data=data)
    else:
        raise('Not supported')
    print('Saved ' + path)

    
def load_data(folder, filename, hint):
    print('Loading ' + filename)
    path = os.path.join(folder, filename) 
    if isinstance(hint, pd.DataFrame):
        path += '.parquet'
        data = pd.read_parquet(path, engine='pyarrow')
    elif isinstance(hint, np.ndarray):
        path += '.h5'
        with h5py.File(path,'r') as f:
            data = f[_DATASET_KEY][:]
    else:
        raise('Not supported')
    print('Loaded ' + path)
        
    return data