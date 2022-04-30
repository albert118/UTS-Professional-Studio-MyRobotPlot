import logging

import numpy as np
import pandas as pd
from pandas import DataFrame

from .deserializer import Deserializer
from .string_cleaner import deep_clean

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)

def drop_empty_list_rows(self, column: str): return self[self[column].astype(bool)]

DataFrame.drop_empty_list_rows = drop_empty_list_rows


class Transformer:
    def __init__(self, df: DataFrame):
        self.actionName = "transform operation"
        self._data = df

    def drop_invalid(self): 
        self._data = self._data.dropna()

        return self

    def drop_rowIds(self, ids: list):
        self._data = self._data.drop(ids, axis=0, errors='ignore')

        return self

    def drop_unnamed_cols(self):
        unnamed_cols = filter(lambda s: 'Unnamed: ' in s, self._data.columns)

        self._data = self._data.drop(unnamed_cols, axis=1)

        return self

    def transform_col_types(self):
        for c in _get_cols_with_dtype(self._data, 'O'):
            self._attempt_json_col(c)
        
        for c in filter(lambda x: '_normalised' in x, self._data.columns):
            self._attempt_normalised_col_distribution_and_save_to_csv(c)

        return self

    def _attempt_json_col(self, col):
        try:
            testClean = deep_clean(self._data[col].iloc[0])
            Deserializer().deserialize(testClean)

            _logger.info(f"serial JSON detected for '{col}'")

            assignKwargs = { 
                f'{col}_cleaned': lambda df: df[col].apply(deep_clean),
                f'{col}_dict': lambda df: df[f'{col}_cleaned'].apply(Deserializer().deserialize),
                f'{col}_normalised': lambda df: df[f'{col}_dict'].apply(pd.json_normalize),
            }

            self._data = (self._data
                .assign(**assignKwargs)
                .drop_empty_list_rows(f'{col}_dict')
                .drop([col, f'{col}_dict'], axis=1)
            )

            _logger.info(f"serial JSON successfully transformed for '{col}'")
        except Exception as e:
            _logger.warn(f"'{col}' was not JSON parsable with error '{e}'")
            return

    def _attempt_normalised_col_distribution_and_save_to_csv(self, col):
        pd.concat(self._data[col].to_list()).to_csv(f'{col}.csv')
        _logger.info(f"'{col}' was expanded to usable dataset and saved to csv of the same name")

    def get_data(self) -> DataFrame: return self._data


def _get_cols_with_dtype(df, tCol):
    col_dtypes = dict(df.dtypes)
    tCol_cols = list(filter(lambda key: col_dtypes[key] == np.dtype(tCol), list(col_dtypes.keys())))
    return tCol_cols
