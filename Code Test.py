import requests
from bs4 import BeautifulSoup
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

def getusefulinfo(content, question, taggedwords=""):
    question = question.lower().split(" ")[2:]
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


content = findinfo("https://en.wikipedia.org/wiki/Terry_Crews")
print(getusefulinfo(content, "who is terry crews"))