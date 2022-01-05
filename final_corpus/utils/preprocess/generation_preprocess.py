
import os
import pandas as pd


def merge_evidence(data_path):
    data = []
    corpus=os.path.join(data_path,"Corpus2.csv")
    out_corpus=os.path.join(data_path,"Corpus2_for_generation.csv")
    evidence_list=[]
    evidence_df = pd.read_csv(corpus ,encoding="utf8")  
    evidence_merged_df = evidence_df.drop_duplicates(subset='claim_id', keep="first")
    evidence_merged_df =evidence_merged_df.drop(columns=[ 'Evidence'])
    evidence_merged_df=evidence_merged_df.reset_index(drop=True)
    for i,row in evidence_merged_df.iterrows():
        claim_id=row["claim_id"]
        found=evidence_df.loc[evidence_df['claim_id'] ==claim_id]
        evidence=append_str(found["Evidence"].values)
        evidence=evidence.replace("<p>","")
        evidence=evidence.replace("</p>","")
        evidence_list.append(evidence)
        # print(evidence)
    evidence_merged_df.insert(13, "Evidence",evidence_list )
    evidence_merged_df.to_csv(out_corpus,index=False)
    
def append_str(evidence_array):
    evidence=""
    for i in range(len(evidence_array)):
        evidence+=str(evidence_array[i])+" "
    return evidence

def merge_evidence_truthfulness(data_path):
 
    corpus=os.path.join(data_path,"Corpus2_for_generation.csv")
    out_corpus=os.path.join(data_path,"Corpus2_for_controlled_generation2.csv")
    evidence_list=[]
    evidence_df = pd.read_csv(corpus ,encoding="utf8")  
      
    for i,row in evidence_df.iterrows():
        claim_id=row["claim_id"]
        truthfulness=row["Truthfulness"]
        claim=row["Claim"]
        evidence=row["Evidence"]
        truth_claim_evidence=truthfulness+" </s> "+claim+" </s> "+evidence
        evidence_list.append(truth_claim_evidence)
        # print(evidence)
    evidence_df.insert(14, "truth_claim_evidence",evidence_list )
    evidence_df.to_csv(out_corpus,index=False)

if __name__ == '__main__':
   
    data_path ="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/politifact_v1_perfect"
 
    # merge_evidence(data_path)
    merge_evidence_truthfulness(data_path)
     