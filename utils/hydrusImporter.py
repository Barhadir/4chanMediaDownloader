import requests
import time

import os
import logging

import json

from PIL import Image

hydrus_url = "http://127.0.0.1:45869/"
api_access_key = "727d10fdcdd0616a6fb7aa7a19a05140f9c0d1ead0ff56d731108163d9db9b35";
firefoxHeaders = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}

class fchanMedia:
     links = []
     notes = {
          "post text": ""
     }
     board = ""
     threadID = ""
     postID = ""
     filename = ""
     mediaBytes = None

def hydrusImport(media: fchanMedia): 
     
     response = requests.post(hydrus_url + "add_files/add_file", media.mediaBytes, headers= { "Content-Type": "application/octet-stream",
               "Hydrus-Client-API-Access-Key": api_access_key})
          

     hydrusHash = json.loads(response.content)["hash"]

     for link in media.links:
          requests.post(hydrus_url + "add_urls/associate_url", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key}, 
          json={
               "url_to_add": link,
               "hash": hydrusHash,
          }) 

     requests.post(hydrus_url + "add_tags/add_tags", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key},
          json={
              "hash": hydrusHash,
              "service_names_to_tags": {
                  "my tags":  [ "import_source:external_api_call", "filename:" + media.filename, "board:" + media.board, "thread: " +
                               media.threadID, "post: " + media.postID ]
              }
          })
     
     requests.post(hydrus_url + "add_notes/set_notes", headers= {"Content-Type": "application/json", 
          "Hydrus-Client-API-Access-Key": api_access_key}, 
          json={
               "notes": media.notes,
               "hash": hydrusHash
          })
     print("Imported image: "+ hydrusHash)