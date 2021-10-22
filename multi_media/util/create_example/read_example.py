import os
from util.create_example.example import Example
import pandas as pd

 
 
def read_example(data_path):
    
    evidence_corpus=os.path.join(data_path,"Corpus2.csv")
    relevant_doc_corpus=os.path.join(data_path,"Corpus3.csv")
    image_corpus=os.path.join(data_path,"images")

    example_dict={}
    df_news = pd.read_csv(evidence_corpus ,encoding="utf8")
    for _,row in df_news.iterrows():
        claim_id=row["claim_id"]
         
        if claim_id in example_dict:
            example=example_dict[claim_id]
            example.add_evidence(row["Evidence"])
        else:
            example=Example(claim_id,row["Snopes URL"],row["Evidence"],row['Claim'],row['Truthfulness'],row['Origin'])
            example_dict[claim_id]=example

    df_relevant_doc = pd.read_csv(relevant_doc_corpus ,encoding="utf8")
    for _,row in df_relevant_doc.iterrows():
        claim_id=row["claim_id"]
         
        if claim_id in example_dict:
            example=example_dict[claim_id]
            example.add_relevant_doc(row["Origin Document"])
         

    img_list=os.listdir(image_corpus)
    for img_name in img_list:
        prefix=img_name[:14]
        ids=prefix.split("-")
        claim_id= int(ids[0]) 
        evidence_id=ids[1]
        img_id=ids[2]
        if claim_id in example_dict:
            example=example_dict[claim_id]
            example.evidence_img_list.append(img_name)
         
    return example_dict



if __name__ == '__main__':

    read_example()