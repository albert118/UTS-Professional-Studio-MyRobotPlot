import argparse
import logging

from .common.file_handler import normalise_filepath
from .etl import default_pipeline, handle_normalised_frames_pipeline
from .plot_builder import builder

GENRE_LIST = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western']
TONE_LIST = ['happy', 'sad', 'serious', 'humorous', 'threatening', 'pessimistic', 'optimistic', 'anxious', 'excited', 'depressing']
VOWELS = ['a','e', 'i', 'o', 'u']

class MovieCriteria:
	def __init__(self, _logger, genre: str, tone: str, character: str, length: int, iterations: int):
		self.genre = genre
		self.tone = tone
		self.character = character
		self.length = length
		self.iterations = iterations
		_logger.info(self)

def web_tool(user_selection):
	_logger = setup_logger()
	_args = MovieCriteria(_logger=_logger, genre=user_selection['genre'], tone=user_selection['tone'], character=user_selection['characters'],
						  length=user_selection['plot_length'], iterations=user_selection['iterations'])
	print(_args)
	plot_iters = builder.run_movie_plot_tool(_logger, _args)


	print(10*"*")
	print("PLOT BUILDER FINISHED")
	print(plot_iters[-1].plot)
	print(10*"*")

	return plot_iters[-1].plot

def main():

	_logger = setup_logger()
	_args = setup_argparser(_logger)
	print(_args)
	builder.run_movie_plot_tool(_logger, _args)

def show_pipeline_results(df, logger):
	logger.info(df.info())
	logger.info(df.head())

def setup_logger():
	LOG_LVL = logging.NOTSET
	logging.basicConfig(level=LOG_LVL)
	return logging.getLogger(__name__)

def setup_argparser(_logger):
	_parser = init_argparser()
	_args = _parser.parse_args()
	check_args(_args, _logger)

	return _args

def check_args(_args, _logger):
	if _args.tone and _args.tone.lower() not in TONE_LIST:
		_logger.error('Tone must be from list: happy, sad, serious, humorous, threatening, pessimistic, optimistic, anxious, excited, depressing.')
	if _args.genre.lower() not in GENRE_LIST:
		_logger.error('Genre must be from list: action, comedy, drama, fantasy, horror, mystery, romance, thriller, western.')

def init_argparser():
	_parser = argparse.ArgumentParser(
		description="::::::::TODO::::::::"
	)

	_parser.add_argument("-g", "--genre", type=str,
						help="Genre of the movie you want generated. Choose from action, comedy, drama, fantasy, horror, mystery, romance, thriller, western"
	)

	_parser.add_argument("-t", "--tone", type=str,
						help="Tone of the plot you want generated. Choose from happy, sad, serious, humorous, threatening, pessimistic, optimistic, anxious, excited, depressing"
	)

	_parser.add_argument("-c", '--character', type=str,
						help="Characters you want in the movie. Can be existing movie characters or made up. Separate characters by comma. E.g., 'Alice, Howin'"
	)

	_parser.add_argument("-l", '--length', type=int,
						help="Length of the movie plot you want return in characters. Recommended value 250"
	)

	_parser.add_argument("-i", '--iterations', type=int, default=2,
						help="Number of iterations the movie plot should be improved with (defaults to 2)"
	)

	_parser.add_argument("--preprocessing-pipelines", action="store_true",
		help="Run the data preprocessing pipelines"
	)

	return _parser

def run_pipelines(_logger):
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

if __name__ == "__main__":
	main()