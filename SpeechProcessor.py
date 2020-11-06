import nltk.corpus
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.corpus import conll2000
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from WebCrawler import findperson
from playsound import playsound
import DefaultVoiceSynthesizer as synth
import AudioRecorder as recorder
import WebCrawler
import random
import cv2
import os

PRONOUN = 'PRON'
CONJECTION = 'CONJ'
ADJECTIVE = 'ADJ'
PARTICLE = 'PRT'
VERB = 'VERB'
ADPOSITION = 'ADP'
ADVERB = 'ADV'
DETERMINER, ARTICLE = 'DET', 'DET'
NOUN = 'NOUN'
NUMERAL = 'NUM'
PUNCTUATION = '.'
NOTAPPLICABLE = 'None'
operators = ('plus', 'minus', 'times', 'divided', 'over', 'and', 'END')
numerals = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
            'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
            'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty',
            'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand')
numbconstants = (
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000)

print("Initializing word comprehension", end='')
chunker_training = brown.tagged_sents(tagset='universal') + \
                   treebank.tagged_sents(tagset='universal') + \
                   conll2000.tagged_sents(tagset='universal')
                 #  webtext.tagged_sents(tagset='universal')
print('.', end='')
backup_chunker = nltk.tag.UnigramTagger(train=chunker_training)
print('.', end='')
word_chunker = nltk.tag.BigramTagger(train=chunker_training, backoff=backup_chunker)
print('.')
googlesearch = WebCrawler.googlesearch

# Oh for FUCKS SAKE I'M BACK TO PUTTING THE METHODS AT THE TOP OF THE FILE
def tagtext(text):
    if not isinstance(text, str):
        taggedtext = []
        for i in text:
            taggedtext.append(word_chunker.tag(i))
    else:
        taggedtext = word_chunker.tag(text)
    return taggedtext

def findAudio(filename):
    supportedfiletypes = [".mp3", ".wav"]
    possiblefiles = []
    shortnames = []
    for root, dirs, file in os.walk("C:", topdown=True):
        for name in file:
            for filetype in supportedfiletypes:
                if name.lower() == filename.lower()+filetype:
                    possiblefiles.append(os.path.join(root,name))
                    shortnames.append(name)
    return possiblefiles, shortnames

def findVideo(filename):
    supportedfiletypes = [".avi"]
    possiblefiles = []
    shortnames = []
    for root, dirs, file in os.walk("C:", topdown=True):
        for name in file:
            for filetype in supportedfiletypes:
                if name.lower() == filename.lower() + filetype:
                    possiblefiles.append(os.path.join(root, name))
                    shortnames.append(name)
    return possiblefiles, shortnames

def getresults(words, taggedwords):
    results, urls = googlesearch(words, taggedwords)
    speech = recorder.recordandrecognise()
    if not speech.lower() == "cancel":
        number = parsenumber([speech])
        print(number)
        info = WebCrawler.findinfo(urls[number - 1])
        return info
    else:
        return "Ok, i'm here if you need me"

def parsenumber(numbers):
    try:
        if type(numbers) == type("string"):
            result = int(numbers)
        elif type(numbers) == type(["list"]) and len(numbers) == 1:
            result = int(numbers[0])
        return result
    except:
        result = 1
    for i in range(0,len(numbers)):
        if i == 0 and numbers[0] in numerals:
            print(True)
            result = numbconstants[numerals.index(numbers[0])]
        if numbers[i] == 'hundred':
            if i == 1:
                result *= 100
            else:
                if numbers[i-2] in numerals[20:28]:
                    result+= 100*(numbconstants[numerals.index(numbers[i-1])] +
                              numbconstants[numerals.index(numbers[i-2])])
                    result-=(numbconstants[numerals.index(numbers[i-1])] +
                              numbconstants[numerals.index(numbers[i-2])])
                else:
                    result+= numbconstants[numerals.index(numbers[i-1])]*100
                    # The line below is to account for the final if statement
                    result -= numbconstants[numerals.index(numbers[i - 1])]
        if numbers[i] == 'thousand':
            if i ==1:
                result *= 1000
            else:
                if numbers[i - 2] in numerals[20:28]:
                    if numbers[i-3] == 'hundred':
                        result += 1000 * ((numbconstants[numerals.index(numbers[i - 4])]*100)+numbconstants[numerals.index(numbers[i - 1])] +
                                          numbconstants[numerals.index(numbers[i - 2])])
                        result -= ((numbconstants[numerals.index(numbers[i - 4])]*100)+numbconstants[numerals.index(numbers[i - 1])] +
                                   numbconstants[numerals.index(numbers[i - 2])])
                    else:
                        result += 1000 * (numbconstants[numerals.index(numbers[i - 1])] +
                                     numbconstants[numerals.index(numbers[i - 2])])
                        result -= (numbconstants[numerals.index(numbers[i - 1])] +
                        numbconstants[numerals.index(numbers[i - 2])])

                else:
                    result += numbconstants[numerals.index(numbers[i - 1])] * 1000
                    # The line below is to account for the final if statement
                    result -= numbconstants[numerals.index(numbers[i-1])]
        if numbers[i] in numerals[0:28] and i > 0: # Numerals[0:28] includes everything but the multipliers
            result += numbconstants[numerals.index(numbers[i])]
    return result

