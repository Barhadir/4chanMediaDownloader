import re
import pathlib

import requests
from bs4 import BeautifulSoup
from utils.mediaDownloader import mediaDownload

#TODO: write multiple parsers, archive.moe with redirects, 4chan with api(?)

URL = input("Enter archive link: ")
catbox = input("Want to download catbox files as well?:[y/n] ")
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}
page = requests.get(URL, headers=headers)
pageHTML = BeautifulSoup(page.content, "html.parser")
imageLinks = pageHTML.find_all("a", {"class": "thread_image_link"})
threadID = re.search("\/(\w)\/", URL).group()[1] + '_' + re.search("[0-9]+\/$", URL).group()
pathlib.Path('./out/thread_'+threadID).mkdir(exist_ok=True)
print("downloading to: " + './out/thread_'+threadID )

for a_tag in imageLinks:
  mediaDownload(a_tag["href"], headers, threadID)

if catbox == "y":
  print("Downloading catbox files")
  catboxLinks = pageHTML.find_all("a", {"href": re.compile(".+(files\.catbox\.moe\/)(.+)\.(png|jpg|jpeg|mp4|webm|gif)$")}) #ignore litterbox for now, as it is most likeley expired

  for a_tag in catboxLinks:
    mediaDownload(a_tag["href"], headers, threadID)



