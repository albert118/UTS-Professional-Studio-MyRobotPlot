import logging

from pandas import DataFrame

from .csvReader import CsvReader

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self, fType = 'csv'):
        if fType != 'csv':
            _logger.warn(f"the only supported file type is CSV currently")

        self.fType = fType
        self.actionName = "load operation"
        self._data = DataFrame()

    def Load(self, fName, idx_col):
        try:
            self._data = CsvReader(fName, idx_col)
        except FileNotFoundError:
            _logger.warn(f"File not found {fName} when running {Extractor.__name__} {self.actionName}")
        except ValueError as e:
            if str(e) == "Index id invalid":
                _logger.warn(f"Index Id '{idx_col}' was invalid, attempting hot-reload with default")
                return self.Load(fName, None)
            else:
                raise
        finally:
            return self

    def GetData(self): return self._data


def Extract(fName: str, fType = 'csv', default_index_col = 'id') -> DataFrame:
    if len(fName) == 0:
        _logger.warn(f"fName must be set with '{Extractor.__name__}'")
        return DataFrame()
    
    return(
        Extractor(fType)
            .Load(fName, default_index_col)
            .GetData()
    )
