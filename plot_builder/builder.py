import re

import openai

from .plot_iteration import PlotIteration

# Options user can choose from - genre & tone. More options can be added. 
GENRE_LIST = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western']
TONE_LIST = ['happy', 'sad', 'serious', 'humorous', 'threatening', 'pessimistic', 'optimistic', 'anxious', 'excited',
			 'depressing']
VOWELS = ['a', 'e', 'i', 'o', 'u']

################################################################################
# 								Runners
################################################################################

def run_movie_plot_tool(_logger, _args, openAiApiKey='OPEN API KEY HERE') -> list:
	conf_openAi(openAiApiKey)

	plot_iters = []

	characters = get_characters(_logger, _args.character)			# Gather the characters from string input 
	init_prompt = generate_prompt_init(								# Establish the initial prompt 
		_logger,
		_args.genre, _args.tone, characters, _args.length
	)

	movie_plot = get_gpt3(init_prompt)								# Get first movie plot from GPT-3
	title = get_title(movie_plot)									# Get movie title of movie movie plot 

	imdb_rating = get_imdb_rating(movie_plot)						# Get IMDb rating
	rt_rating = get_rt_rating(movie_plot)							# Get Rotten Tomatoes rating
	genre_rating = get_genre(movie_plot, _args.genre)				# Get genre rating from initial input 
	improvement = get_improvements(movie_plot)						# Get suggested inputs 

	plot_iters.append(PlotIteration(								# Append above information to an iterable 
		_logger,
		title,
		movie_plot,
		imdb_rating,
		rt_rating,
		genre_rating,
		improvement
	))

	valid = True

	"""This loop is the 'validator' feature of GPT-3. The movie plot will be put through multiple validation 
	tests to (potentially) be improved. Each iteration will be logged into an iterable and best one will be 
	determined by the star rating or human interpretation. """

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

################################################################################
# 								Utils
################################################################################

def get_characters(_logger, characters):
	_logger.info("Getting characters for plot!")

	_characters = [c.strip() for c in characters.split(',')]

	_logger.info(f"Got characters {_characters}")

	return _characters

"""
Using Open AI's API and text-davinci-002 engine. Can choose from the following engines 
	- text-davinci-002				- davinci-instruct-beta
	- text-curie-001				- davinci
	- text-babbage-001				- curie-instruct-beta
	- text-ada-001					- curie
	- text-davinci-001				- babbage
	- ada
"""
def get_gpt3(prompt, engine='text-davinci-002', max_tokens=3000,
			 temperature=1, top_p=1, frequency_penalty=0, presence_penalty=0):

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

# Function that generates the initial prompt 
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

# Function to validate plot is of same genre as input 
def validatePlot(plot, genre):
	prompt = "Turn this plot into a " + genre + " plot: " + plot + "\n\n"
	print(prompt + '\n')
	return get_gpt3(prompt)

# Function to improve plot based on the suggestions made by GPT-3
def generate_improved_plot(plot, improvements):
	model_prompt = "This is a movie plot: \n" + plot + "\n" \
				   + "Improve the plot using the following suggestions: \n" + improvements + '\n\n'

	print(20 * "*")
	print(model_prompt)
	print(20 * "*")
	return get_gpt3(model_prompt)

# Function to get IMDb rating of movie plot from GPT-3 
def get_imdb_rating(movie):
	prompt = "On a scale of 0.0 to 10.0, (eg. 6.5) give this plot an imdb rating: \n" + movie + '\n\n'
	print(prompt + '\n')
	raw_imdb_out = get_gpt3(prompt)
	return get_raw_rating(raw_imdb_out)

# Function to get Rotton Tomatoes rating of movie plot from GPT-3 
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

# Function to get title of movie plot from GPT-3 
def get_title(movie):
	prompt = "Create a title for this movie plot: \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)

# Function to get genre of a movie plot from GPT-3
def get_genre(movie, genre):
	if genre[0] in VOWELS:
		grammar = 'n '
	else:
		grammar = ' '

	prompt = "Is this a" + grammar + genre + " movie plot? \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)

# Function to get improvements of a movie plot from GPT-3
def get_improvements(movie):
	prompt = "Provide some ideas of how this movie plot could be improved: \n" + movie + '\n\n'
	print(prompt + '\n')
	return get_gpt3(prompt)

# Function to get social satisfaction score of a movie plot from GPT-3
def getSocialSatisfaction():
	prompt = "Is this plot gender or culturally diverse?"
	return get_gpt3(prompt)

# Cleans the return outputs from GPT by removing '\n' and quotations
def cleanOutput(output):
	output = re.sub('\n', '', output)
	output = re.sub("'", '', output)
	output = re.sub('"', '', output)
	return output

# Function to check whether returned output is valid or not by searching for the term 'no'
def valid_genre(output):
	if re.search("no", output.lower()):
		return False
	else:
		return True

# Function to get the raw rating of the movie plot from GPT-2
def get_raw_rating(raw_rating):
	try:
		extracted_rating = re.findall(r"\d+\.\d+", raw_rating)
	except:
		extracted_rating = re.findall(r"\d+", raw_rating)

	return extracted_rating[0]

# Extract API key
def conf_openAi(openAiApiKey: str):
	openai.api_key = openAiApiKey
