from .extractor import extract
from .transformer import Transformer


MAX_JSON_SIZE = 300

def default_pipeline(file_name: str, drop_ids=[]):
    raw_frame = extract(file_name)

    # cause im bad at regex and some of these rows are flippin' huge
    colA = raw_frame.columns[0]
    colB = raw_frame.columns[1]
    filtered_frame = raw_frame[(raw_frame[colA].str.len() <= MAX_JSON_SIZE) & (raw_frame[colB].str.len() <= MAX_JSON_SIZE)]

    if (filtered_frame.shape[0] < 1): return filtered_frame

    return (
        Transformer(filtered_frame)
            .drop_invalid()
            .drop_rowIds(drop_ids)
            .transform_col_types()
            .get_data()
    )


def handle_normalised_frames_pipeline(file_name: str, drop_ids=[]):
    raw_frame = extract(file_name)

    return (
        Transformer(raw_frame)
            .drop_unnamed_cols()
            .drop_invalid()
            .drop_rowIds(drop_ids)
            .get_data()
    )
