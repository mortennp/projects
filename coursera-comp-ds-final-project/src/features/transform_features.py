import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler #, SimpleImputer


def create_mapper(categorical_features, numeric_features, n_jobs=-1):
    from sklearn.compose import ColumnTransformer

    return ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(dtype=np.int32, sparse=False, handle_unknown='error'), categorical_features)
        ],
        remainder='passthrough',
        n_jobs=n_jobs
    )


def create_mapper_sklearn_pandas_contrib(categorical_features, numeric_features):
    from sklearn_pandas import DataFrameMapper, gen_features

    categorial_maps = gen_features(
        columns=[[feature] for feature in categorical_features],
        classes=[{'class': OneHotEncoder, 'dtype': np.float32, 'sparse':False, 'handle_unknown':'ignore'}])
    numeric_maps = gen_features(
        columns=[[feature] for feature in numeric_features],
        classes=[StandardScaler])
    return DataFrameMapper(categorial_maps + numeric_maps, default=None)