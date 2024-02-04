import re
import pathlib

import requests
from bs4 import BeautifulSoup
from utils.mediaDownloader import mediaDownload

def fourchanParser(URL, headers, catbox):
  print('Scraping 4chan.')

  page = requests.get(URL, headers=headers)
  pageHTML = BeautifulSoup(page.content, "html.parser")

  imageLinks = pageHTML.find_all("a", {"class": "fileThumb"})

  threadID = re.search("\/([a-z0-9]{1,5})\/", URL).group().strip('/') + '_' + re.search("[0-9]+\/$", URL).group()

  print(str(len(imageLinks))+" thread media found.")

  pathlib.Path('./out/thread_'+threadID).mkdir(exist_ok=True)
  print("downloading to: " + './out/thread_'+threadID )


  for ind, a_tag in enumerate(imageLinks):
    print(str(ind+1) + " out of " + str(len(imageLinks)))
    mediaDownload("https:"+a_tag["href"], headers, threadID)

    #TODO: implement catbox and litterbox(which might exist)