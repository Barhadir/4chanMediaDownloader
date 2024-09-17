import re
import time

import requests
from bs4 import BeautifulSoup
from utils.hydrusImporter import hydrusImport, fchanMedia

catboxPattern = re.compile(r"(https\:\/\/(files|litter)\.catbox\.moe\/([\w\d])+\.(png|jpg|jpeg|mp4|webm|gif))")

def warosuParser(URL, headers):
     print('Scraping warosu.org')
     #normalize url
     if URL[-1] == "/":
          URL = URL[:-1]
     URL = URL.split("#")[0]

     page = requests.get(URL, headers=headers)
     pageHTML = BeautifulSoup(page.content, "html.parser")

     board = re.search(r"\/([a-z0-9]{1,5})\/", URL).group().strip('/')
     threadID = re.search(r"[0-9]{2,}$", URL).group()

     threadPosts = pageHTML.find_all("table") #posts are tables

     # every post: check for image or catbox links
     for post in threadPosts:
          media = fchanMedia()
          media.links = []

          media.board = board

          media.threadID = str(threadID)
          postSoup = BeautifulSoup(str(post), "html.parser") 
          
          tds = postSoup.find_all("td")
          media.postID = ""
          postbody = tds[0]
     
          for td in tds:
               if "id" in td.attrs.keys():
                    media.postID = td["id"].replace("p", "")
                    postbody = td
                    break

          media.links.append(URL + "#p" +media.postID)
          
          bodySoup = BeautifulSoup(str(postbody), "html.parser")
          posttxt = ""
          if bodySoup.find("blockquote") is not None:
               posttxt = bodySoup.find("blockquote").text
          
          catboxLinks = []
          pos = 0
          while (match := catboxPattern.search(posttxt, pos)) is not None:
            pos = match.start() + 1
            catboxLinks.append(match[1])

          if len(catboxLinks) > 0:
            print("Found " + str(len(catboxLinks)) + " catbox links for post " + media.postID)

          for link in catboxLinks:
            catboxMedia = media
            try: 
              catboxMedia.mediaBytes = None

              catboxMedia.mediaBytes = requests.get(link, headers=headers).content

              catboxMedia.links.append(link)
              catboxMedia.filename = link.split("/")[-1]

              hydrusImport(catboxMedia)
            except:
              print("Couldn't get " + link)

          for img in bodySoup.find_all("img"):
               if img.parent.name == "a":
                    relMediaLink = img.parent["href"]
                    media.mediaBytes = requests.get(relMediaLink, headers=headers).content
                    media.links.append(relMediaLink)
                    hydrusImport(media)
                    time.sleep(0.2)
                    

          


                    
          
          