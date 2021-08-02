

import os
import pandas as pd
from urllib.parse import urlparse
import sys
def relevant_docs_statistic():
    ORIGIN_LINK_CORPUS="LinkCorpus.csv"
    data_path="crawler/Results"
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    domain_dict={}
    for _,row in df_evidence.iterrows():
        snope_url=row["Snopes URL"]
        origin_doc_url=row["Original Link URL"]
        domain_of_origin_doc=fetch_domain(origin_doc_url)
        if domain_of_origin_doc not in domain_dict:
            count=1
            domain_dict[domain_of_origin_doc] = count
        else:
            count=domain_dict[domain_of_origin_doc]
            count+=1
            domain_dict[domain_of_origin_doc]=count
    show_result(domain_dict)

def show_result(domain_dict):
    sorted_domain_dict=sorted(domain_dict.items(), key=lambda item: item[1],reverse=True)
    with open("multi_media/out/statistic.txt","w") as file:
        for key,value in sorted_domain_dict :
            print(f" {key}:  {value}",file=file)
    

def fetch_domain(origin_doc_url):
    domain = urlparse(origin_doc_url).netloc
    return domain


if __name__ == '__main__':
    relevant_docs_statistic()