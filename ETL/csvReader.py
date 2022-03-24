import pandas as pd


def CsvReader(fName, idx_col) -> pd.DataFrame:
    df = pd.read_csv(
        _fixFileNameEnding(fName),
        index_col=idx_col,
        memory_map=True,
        low_memory=False
    )
        
    return df


def _fixFileNameEnding(fName):
        if not fName.endswith('.csv'):
            fName = fName + '.csv'

        return fName

