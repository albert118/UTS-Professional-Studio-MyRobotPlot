from .extractor import Extract
from .transformer import Transform


MAX_JSON_SIZE = 300

def DefaultPipeline(fileName: str, dropIds=[]):
    rawFrame = Extract(fileName)

    # cause im bad at regex and some of these rows are flippin' huge
    colA = rawFrame.columns[0]
    colB = rawFrame.columns[1]
    filteredFrame = rawFrame[(rawFrame[colA].str.len() <= MAX_JSON_SIZE) & (rawFrame[colB].str.len() <= MAX_JSON_SIZE)]

    transformedFrame = Transform(filteredFrame, dropIds)

    return transformedFrame
