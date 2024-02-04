import os

import requests
from bs4 import BeautifulSoup

URL = input("Enter archive link: ")
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("a", {"class": "thread_image_link"})

for a_tag in results:
    link = a_tag["href"]
    filename = link.split("/")[-1]
    if os.path.isfile("./out/" + filename):
      print(filename+' already exists. Skipping.')
    else:
      image = requests.get(link)
      if image.status_code == 200:
        with open("./out/" + link.split("/")[-1], 'wb') as f:
          f.write(image.content)
        print("Saved: "+ filename)

#Scrape catbox links ending in png/jpg/jpeg/webm/gif