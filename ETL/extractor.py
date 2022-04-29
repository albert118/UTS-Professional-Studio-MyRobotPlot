import logging

from pandas import DataFrame

from .csv_reader import csv_reader

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self, fType = 'csv'):
        if fType != 'csv':
            _logger.warn(f"the only supported file type is CSV currently")

        self.fType = fType
        self.action_name = "load operation"
        self._data = DataFrame()

    def load(self, fn, idx_col):
        try:
            self._data = csv_reader(fn, idx_col)
        except FileNotFoundError:
            _logger.warn(f"File not found {fn} when running {Extractor.__name__} {self.action_name}")
        except ValueError as e:
            if str(e) == "Index id invalid":
                _logger.warn(f"Index Id '{idx_col}' was invalid, attempting hot-reload with default")
                return self.load(fn, None)
            else:
                raise
        finally:
            return self

    def get_data(self): return self._data


def extract(file_name: str, fType = 'csv', default_index_col = 'id') -> DataFrame:
    if len(file_name) == 0:
        _logger.warn(f"fName must be set with '{Extractor.__name__}'")
        return DataFrame()
    
    return(
        Extractor(fType)
            .load(file_name, default_index_col)
            .get_data()
    )
