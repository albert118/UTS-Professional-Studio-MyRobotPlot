import re
import openai

GENRE_LIST = ['action','anime', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western']
TONE_LIST = ['happy', 'sad', 'serious', 'humorous', 'threatening', 'pessimistic', 'optimistic', 'anxious', 'excited', 'depressing']
VOWELS = ['a','e', 'i', 'o', 'u']


class PlotIteration:
    def __init__(self, _logger, plot: str, star_rating: str, genre_rating: str, improvment: str,character: bool):
        self.plot = plot
        self.star_rating = star_rating
        self.genre_rating = genre_rating
        self.improvement = improvment
        self.char_confirm = character
        _logger.info(self)

    def __repr__(self):
        return f"""
            plot        : {self.plot}\n
            stars       : {self.star_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n
            character_Confirm: {self.char_confirm}\n"""

    def __str__(self):
        return f"""
            plot        : {self.plot}\n
            stars       : {self.star_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n
            character_Confirm: {self.char_confirm}\n"""

def get_plot():
    plot_iters = run_movie_plot_tool()
    return filter(plot_iters, get_high_rating)

def get_high_rating():
    pass


#Inital Start ---
def run_movie_plot_tool(_logger, _args) -> list:
    conf_openAi()
    
    plot_iters = []
    
    characters = get_characters(_logger, _args.character)
    
    init_prompt = generate_prompt_init(
        _logger,
        _args.genre, _args.tone, characters, _args.length
    )

    movie_plot = get_gpt3(init_prompt)
    char_confirm = confirm_chars(_logger, movie_plot,characters)
    star_rating = get_rating(movie_plot)
    genre_rating = get_genre(movie_plot, _args.genre)
    improvement = get_improvements(movie_plot)

    plot_iters.append(PlotIteration(
        _logger,
        movie_plot,
        star_rating,
        genre_rating,
        improvement,
        char_confirm
    ))
    
    valid = True

    for i in range(1, _args.iterations):
        _logger.info(f"Loop: {i}")

        if not valid: 
            validated = validatePlot(plot_iters[i - 1].plot, _args.genre)
        else: 
            validated = plot_iters[i - 1].plot

        if not char_confirm:
            validated  = validate_char(validated,characters)
        
        plot = (generate_improved_plot(validated, plot_iters[i - 1].improvement)).strip()
    
        star_rating = get_rating(plot)
        genre_rating = get_genre(plot, _args.genre)
        improvement = get_improvements(plot)
        valid = valid_genre(genre_rating)
        char_confirm = confirm_chars(_logger,plot,characters)
        plot_iters.append(PlotIteration(
            _logger,
            plot,
            star_rating,
            genre_rating,
            improvement,
            char_confirm,
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

def validate_char(plot,character):
    prompt = "Make this plot with characters " + character + " :" + plot + "\n\n"
    print(prompt + '\n')

    return get_gpt3(prompt)

def confirm_chars(_logger, plot,character):
    confirm_array = []
    for i in range(len(character)):

        if (character[i].lower() in plot.lower()):
            _logger.info("{0}, character is present".format(character[i]))
            confirm_array.append(True)
        else:
            _logger.info("{0}, character is not present".format(character[i]))
            confirm_array.append(False)
    
    for s in range(len(confirm_array)):
        if (confirm_array[s] == True):
            pass
        else:
            return False
            #retrying

    return True

def get_gpt3(prompt, engine='text-davinci-002', max_tokens=3000,
            temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0):

    # TODO: Implement length of response from CLI input. 
    response = openai.Completion.create(
        prompt=prompt + '>',
        engine=engine,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop = '>'
    )

    answer = response.choices[0]['text']

    return cleanOutput(answer)

def generate_prompt_init(_logger, genre, tone, characters, length): 
    model_prompt = "Write a movie plot with\n" + \
                    "Genre: " + genre + "\n" 
    if tone:
        model_prompt += "Tone: " + tone + "\n"
    if characters and len(characters) > 0:
        model_prompt += f"Characters: {', '.join(characters)}\n"
    if length:
        model_prompt += f"Length: {length}\n"

    _logger.info(f"Model prompt constructed: {model_prompt}\n")

    return model_prompt

def validatePlot(plot, genre):
    prompt = "Turn this plot into a " + genre + " plot: " + plot + "\n\n"
    print(prompt + '\n')
    return get_gpt3(prompt)

def generate_improved_plot(plot, improvements): 

    model_prompt = "Improve this movie plot: " + plot + '\n' \
                    + " Using this advice: " + improvements + '\n\n'
    
    print(model_prompt + '\n')
    return get_gpt3(model_prompt)

def get_rating(movie):
    prompt = "What is this movie plot's IMDB rating: " + movie + '\n\n'
    print(prompt + '\n')
    return get_gpt3(prompt)

def get_genre(movie, genre):
    if genre[0] in VOWELS:
        grammar = 'n '
    else: 
        grammar = ' '

    prompt = "Is this a" + grammar + genre + " movie plot? " + movie + '\n\n'
    print(prompt + '\n')
    return get_gpt3(prompt,max_tokens= 3)

def get_improvements(movie):
    prompt = "How can this movie plot be improved? "+ movie + '\n\n'
    print(prompt + '\n')
    return get_gpt3(prompt)


# TODO: Adam's suggestion
def getSocialSatisfaction():
    prompt = "Is this plot gender or culturally diverse?" 
    return get_gpt3(prompt)

def cleanOutput(output):
    output = re.sub('\n', '', output)
    output = re.sub("'",'', output)
    output = re.sub('"','', output)
    return output

def valid_genre(output):
    if re.search("no", output.lower()):
        return False
    else: 
        return True

def conf_openAi():
    openAi_Api_key = "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" #Howin's API Key

    openai.api_key = openAi_Api_key
