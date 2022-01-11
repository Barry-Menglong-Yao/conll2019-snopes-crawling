
import os
import pandas as pd
from urllib.parse import urlparse
import sys
from utils.statistic_helper import *





def label_statistic(data_path):
    evidence_corpus="Corpus2.csv"
    df_evidence = pd.read_csv(os.path.join(data_path,evidence_corpus) ,encoding="utf8")
    cur_claim_id=-2
    label_num={"supported":0,"refuted":0,"NEI":0,"other":0}
    for _,row in df_evidence.iterrows():
        claim_id=row["claim_id"]
        truthfulness=row["Truthfulness"]
        if claim_id !=cur_claim_id:
            cleaned_truthfulness=gen_cleaned_truthfulness(truthfulness)
            label_num[cleaned_truthfulness]+=1
            cur_claim_id=claim_id
    print(label_num)
    # print(df_evidence["cleaned_truthfulness"].value_counts())
    
    sum=0
    for num in label_num.values():
        sum+=num
    print(f"remaining instance:{sum-label_num['other']}")


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
    print(f"claim: {count}, evidence: {len(df_evidence)}")
    
def instance_completeness_statistic(data_path):
    evidence_corpus="Corpus2.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,evidence_corpus) ,encoding="utf8")
    cur_snope_url=-2
    claim_dict={}
    count=0
    print(df_evidence.isnull().sum())
    for _,row in df_evidence.iterrows():
        claim_id=row["claim_id"] 
        ruling_outline=row["ruling_outline"] 
        evidence=row["Evidence"] 
        if not pd.isna(ruling_outline) and not pd.isna(evidence):
            count+=1
        else:
            pass


    print(f"perfect instance: {count}")

def corpus3_statistic(data_path):
    
    ORIGIN_LINK_CORPUS="Corpus3.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    
    cur_snope_url=""
    snope_url_dict={}
    count=0
    
     
    
    # print(snope_url_dict)
    print(f"relevant_document: {len(df_evidence)}")     


def statistic(data_path):
    label_statistic(data_path)
    corpus2_statistic(data_path)
    corpus3_statistic(data_path)
    instance_completeness_statistic(data_path)




if __name__ == '__main__':
     
    # data_path="mode3_latest_v4"
    data_path="final_corpus/politifact_v1"
    # data_path="mode3_latest_v4/test"
    statistic(data_path)
    
    
    # show_dataset_example(data_path)
    # check_removed_label(data_path)
    