import os
import time

import requests

#Download the media behind a given link.
def mediaDownload(link, headers, threadID):
  filename = link.split("/")[-1]
  if os.path.isfile("./out/thread_"+ threadID + '/' + filename):
    print(filename+' already exists. Skipping.')
  else:
    image = requests.get(link, headers=headers)
    if image.status_code == 200:
      print("Downloading " + link.split(".")[-1])
      path ="./out/thread_"+ threadID + link.split("/")[-1]
      with open(path, 'wb') as f:
        f.write(image.content)
      print("Saved: "+ filename + '\n-------------------')
    time.sleep(0.2) #wait to not trigger too many requests at once