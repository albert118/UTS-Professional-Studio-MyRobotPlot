import logging
import re
from argparse import ArgumentParser

import openai

GENRE_LIST = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western']
TONE_LIST = ['happy', 'sad', 'serious', 'humorous', 'threatening', 'pessimistic', 'optimistic', 'anxious', 'excited', 'depressing']
OPENAI_KEY = "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"
VOWELS = ['a','e', 'i', 'o', 'u']

def check_param(args):
    # TODO: fix logging
    if args.tone and args.tone.lower() not in TONE_LIST: 
        pass
        #logging.error('Tone must be from list: happy, sad, serious, humorous, threatening, pessimistic, optimistic, anxious, excited, depressing.')
    if args.genre.lower() not in GENRE_LIST:
        pass
        #logging.error('Genre must be from list: action, comedy, drama, fantasy, horror, mystery, romance, thriller, western.')

def getCharacters(args):
    # TODO: If we want to specify main/secondary characters

    if re.search(',', args): 
        characters = []
        for i in re.findall('[^,]+', args):
            characters.append(i.strip())
    return characters

def getGPT3(prompt, engine='text-davinci-002', max_tokens=3000,
            temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0):

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

def generatePromptInit(genre, tone, characters, length): 
    model_prompt = "Write a movie plot with\n" + \
                    "Genre: " + genre + "\n" 
    if args.tone: 
        model_prompt += "Tone: " + tone + "\n" 
    if args.character: 
        model_prompt += "Characters: " + characters + "\n" 
    if args.length: 
        model_prompt += "Length: " + length + "\n" 

    print(model_prompt + '\n')
    return model_prompt

def validatePlot(plot, genre):
    prompt = "Turn this plot into a " + genre + " plot: " + plot + "\n\n"
    print(prompt + '\n')
    return getGPT3(prompt)

def generateImprovedPlot(plot, improvements): 

    model_prompt = "Improve this movie plot - " + plot \
                    + " Using this advice - " + improvements + '\n\n'
    
    print(model_prompt + '\n')
    return getGPT3(model_prompt)

def getRating(movie):
    prompt = "On a scale of 1-5, rate this movie plot - " + movie + '\n\n'
    print(prompt + '\n')
    return getGPT3(prompt)

def getGenre(movie, genre):
    if genre[0] in VOWELS:
        grammar = 'n '
    else: 
        grammar = ' '

    prompt = "Is this a" + grammar + genre + " movie plot? " + movie + '\n\n'
    print(prompt + '\n')
    return getGPT3(prompt)

def getImprovements(movie):
    prompt = "How can this movie plot be improved? "+ movie + '\n\n'
    print(prompt + '\n')
    return getGPT3(prompt)

# TODO: Adam's suggestion
def getSocialSatisfaction():
    prompt = "Is this plot gender or culturally diverse?" 
    return getGPT3(prompt)

def cleanOutput(output):
    output = re.sub('\n', '', output)
    output = re.sub("'",'', output)
    output = re.sub('"','', output)
    return output 

def validGenre(output):
    if re.search("no", output.lower()):
        return False
    else: 
        return True

if __name__=='__main__':

    master = []
    
    openai.api_key = OPENAI_KEY

    parser = ArgumentParser()

    parser.add_argument("-g", "--genre", type=str, required=True,
                        help="Genre of the movie you want generated. Choose from action, comedy, drama, fantasy, horror, mystery, romance, thriller, western.")
    parser.add_argument("-t", "--tone", type=str,
                        help="Tone of the plot you want generated. Choose from happy, sad, serious, humorous, threatening, pessimistic, optimistic, anxious, excited, depressing.")
    parser.add_argument("-c", '--character', type=str, 
                        help="Characters you want in the movie. Can be existing movie characters or made up. Separate characters by comma. E.g., 'Alice, Howin'")
    parser.add_argument("-l", '--length', type=int, 
                        help="Length of the movie plot you want return in characters. Recommended value 250.")
    parser.add_argument("-i", '--iterations', type=int, default=5, 
                        help="Number of iterations the movie plot should be improved with.")
    args = parser.parse_args()
    
    check_param(args)
    
    characters = getCharacters(args.character)
    # print(characters)

    movie_plot = getGPT3(generatePromptInit(args.genre, args.tone, args.character, args.length))
    starRating = getRating(movie_plot)
    genreRating = getGenre(movie_plot, args.genre)
    improvement = getImprovements(movie_plot)

    temp = {"plot": movie_plot,
            "stars": starRating,
            "relevancy": genreRating,
            "improvement": improvement}
    master.append(temp)

    print("==========================================================================================")
    
    valid = True

    for i in range(1,args.iterations):
        temp = []
        print("Loop: ", i)
        # print("Plot is relevant to genre: " + str(valid))
        if not valid: 
            validated = validatePlot(master[i-1]['plot'], args.genre)
        else: 
            validated = master[i-1]['plot']
        
        plot = (generateImprovedPlot(validated, master[i-1]['improvement'])).strip()
        starRating = getRating(plot)
        genreRating = getGenre(plot, args.genre)
        improvement = getImprovements(plot)
        valid = validGenre(genreRating)

        temp = {"plot": plot,
            "stars": starRating,
            "relevancy": genreRating,
            "improvement": improvement}

        master.append(temp)

        print("==========================================================================================")

    print(master)

