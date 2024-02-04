import re
import pathlib

import requests
from bs4 import BeautifulSoup
from utils.mediaDownloader import mediaDownload

#TODO: write multiple parsers, archive.moe with redirects, 4chan with api(?)

URL = input("Enter archive link: ")
catbox = input("Want to download catbox files as well?:[y/n] ")
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}

threadID = re.search("\/(\w)\/", URL).group()[1] + '_' + re.search("[0-9]+\/$", URL).group()

page = requests.get(URL, headers=headers)
pageHTML = BeautifulSoup(page.content, "html.parser")
imageLinks = pageHTML.find_all("a", {"class": "thread_image_link"})

print(str(len(imageLinks))+" thread media found.")

pathlib.Path('./out/thread_'+threadID).mkdir(exist_ok=True)
print("downloading to: " + './out/thread_'+threadID )


for ind, a_tag in enumerate(imageLinks):
  print(str(ind+1) + " out of " + str(len(imageLinks)))
  mediaDownload(a_tag["href"], headers, threadID)

if catbox == "y":
  print("Downloading catbox files")
  catboxLinks = pageHTML.find_all("a", {"href": re.compile(".+(files\.catbox\.moe\/)(.+)\.(png|jpg|jpeg|mp4|webm|gif)$")}) #ignore litterbox for now, as it is most likeley expired
  print(str(len(catboxLinks))+" catbox media found.")

  for ind, a_tag in enumerate(catboxLinks):
    print(str(ind+1) + " out of " + str(len(catboxLinks)))
    mediaDownload(a_tag["href"], headers, threadID)



