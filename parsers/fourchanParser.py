import re
import pathlib

import requests
from bs4 import BeautifulSoup
from utils.mediaDownloader import mediaDownload
from utils.hydrusImporter import hydrusImport

def fourchanParser(URL, headers, catbox, hydrus):
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
    # mediaDownload("https:"+a_tag["href"], headers, threadID)
    hydrusImport(URL, "https:"+a_tag["href"], threadID)

    #TODO: implement catbox and litterbox(which might exist)
  if catbox:
    print("Downloading catbox files")
    replies = pageHTML.find_all("blockquote", class_='postMessage')
    catboxLinks = []
    for reply in replies: 
      pattern = re.compile("(https\:\/\/(files|litter)\.catbox\.moe\/([\w\d])+\.(png|jpg|jpeg|mp4|webm|gif))")
      pos = 0
      while (match := pattern.search(reply.text, pos)) is not None:
        pos = match.start() + 1
        catboxLinks.append(match[1])
    
    print(str(len(catboxLinks))+" catbox media found.")

    for ind, link in enumerate(catboxLinks):
      print(str(ind+1) + " out of " + str(len(catboxLinks)))
      print(link)
      if hydrus: 
        hydrusImport(URL, link, threadID)