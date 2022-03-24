#!/usr/bin/env python3

import logging

from ETL import DefaultPipeline, HandleNormalisedFramesPipeline

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)


# Default pipeline config
# fn = "EmbeddedData\\TheMoviesDataset\\credits.csv"
# dropRowIds = [69061, 132166, 269843]
# loadedFrame = DefaultPipeline(fn, dropRowIds)

# Normalised frames 'semi-processed'
fileNames = [
    'cast_normalised',
    'crew_normalised'
]

for fn in fileNames:
    _logger.info("Beginning: Pipeline Run")
    
    loadedFrame = HandleNormalisedFramesPipeline(fn)

    _logger.info("Finished: Pipeline Run")

    _logger.info(loadedFrame.info())
    _logger.info(loadedFrame.head())
    
    loadedFrame.to_csv(f'{fn}_processed.csv')
