import re

from parsers.fourchanParser import fourchanParser
from parsers.fuukaArchiveParser import fuukaArchiveParser

URL = input("Enter thread link: ")
#code expects a "/" at end
if URL[len(URL)-1]!= "/":
  URL = URL + "/"

catbox = input("Want to download catbox files as well?:[y/n] ") == "y"
hydrus = input("Want to add files to hydrus?[y/n]") == "y"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}

domain = re.search("^https:\/\/[a-z0-9.-]+\/", URL).group()[8:].strip('/')

if domain == "boards.4chan.org":
  fourchanParser(URL,headers, catbox, hydrus)
else:
  fuukaArchiveParser(URL,headers,catbox,domain, hydrus)