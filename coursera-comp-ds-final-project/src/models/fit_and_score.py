import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def score(model_name, ground_truths, predictions):
    print(model_name)
    print('RMSE is %f' % np.sqrt(mean_squared_error(ground_truths, predictions)))
    print('R-squared is %f' % r2_score(ground_truths, predictions))    