import re

import openai

GENRE_LIST = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western']
TONE_LIST = ['happy', 'sad', 'serious', 'humorous', 'threatening', 'pessimistic', 'optimistic', 'anxious', 'excited',
			 'depressing']
VOWELS = ['a', 'e', 'i', 'o', 'u']


class PlotIteration:
	def __init__(self, _logger, title: str, plot: str, imdb_rating: str, rt_rating: str, genre_rating: str, improvement: str):
		self.title = title
		self.plot = plot
		self.imdb_rating = imdb_rating
		self.rt_rating = rt_rating
		self.genre_rating = genre_rating
		self.improvement = improvement

		_logger.info(self)

	def __repr__(self):
		return f"""
			title       : {self.title}\n
            plot        : {self.plot}\n
            imdb_rating : {self.imdb_rating}\n
			rt_rating   : {self.rt_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n"""

	def __str__(self):
		return f"""
			title       : {self.title}\n
            plot        : {self.plot}\n
            imdb_rating : {self.imdb_rating}\n
			rt_rating   : {self.rt_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n"""


# def get_plot():
# 	plot_iters = run_movie_plot_tool()
# 	return filter(plot_iters, get_high_rating)


def get_raw_rating(raw_rating):
	extracted_rating = re.findall(r"\d+\.\d+", raw_rating)
	return extracted_rating[0]


def run_movie_plot_tool(_logger, _args) -> list:
	conf_openAi()

	plot_iters = []

	characters = get_characters(_logger, _args.character)
	init_prompt = generate_prompt_init(
		_logger,
		_args.genre, _args.tone, characters, _args.length
	)

	movie_plot = get_gpt3(init_prompt)
	title = get_title(movie_plot)

	imdb_rating = get_imdb_rating(movie_plot)
	rt_rating = get_rt_rating(movie_plot)
	genre_rating = get_genre(movie_plot, _args.genre)
	improvement = get_improvements(movie_plot)

	plot_iters.append(PlotIteration(
		_logger,
		title,
		movie_plot,
		imdb_rating,
		rt_rating,
		genre_rating,
		improvement
	))

	valid = True

	for i in range(1, _args.iterations):
		_logger.info(f"Loop: {i}")

		if not valid:
			validated = validatePlot(plot_iters[i - 1].plot, _args.genre)
		else:
			validated = plot_iters[i - 1].plot

		plot = (generate_improved_plot(validated, plot_iters[i - 1].improvement)).strip()
		title = get_title(movie_plot)
		imdb_rating = get_imdb_rating(plot)
		rt_rating = get_rt_rating(plot)
		genre_rating = get_genre(plot, _args.genre)
		improvement = get_improvements(plot)
		valid = valid_genre(genre_rating)

		plot_iters.append(PlotIteration(
			_logger,
			title,
			movie_plot,
			imdb_rating,
			rt_rating,
			genre_rating,
			improvement
		))

	_logger.info(plot_iters)
	return plot_iters


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################

def get_characters(_logger, characters):
	_logger.info("Getting characters for plot!")

	_characters = [c.strip() for c in characters.split(',')]

	_logger.info(f"Got characters {_characters}")

	return _characters


def get_gpt3(prompt, engine='text-davinci-002', max_tokens=3000,
			 temperature=1, top_p=1, frequency_penalty=0, presence_penalty=0):
	# TODO: Implement length of response from CLI input.
	response = openai.Completion.create(
		prompt=prompt,
		engine=engine,
		max_tokens=max_tokens,
		temperature=temperature,
		top_p=top_p,
		frequency_penalty=frequency_penalty,
		presence_penalty=presence_penalty,
	)

	answer = response.choices[0]['text']

	return cleanOutput(answer)


def generate_prompt_init(_logger, genre, tone, characters, length):
	model_prompt = "Write an original movie plot using the following criteria " \
				   "criteria: \n" + \
				   "Genre: " + genre + "\n"
	if tone:
		model_prompt += "Tone: " + tone + "\n"
	if characters and len(characters) > 0:
		model_prompt += f"Characters: {' '.join(characters)}\n"
	if length:
		model_prompt += f"Length: {length}\n"

	_logger.info(f"Model prompt constructed: {model_prompt}\n")

	print(20 * "*")
	print(model_prompt)
	print(20 * "*")

	return model_prompt


def validatePlot(plot, genre):
	prompt = "Turn this plot into a " + genre + " plot: " + plot + "\n\n"
	print(prompt + '\n')
	return get_gpt3(prompt)


def generate_improved_plot(plot, improvements):
	model_prompt = "This is a movie plot: \n" + plot + "\n" \
				   + "Improve the plot using the following suggestions: \n" + improvements + '\n\n'

	print(20 * "*")
	print(model_prompt)
	print(20 * "*")
	return get_gpt3(model_prompt)


def get_imdb_rating(movie):
	prompt = "On a scale of 0.0 to 10.0, (eg. 6.5) give this plot an imdb rating: \n" + movie + '\n\n'
	print(prompt + '\n')
	raw_imdb_out = get_gpt3(prompt)
	return get_raw_rating(raw_imdb_out)


def get_rt_rating(movie):
	prompt = "On a scale of 0.0 to 10.0, (eg. 6.5) give this plot a rotten tomatoes rating: \n" + movie + '\n\n'
	print(prompt + '\n')
	raw_rt_out = get_gpt3(prompt)
	print("Raw: " + raw_rt_out)
	cleaned_rt_rating = get_raw_rating(raw_rt_out)
	print("Cleaned: " + cleaned_rt_rating)
	percentage_rating = "{:.0%}".format(float(cleaned_rt_rating) / 10)
	print("Percentage: " + percentage_rating)
	return percentage_rating


def get_title(movie):
	prompt = "Create a title for this movie plot: \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)


def get_genre(movie, genre):
	if genre[0] in VOWELS:
		grammar = 'n '
	else:
		grammar = ' '

	prompt = "Is this a" + grammar + genre + " movie plot? \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)


def get_improvements(movie):
	prompt = "Provide some ideas of how this movie plot could be improved: \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)


# TODO: Adam's suggestion
def getSocialSatisfaction():
	prompt = "Is this plot gender or culturally diverse?"
	return get_gpt3(prompt)


def cleanOutput(output):
	output = re.sub('\n', '', output)
	output = re.sub("'", '', output)
	output = re.sub('"', '', output)
	return output


def valid_genre(output):
	if re.search("no", output.lower()):
		return False
	else:
		return True


def conf_openAi():
	openAi_Api_key = "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"

	openai.api_key = openAi_Api_key
