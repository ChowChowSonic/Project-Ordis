import requests
from bs4 import BeautifulSoup
import DefaultVoiceSynthesizer as synth
from googlesearch import search

def googlesearch(query, wordtags):
    querytostring = ""
    try:
        for i in query:
            if not i[0] == "'":
                querytostring += i + " "
            else:
                querytostring += i
    except:
        querytostring = query
    query = querytostring

    results = search(query, tld='com', lang='en', num=5, start=0, stop=5, pause=2.0)
    filteredresults = []
    simpleresults = []
    synth.say("Here are the top five google results for " + query +
              ". Which result should I read off of for you?")
    print("Top google results found:")
    for result in results:
        simpleurl = result.split('/')[2]
        if simpleurl not in simpleresults:
            simpleresults.append(simpleurl)
            filteredresults.append(result)
    print(*simpleresults)
    return (simpleresults, filteredresults)

def findinfo(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    paragraphs = str(soup.findAll("p"))
    text = ""
    isinbracket = False
    for paragraph in range(len(paragraphs)):
        for i in range(len(paragraphs[paragraph])):
            if paragraphs[paragraph][i] == "<" or paragraphs[paragraph][i] == "[":
                isinbracket = True
            if not isinbracket:
                text += paragraphs[paragraph][i]
            if paragraphs[paragraph][i] == ">" or paragraphs[paragraph][i] == "]":
                isinbracket = False
    return text

def findperson(query, doesabsolutelynothing):
    querytostring = ""
    try:
        for i in query:
            if not i[0] == "'":
                querytostring += i + " "
            else:
                querytostring += i
    except:
        querytostring = query
    query = querytostring
    url = list(search(query, tld='com', lang='en', num=1, start=0, stop=1, pause=2.0))[0]
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    paragraphs = str(soup.findAll("p")[2])
    text = ""
    isinbracket = False
    for i in range(len(paragraphs)):
        if paragraphs[i] == "<" or paragraphs[i] == "[":
            isinbracket = True
        if not isinbracket:
            text += paragraphs[i]
        if paragraphs[i] == ">" or paragraphs[i] == "]":
            isinbracket = False

    return text

def getusefulinfo(content, question, taggedwords=""):
    contentlist = content.lower().split(".")
    rnge = [0,0]
    foundword = False
    #Set the initial position
    for sentencepos in range(len(contentlist)):
        for word in question:
            if word in contentlist[sentencepos]:
                rnge[0] = sentencepos
                foundword = True
                break
        if foundword:
            break

    #set the final position
    for sentencepos in range(len(contentlist)):
        for word in question:
            if word in contentlist[sentencepos]:
                rnge[1] = sentencepos
                question.remove(word)
                break
    if rnge[1] > 10:
        rnge[1] = 10
    print(rnge)
    smartcontent = ""
    #Change everything back to a string from a list[string]
    for i in range(rnge[0], rnge[1]+1):
        smartcontent += contentlist[i]
        print(contentlist[i])
    return smartcontent