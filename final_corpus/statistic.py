
import os
import pandas as pd
from urllib.parse import urlparse
import sys
from utils.statistic_helper import *





def label_statistic(data_path):
    evidence_corpus="Corpus2.csv"
    df_evidence = pd.read_csv(os.path.join(data_path,evidence_corpus) ,encoding="utf8")
    cur_claim_id=-2
    label_num={"support":0,"refuse":0,"NEI":0}
    for _,row in df_evidence.iterrows():
        claim_id=row["claim_id"]
        truthfulness=row["Truthfulness"]
        if claim_id !=cur_claim_id:
            cleaned_truthfulness=gen_cleaned_truthfulness(truthfulness)
            label_num[cleaned_truthfulness]+=1
            cur_claim_id=claim_id
    print(label_num)
    
    sum=0
    for num in label_num.values():
        sum+=num
    print(sum)


def corpus2_statistic(data_path):
    
    ORIGIN_LINK_CORPUS="Corpus2.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    
    cur_snope_url=-2
    snope_url_dict={}
    count=0
    
    for _,row in df_evidence.iterrows():
        snope_url=row["claim_id"]#row["Snopes URL"]
        
        if snope_url !=cur_snope_url:
            count+=1
            cur_snope_url=snope_url
            snope_url_dict[snope_url]=1
        else:
            snope_url_dict[snope_url]+=1
    
    # print(snope_url_dict)
    print(f"{count} evidence:{len(df_evidence)}")
    

def corpus3_statistic(data_path):
    
    ORIGIN_LINK_CORPUS="Corpus3.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    
    cur_snope_url=""
    snope_url_dict={}
    count=0
    
     
    
    # print(snope_url_dict)
    print(f"{len(df_evidence)}")     


if __name__ == '__main__':
    # label_statistic("mode3_latest_v3")
    # check_removed_label("mode3_latest_v3")
    data_path="mode3_latest_v4"
    # label_statistic(data_path)
    # corpus2_statistic(data_path)
    corpus3_statistic(data_path)
    # check_removed_label("mode3_latest_v4") #TODO only print num>100