
from link_crawler.Image.Download import Download
 
import os
import pandas as pd
from urllib.parse import urlparse
import sys
from newspaper import Article
import urllib.request
import pandas as pd
import newspaper
from newspaper import Config
# import wget

data_path="../crawler/Results_mode1"
ORIGIN_LINK_CORPUS="LinkCorpus.csv"
url_to_crawl=os.path.join(data_path,ORIGIN_LINK_CORPUS)
out_dir="out/running"
url_to_crawl="util/tried_image_crawler/test_url.csv"
 
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
            try:
                fetch_img_by_newspaper(snope_url, snope_id,"S",run_dir)
            except Exception as e:
                print(e)
        try:
            fetch_img_by_newspaper(origin_doc_url, snope_id,evidence_id,run_dir)
        except Exception as e:
            print(e)

def gen_run_dir():
    dir_list = next(os.walk(out_dir))[1]

    max_run_id=0
    for dir in dir_list:
        run_id=int(dir[len(dir)-3:])
        max_run_id=max(run_id,max_run_id)
    return out_dir+"/run"+"{:0>3d}".format(max_run_id+1)
 

def init():
    # Adding information about user agent
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
def fetch_img_by_newspaper(url, snope_id,evidence_id,run_dir):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    article = Article(url, config=config)
    
    article.download()

    article.parse()
    
 
    

    filtered_imgs=filter(article.images)
    prefix=str(snope_id).zfill(5)+"-"+str(evidence_id).zfill(5)
    download = Download(run_dir,prefix,links=filtered_imgs)
    download.start()


def filter(images):
    filter_flags=[".svg",".gif",".ico","lazyload",".cgi","logo","-ad-","Logo",".php","icon","Bubble","svg%","rating-false",
    "rating-true","banner","-line"]
    filtered_imgs=[]
    for img_url in  images:
        should_remove=False
        for filter_flag in filter_flags:
            if  filter_flag   in img_url   :
                should_remove=True
        if not should_remove:    
            filtered_imgs.append(img_url)
    return filtered_imgs



fetch_img()