import os
from joblib import dump, load
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import load_model as keras_load_model

def save_model(folder, filename, model):
    path = str(os.path.join(folder, filename) + '.jlib')
    print('Saving ' + path)    
    if isinstance(model, KerasRegressor):
        model.model.save(path)
    else:
        dump(model, path)        
        
def load_model(folder, filename, hint):
    path = str(os.path.join(folder, filename) + '.jlib')
    print('Loading ' + path)
    if isinstance(hint, KerasRegressor):
        model = keras_load_model(path)
    else:
        model = load(path)
        
    return model     