from .extractor import Extract
from .transformer import Transform


def DefaultPipeline(fileName: str, dropIds=[]):
    rawFrame = Extract(fileName)
    transformedFrame = Transform(rawFrame, dropIds)

    return transformedFrame
