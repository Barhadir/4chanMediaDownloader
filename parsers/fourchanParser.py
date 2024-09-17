import re

import json
import time

import requests
from utils.hydrusImporter import hydrusImport, fchanMedia

catboxPattern = re.compile(r"(https\:\/\/(files|litter)\.catbox\.moe\/([\w\d])+\.(png|jpg|jpeg|mp4|webm|gif))")

def fourchanParser(URL, headers):
  print('Scraping 4chan.')
  if URL[-1] == "/":
    URL = URL[:-1]

  URL = URL.split("#")[0]
  apiURL = URL.replace("boards.4chan","a.4cdn") + ".json"

  print(URL)

  thread = requests.get(apiURL, headers=headers)
  threadJSON = json.loads(thread.content.decode("utf-8"))

  board = re.search(r"\/([a-z0-9]{1,5})\/", URL).group().strip('/')
  threadID = re.search(r"[0-9]{2,}$", URL).group()

  posts = threadJSON["posts"]

  for post in posts: 
    media = fchanMedia()
    media.links = []

    media.board = board

    media.threadID = str(threadID)
    media.postID = str(post["no"])

    media.links.append("https://archived.moe/" + board + "/thread/" + str(threadID))

    if "com" in post:
      media.notes["post text"]= post["com"].replace("<wbr>", "").replace("\\", "")

      #parse catbox and litterbox
      catboxLinks = []
      pos = 0
      while (match := catboxPattern.search(post["com"], pos)) is not None:
        pos = match.start() + 1
        catboxLinks.append(match[1])
      
      if len(catboxLinks) > 0:
        print("Found " + str(len(catboxLinks)) + " catbox links for post " + media.postID)

      for link in catboxLinks:
        link = link.replace("<wbr>", "")
        catboxMedia = media
        try: 
          catboxMedia.mediaBytes = None
          
          catboxMedia.mediaBytes = requests.get(link, headers=headers).content

          catboxMedia.links.append(link)
          catboxMedia.filename = link.split("/")[-1]

          hydrusImport(catboxMedia)
        except:
          print("Couldn't get " + link)

    if "tim" in post:
      relMedia = str(post["tim"]) + str(post["ext"])

      media.filename = post["filename"] + post["ext"]

      relMediaLink = "https://i.4cdn.org/" + board + "/" + relMedia

      media.mediaBytes = requests.get(relMediaLink, headers=headers).content
      media.links.append(relMediaLink)

      hydrusImport(media)