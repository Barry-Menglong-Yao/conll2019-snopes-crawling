
from link_crawler.Image.Download import Download
from util.download import download
import os
import pandas as pd
from urllib.parse import urlparse
import sys
from newspaper import Article
import urllib.request
import pandas as pd
import newspaper
# import wget

data_path="../crawler/Results"
ORIGIN_LINK_CORPUS="LinkCorpus.csv"
#TODO url_to_crawl=os.path.join(data_path,ORIGIN_LINK_CORPUS)
out_dir="out/running"
url_to_crawl="util/tried_image_crawler/test_url2.csv"
 
def fetch_img():
    
    df_evidence = pd.read_csv(url_to_crawl ,encoding="utf8", header=None)
    domain_dict={}
    init()
    cur_snope_url=""
    snope_id=-1
    run_dir=gen_run_dir()
    for evidence_id,row in df_evidence.iterrows():
        snope_url=row[0]
        origin_doc_url=row[1]
        if snope_url!=cur_snope_url:
            cur_snope_url=snope_url
            snope_id+=1
        fetch_img_by_newspaper(origin_doc_url, snope_id,evidence_id,run_dir)

def gen_run_dir():
    dir_list = next(os.walk(out_dir))[1]

    max_run_id=0
    for dir in dir_list:
        run_id=int(dir[len(dir)-1:])
        max_run_id=max(run_id,max_run_id)
    return out_dir+"/run"+str(max_run_id+1)
 

def init():
    # Adding information about user agent
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
def fetch_img_by_newspaper(url, snope_id,evidence_id,run_dir):
    article = Article(url)
    try:
        article.download()
    
        article.parse()
    except newspaper.article.ArticleException as e:
        print(e)
        return
    filtered_imgs=[]
    for img_url in article.images:
        if ".svg" not in img_url:
            filtered_imgs.append(img_url)

 
    prefix=str(snope_id)+"-"+str(evidence_id)
    download = Download(run_dir,prefix,links=filtered_imgs)
    download.start()






fetch_img()