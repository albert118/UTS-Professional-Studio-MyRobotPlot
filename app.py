import logging

from etl import default_pipeline, handle_normalised_frames_pipeline
from common.file_handler import normalise_filepath

def main():
    _logger = setup_logger()

    # Run initial pipeline
    raw_file_path = "data\\raw_data\\TheMoviesDataset\\credits.csv"
    default_pipeline(normalise_filepath(raw_file_path), [69061, 132166, 269843])
    
    # Normalised frames 'semi-processed'
    file_names = [
        normalise_filepath('data\\processed_data\\normalised_frames\\cast_normalised'),
        normalise_filepath('data\\processed_data\\normalised_frames\\crew_normalised')
    ]
    
    for fn in file_names:
        _logger.info("Beginning: Pipeline Run")
        
        loaded_frame = handle_normalised_frames_pipeline(fn)
    
        _logger.info("Finished: Pipeline Run")
    
        show_pipeline_results(loaded_frame, _logger)
        
        loaded_frame.to_csv(f'{normalise_filepath(fn)}_processed.csv')

def setup_logger():
    LOG_LVL = logging.NOTSET
    logging.basicConfig(level=LOG_LVL)
    return logging.getLogger(__name__)

def show_pipeline_results(df, logger):
    logger.info(df.info())
    logger.info(df.head())
