import requests
from bs4 import BeautifulSoup
import re
import lxml.html
#import DefaultVoiceSynthesizer as synth
from googlesearch import search

def findaddress(location):
    '''<div jstcache="811"
    class="ugiz4pqJLAG__primary-text gm2-body-2"
    jsan="7.ugiz4pqJLAG__primary-text,7.gm2-body-2">
    Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France
    </div>'''
    html = requests.get("http://www.google.com/maps/place/"+location).content
    tree = BeautifulSoup(html, "lxml")
    attribs = {
    "jstcache":"811",
    "class":"ugiz4pqJLAG__primary-text gm2-body-2",
    "jsan":"7.ugiz4pqJLAG__primary-text,7.gm2-body-2"
               }
    for node in tree:
        print(node)
        print()

print(findaddress("eiffel+tower"))