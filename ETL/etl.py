from curses import raw
from .extractor import Extract
from .transformer import Transform


MAX_JSON_SIZE = 300

def DefaultPipeline(fileName: str, dropIds=[]):
    rawFrame = Extract(fileName)

    # cause im bad at regex and some of these rows are flippin' huge
    filteredFrame = rawFrame[rawFrame.columns[0].str.len() <= MAX_JSON_SIZE & rawFrame.columns[1].str.len() <= MAX_JSON_SIZE]

    transformedFrame = Transform(filteredFrame, dropIds)

    return transformedFrame
