

import os
import pandas as pd
from urllib.parse import urlparse
import sys
 

def check_match():
    ORIGIN_LINK_CORPUS="Corpus4.csv"
    data_path="newdata/"
    df_corpus = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    evidence_match_num=0
    news_match_num=0
    total_news_num=0
    total_evidence_num=0
    groupby_one_news=df_corpus.groupby(["Snopes URL" ])
    for snope_url, one_news in groupby_one_news:
        # print(snope_url)
        total_news_num+=1
        news_match=True
        groupby_one_evidence=one_news.groupby([ "Evidence"])
        for name, one_evidence in groupby_one_evidence:
            total_evidence_num+=1
            # print(name)
            match=False
            for _,row in one_evidence.iterrows(): 
                if row['Match'] == 'match':
                    match=True
                    break
            if not match:
                news_match=False
            else:
                evidence_match_num+=1
        if news_match:
            news_match_num+=1
    show_result(  evidence_match_num,total_evidence_num,data_path,news_match_num,total_news_num)

    double_check(data_path,df_corpus)
    
def double_check(data_path,df_corpus):
    groupby_one_news_1=df_corpus.groupby(["Evidence" ])
    evidence_match_num=0
    for _,row in df_corpus.iterrows():
        match=row["Match"]
        if match=="match":
            evidence_match_num+=1
    with open(data_path+"statistic.txt","a") as file:
        print(f'double check: evidence_match={evidence_match_num}, total={len(groupby_one_news_1)}' )

def show_result( match_total_num,total_num,data_path,news_match_num,total_news_num):
    
    # sorted_domain_dict=sorted(domain_dict.items(), key=lambda item: item[1],reverse=True)
    with open(data_path+"statistic.txt","w") as file:
        print(f'evidence match={match_total_num}, total={total_num}',file=file)
        print(f'news_match={news_match_num}, total={total_news_num}',file=file)
    #     for key,value in sorted_domain_dict :
    #         print(f"{key}, {value}",file=file)



check_match()