import logging

import numpy as np
from pandas import DataFrame

from .deserializer import Deserializer
from .stringCleaner import DeepClean

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)


class Transformer:
    def __init__(self, df: DataFrame):
        self.actionName = "transform operation"
        self._data = df
        self._deserializer = Deserializer()

    def Drop_Invalid(self): 
        self._data = self._data.dropna()

        return self

    def Drop_RowIds(self, ids: list):
        self._data = self._data.drop(ids, axis=0, errors='ignore')

        return self

    def Transform_Col_Types(self):
        for c in _getColsWithDtype(self._data, 'O'):
            self._attempt_json_col(c)

        return self

    def _attempt_json_col(self, col):
        try:
            testClean = DeepClean(self._data[col].iloc[0])
            self._deserializer.Deserialize(testClean)
            _logger.info(f"serial JSON detected for '{col}'")

            self._data.loc[:, col] = self._data[col].apply(DeepClean)
            # TODO: https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
            self._data.loc[:, col] = self._data[col].apply(self._deserializer.Deserialize)
            _logger.info(f"serial JSON successfully transformed for '{col}'")
        except Exception as e:
            _logger.warn(f"'{col}' was not JSON parsable with error '{e}'")
            return

    def GetData(self) -> DataFrame: return self._data

def Transform(df: DataFrame, dropIds=[]) -> DataFrame:
    if (df.shape[0] < 1): return df

    return (
        Transformer(df)
            .Drop_Invalid()
            .Drop_RowIds(dropIds)
            .Transform_Col_Types()
            .GetData()
    )


def _getColsWithDtype(df, tCol):
    col_dtypes = dict(df.dtypes)
    tCol_cols = list(filter(lambda key: col_dtypes[key] == np.dtype(tCol), list(col_dtypes.keys())))
    return tCol_cols
