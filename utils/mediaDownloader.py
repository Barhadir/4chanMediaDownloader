import os
import time

import requests

#Download the media behind a given link.
def mediaDownload(link, headers):
  filename = link.split("/")[-1]
  if os.path.isfile("./out/" + filename):
    print(filename+' already exists. Skipping.')
  else:
    image = requests.get(link, headers=headers)
    if image.status_code == 200:
      print("Downloading " + link.split(".")[-1])
      with open("./out/" + link.split("/")[-1], 'wb') as f:
        f.write(image.content)
      print("Saved: "+ filename)
    time.sleep(0.5) #wait to not trigger too many requests at once