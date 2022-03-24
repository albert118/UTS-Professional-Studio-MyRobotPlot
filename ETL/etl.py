from .extractor import Extract
from .transformer import Transformer


MAX_JSON_SIZE = 300

def DefaultPipeline(fileName: str, dropIds=[]):
    rawFrame = Extract(fileName)

    # cause im bad at regex and some of these rows are flippin' huge
    colA = rawFrame.columns[0]
    colB = rawFrame.columns[1]
    filteredFrame = rawFrame[(rawFrame[colA].str.len() <= MAX_JSON_SIZE) & (rawFrame[colB].str.len() <= MAX_JSON_SIZE)]

    if (filteredFrame.shape[0] < 1): return filteredFrame

    return (
        Transformer(filteredFrame)
            .Drop_Invalid()
            .Drop_RowIds(dropIds)
            .Transform_Col_Types()
            .GetData()
    )


def HandleNormalisedFramesPipeline(fileName: str, dropIds=[]):
    rawFrame = Extract(fileName)

    return (
        Transformer(rawFrame)
            .Drop_Unnamed_Cols()
            .Drop_Invalid()
            .Drop_RowIds(dropIds)
            .GetData()
    )
