import os
import pandas as pd
import h5py

_DATASET_KEY = 'dataset_1'

def save_data(folder, filename, data):
    path = str(os.path.join(folder, filename) + '.h5')
    print('Saving ' + path)
    if isinstance(data, pd.DataFrame):
        data.to_hdf(path, _DATASET_KEY, mode='w')
    elif isinstance(data, np.ndarray):
        with h5py.File(path, 'w') as f:
            f.create_dataset(_DATASET_KEY, data=data)
    else:
        raise('Not supported')
    
def load_data(folder, filename, hint):
    path = str(os.path.join(folder, filename) + '.h5')
    print('Loading ' + path)
    if isinstance(hint, pd.DataFrame):
        data = pd.read_hdf(path, _DATASET_KEY)
    elif isinstance(hint, np.ndarray):
        with h5py.File(path,'r') as f:
            data = f[_DATASET_KEY][:]
    else:
        raise('Not supported')
        
    return data