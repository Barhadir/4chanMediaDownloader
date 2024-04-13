import requests
import time

import os

import json

from PIL import Image

hydrus_url = "http://127.0.0.1:45869/"
api_access_key = "727d10fdcdd0616a6fb7aa7a19a05140f9c0d1ead0ff56d731108163d9db9b35";
firefoxHeaders = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}


def hydrusImport(threadURL, link, threadID, filename = None): 
     if filename == None:
          filename = link.split("/")[-1]

     # Get media

     image = requests.get(link, headers=firefoxHeaders)
     if (image.status_code != 200): 
          print("Error:" + image.status_code)
          return

     imageData = image.content

     path ="./out/thread_"+ threadID + link.split("/")[-1]
     with open(path, 'wb') as f:
        f.write(image.content)

     # read tags from image data

     metadata = Image.open("/home/barhadir/Documents/Files/ComfyUI/output/ComfyUI_00032_.png")

     # Add media to hydrus

     hydrusResponse = requests.post(hydrus_url + "add_files/add_file", headers= { "Content-Type": "application/json",
          "Hydrus-Client-API-Access-Key": api_access_key}, json={
              "path": os.path.abspath(path)
          }) 

     hydrusResponseJSON = json.loads(hydrusResponse.content)

     # add urls to hydrus file

     addUrlResponse = requests.post(hydrus_url + "add_urls/associate_url", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key}, 
          json={
               "url_to_add": threadURL,
               "hash": hydrusResponseJSON["hash"],
          }) 
     addUrlResponse1 = requests.post(hydrus_url + "add_urls/associate_url", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key}, 
          json={
               "url_to_add": link,
               "hash": hydrusResponseJSON["hash"],
          }) 

     # add tags to hydrus file

     print(requests.post(hydrus_url + "add_tags/add_tags", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key},
          json={
              "hash": hydrusResponseJSON["hash"],
              "service_names_to_tags": {
                  "my tags":  [ "import_source:external_api_call", "filename:" + filename, "board:" + threadID.split("_")[0] ]
              }
          }))
     
     os.remove(path)
     time.sleep(0.2)