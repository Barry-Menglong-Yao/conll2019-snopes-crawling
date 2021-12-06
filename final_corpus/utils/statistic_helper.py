

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
        snope_url=row[0]
        origin_doc_url=row[1]
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
    with open("out/statistic.txt","w") as file:
        for key,value in sorted_domain_dict :
            print(f"{key}, {value}",file=file)




data_path="crawler/Results"    
def gen_top_domain_list(n):
    top_domain_list=[]
    file_name=os.path.join( "out", "statistic.txt") 
     
    df = pd.read_csv(file_name, delimiter = ", ", header=None)
    i=0
    for _,row in df.iterrows():
        domain=row[0]

        if "archive" not in domain:
            i+=1
            top_domain_list.append(domain)
        if i>=n:
            break
    return top_domain_list


def evidence_from_top():
    ORIGIN_LINK_CORPUS="LinkCorpus.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    relevant_dict={}
    cur_snope_url=""
    cur_relevant_doc_url=[]
    
    for _,row in df_evidence.iterrows():
        snope_url=row[0]
        origin_doc_url=row[1]
        
        if snope_url==cur_snope_url:
            cur_relevant_doc_url.append(origin_doc_url)
        else:
            relevant_dict[cur_snope_url]=cur_relevant_doc_url
            cur_relevant_doc_url=[]
            cur_relevant_doc_url.append(origin_doc_url)
            cur_snope_url=snope_url

    
    top_domain_list=gen_top_domain_list(10)
    doc_in_top_count=0
    for snope_url,relevant_doc_urls in relevant_dict.items():
        are_all_in_top=True
        for relevant_doc_url in relevant_doc_urls:
            if not in_top(relevant_doc_url,top_domain_list):
                are_all_in_top=False
                break 
        if are_all_in_top:
            doc_in_top_count+=1

    with open("out/only_use_top_evidence_website.txt","w") as file:
        print(f"total news {len(relevant_dict)}",file=file)
        print(f"news whose evidences are only from top n: {doc_in_top_count}",file=file)

def in_top(relevant_doc_url,top_domain_list):
    domain = fetch_domain(relevant_doc_url)        
    if domain in top_domain_list:
        return True
    else:
        return False


def statistic1():
    data_path="crawler/crawler/Results/run005_snopes_10k/Results"
    ORIGIN_LINK_CORPUS="Corpus2.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    
    cur_snope_url=""
    snope_url_dict={}
    count=0
    
    for _,row in df_evidence.iterrows():
        snope_url=row[0]
        origin_doc_url=row[1]
        
        if snope_url !=cur_snope_url:
            count+=1
            cur_snope_url=snope_url
            snope_url_dict[snope_url]=1
        else:
            snope_url_dict[snope_url]+=1
    
    # print(snope_url_dict)
    print(count)
    
    num_dict={}
    for key,value in snope_url_dict.items():
        if value   in num_dict.keys():
            num_dict[value]+=1
        else:
            num_dict[value]=1
    print(num_dict)


label_map={"supported":['Mostly True','Correct Attribution','MOSTLY TRUE', 'TRUE', 'Was true.', 'Was true, but the program has since ended.',  'Was true; now outdated', 'True, but the boycott has ended.',  'TRUE:',  'Status: True.', 'PARTLY TRUE',  'TRUE BUT OUTDATED', 'PROBABLY TRUE', 'Partly true.',  'PArtly true.', 'True', 'True.', 'True.', 'CORRECT ATTRIBUTION', 'CORRECTLY ATTRIBUTED' ],
               "refuted":['Labeled Satire','Miscaptioned','Mostly False','FALSE', 'False', 'FALSE:', 'False.', 'MOSTLY FALSE', 'MOSTLY FALSE:', 'Status: False.',  'INCORRECT ATTRIBUTION',  'INCORRECTLY ATTRIBUTED'],
               "NEI":['Unproven', 'UNDETERMINED', 'UNPROVEN', 'Undetermined.', 'Mixture', 'Mixture.', 'Multiple - see below.', 'Multiple - see below:', 'Multiple:', 'MISATTRIBUTED', 'MISCAPTIONED', 'MIXED ATTRIBUTION', 'MIXTURE', 'MIXTURE OF ACCURATE AND INACCURATE INFORMATION', 'MIXTURE OF CORRECT AND INCORRECT ATTRIBUTIONS', 'MIXTURE OF REAL AND FAKE IMAGES', 'MIXTURE OF TRUE AND FALSE INFORMATION', 'MIXTURE OF TRUE AND FALSE INFORMATION:', 'MIXTURE OF TRUE AND OUTDATED INFORMATION', 'MIXTURE OF TRUE, FALSE, AND OUTDATED INFORMATION:']}
def gen_cleaned_truthfulness(truthfulness):
    for label in ["supported","refuted","NEI"]:
        if truthfulness in label_map[label]:
            return label
    return "other"

def check_removed_label(data_path):
    evidence_corpus="Corpus2.csv"
    df_evidence = pd.read_csv(os.path.join(data_path,evidence_corpus) ,encoding="utf8")
    cur_claim_id=-2
    label_num={}
    for _,row in df_evidence.iterrows():
        claim_id=row["claim_id"]
        truthfulness=row["Truthfulness"]
        if claim_id !=cur_claim_id:
            is_found=False
            for label in ["support","refuse","NEI"]:
                if truthfulness in label_map[label]:
                    is_found=True
                    break
            if not is_found:
                if truthfulness in label_num.keys():
                    label_num[truthfulness]+=1
                else:
                    label_num[truthfulness]=1
            cur_claim_id=claim_id
    print(label_num)
    
    sum=0
    for num in label_num.values():
        sum+=num
    print(sum)

def statistic2():
    data_path="crawler/crawler/Results/run005_snopes_10k/Results"
    ORIGIN_LINK_CORPUS="Corpus3.csv"
    
    df_evidence = pd.read_csv(os.path.join(data_path,ORIGIN_LINK_CORPUS) ,encoding="utf8")
    
    cur_snope_url=""
    snope_url_dict={}
    count=0
    
    for _,row in df_evidence.iterrows():
        snope_url=row[0]
        origin_doc_url=row[1]
        
        if snope_url !=cur_snope_url:
            count+=1
            cur_snope_url=snope_url
            snope_url_dict[snope_url]=1
        else:
            snope_url_dict[snope_url]+=1
    
    # print(snope_url_dict)
    print(count)
     


def fetch_domain(origin_doc_url):
    domain = urlparse(origin_doc_url).netloc
    return domain


if __name__ == '__main__':
    # evidence_from_top()
    # relevant_docs_statistic()
    statistic1()