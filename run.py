#!/usr/bin/env python3

import logging

from ETL import *

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)


fn = "EmbeddedData\\TheMoviesDataset\\credits.csv"
dropRowIds = [69061, 132166, 269843]

_logger.info("Beginning: Default Pipeline Run")
loadedFrame = DefaultPipeline(fn, dropRowIds)
_logger.info("Finished:  Default Pipeline Run")

_logger.info(loadedFrame.info())
_logger.info(loadedFrame.head())

loadedFrame.to_csv('cleaned.csv')