def parsefunction(numbers, taggedwords):
    numbers = numbers.split()
    functions = []
    temp = []
    #remove all unnescisary words
    for num in numbers:
        if num != 'by':
            temp.append(num)
    numbers = temp.copy()
    numbers.append('END')
    temp = []
    for num in numbers:
        if num in operators:
            functions.append(temp.copy())
            temp = []
            if num != 'END':
                functions.append(num)
        else:
            temp.append(num)
    # Order to follow: [[number1], function1, [number2], [function2], [number3]...]
    result = parsenumber(functions[0])
    print(functions[0])
    for i in range(len(functions)):
        func = functions[i]
        try:
            if func in operators:
                if func == 'and' or func == 'plus':
                    result+=parsenumber(functions[i+1])
                elif func == 'minus':
                    result -=parsenumber(functions[i+1])
                elif func == 'divided' or func == 'over':
                    result /= parsenumber(functions[i+1])
                elif func == 'multiplied' or func == 'times':
                    result *= parsenumber(functions[i+1])
        except Exception as e:
            print(e.args)
    return result


def what(words, taggedwords):
    if words[1] == "is":
        request = words[2:]
        tagrequest = taggedwords[2:]
    elif words[0] == "what's":
        request = words[1:]
        tagrequest = taggedwords[1:]
    else:
        request = words
        tagrequest = taggedwords

    if (tagrequest[0][1] == NUMERAL) and (tagrequest[-1][1] == NUMERAL):
        func = ""
        for word in request:
            func+= word + " "
        print(func)
        return parsefunction(func.strip(), tagrequest)
    else:
        return getresults(words, taggedwords)

def where(words, taggedwords):
    if words[0] == "where's":
        locationname = words[1:]
    elif words[1] == "is":
        locationname = words[2:]

    words.append("location")
    return getresults(words, taggedwords)

def why(words, taggedwords):
    return getresults(words, taggedwords)

def when(words, taggedwords):
    return getresults(words, taggedwords)

def how(words, taggedwords):
    if words[1] == "are":
        request = words[2:]
        tagrequest = taggedwords[2:]
    elif words[0] == "how're":
        request = words[1:]
        tagrequest = taggedwords[1:]
    else:
        request = words
        tagrequest = taggedwords

    if request[0] == "you":
        response = ""
        if tagrequest[1][1] == VERB:
            response =  "I am " + request[1] + " fine. "
            randomint = random.randint(0,4)
            if randomint == 0:
                response += "Thanks for asking."
            elif randomint == 1:
                response +="How are you?"
            elif randomint == 2:
                response += "How about you?"
        else:
            response = "I'm fine, thanks."
    else:
        return getresults(words, taggedwords)
    return response

def are(words, taggedwords):
    if(words[1] == "you"):
        sentimentScore = 0
        sentimentReader = SentimentIntensityAnalyzer()
        for word in words[2:]:
            sentimentScore += sentimentReader.polarity_scores(word)["compound"]
        if(sentimentScore >= 0):
            return "yes"
        else:
            return "no"

def playmedia(file, uselessvariable):
    filename = ""
    for word in file[1:]:
        filename+= word + " "
    filename = filename.strip()
    possibleaudio, audionames = findAudio(filename)
    possiblevideo, videonames = findVideo(filename)
    if len(videonames) == 0 and len(audionames) == 0:
        synth.say("Sorry, I couldn't find any audio or video with that name")
        return
    elif len(videonames) > 0 and len(audionames) > 0:
        synth.say("Do you want a song or a video?")
        input = recorder.recordandrecognise()
        synth.say("Here's a list of what I've found. What number in the list should I play?")
    elif len(videonames) == 0 and len(audionames) > 0:
        print("Audio found:", audionames)
        input = "song"
    elif len(videonames) > 0 and len(audionames) == 0:
        print("Video found:", videonames)
        input = "video"

    if input == "song":
        if len(audionames) > 1:
            print("Audio found:", audionames)
            input = parsenumber(recorder.recordandrecognise())
            print(input)
            playsound(possibleaudio[input - 1])
        else:
            playsound(possibleaudio[0])
    elif input == "video":
        if len(videonames) > 1:
            print("Video found:", videonames)
            input = parsenumber(recorder.recordandrecognise())
            cap = cv2.VideoCapture(possiblevideo[input - 1])
        else:
            cap = cv2.VideoCapture(possiblevideo[0])
        while (cap.isOpened()):
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cap.release()
            cv2.destroyAllWindows()

def comprehendspeech(words):
    # Define constants for each word type et. al.
    word_tags = word_chunker.tag(nltk.tokenize.word_tokenize(words.lower()))
    words = nltk.tokenize.word_tokenize(words.lower())
    print(words, word_tags)
    # Now let's actually do stuff
    for i in range(len(words)):
        try:
            int(words[i])
            word_tags[i] = (words[i], "NUM")
        except:
            pass
    #results = ""
    if word_tags[0][1] != VERB:
        firstwords = {
            "who": findperson,
            "what": what,
            "what's": what,
            "when": when,
            "where": where,
            "why": why,
            "how": how,
            "how're": how,
            "are": are,
            "is": are
        }
        if len(words) > 0:
            results = firstwords.get(words[0], getresults)(words, word_tags)
            if isinstance(results, type("string")):
                usefulresults = WebCrawler.getusefulinfo(results, words)
            else:
                usefulresults = results
            if not usefulresults == "":
                synth.say(usefulresults)
            else:
                synth.say("I can't find anything of use on this page.")
    else:
        firstverbs ={
            "play": playmedia
        }
        try:
            firstverbs.get(words[0], getresults)(words, word_tags)
        except:
            pass

# ITS LIKE TRYING TO LEARN C ALL OVER AGAIN