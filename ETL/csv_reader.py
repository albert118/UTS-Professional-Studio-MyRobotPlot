import pandas as pd


def csv_reader(fName, idx_col) -> pd.DataFrame:
    df = pd.read_csv(
        _fix_file_name_ending(fName),
        index_col=idx_col,
        memory_map=True,
        low_memory=False
    )
        
    return df


def _fix_file_name_ending(fName):
        if not fName.endswith('.csv'):
            fName = fName + '.csv'

        return fName

