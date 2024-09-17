import re

from parsers.fourchanParser import fourchanParser
from parsers.fuukaArchiveParser import fuukaArchiveParser
from parsers.warosuParser import warosuParser

URL = input("Enter thread link: ")
#code expects a "/" at end
if URL[len(URL)-1]!= "/":
  URL = URL + "/"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}

domain = re.search(r"^https:\/\/[a-z0-9.-]+\/", URL).group()[8:].strip('/')

if domain == "boards.4chan.org":
  fourchanParser(URL,headers)
else:
  warosuParser(URL,headers)