import os
import pandas as pd
from urllib.parse import urlparse
import sys
from newspaper import Article
import urllib.request
# def download(filtered_imgs,save_dir,evidence_id):
    
#     for img_id,img_url  in enumerate(filtered_imgs):
       

#         try:
#             # Use wget download method to download specified image url.
#             image_filename = wget.download(img_url)

def download(filtered_imgs,save_dir,evidence_id):
    

    for img_id,img_url  in enumerate(filtered_imgs):
        # imgURL = "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"

        try:

            urllib.request.urlretrieve(img_url,  save_dir+"/"+str(evidence_id)+"-"+str(img_id)+".jpg")
        except Exception:
            print(f'{img_url} HTTP Error 403: Forbidden')
            continue