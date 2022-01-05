
import os
import pandas as pd


def extract_perfect(data_path):
    evidence_corpus="Corpus2.csv"
    out_path= data_path+"_perfect"
    out_corpus=os.path.join(out_path,"Corpus2.csv")
    df_evidence = pd.read_csv(os.path.join(data_path,evidence_corpus) ,encoding="utf8")
    cur_snope_url=-2
    claim_dict={}
    count=0
    
    print(df_evidence.isnull().sum())
    df=df_evidence.dropna(subset=['ruling_outline', 'Evidence'])
    df=df.reset_index(drop=True)
    df.to_csv(out_corpus,index=False)
    print(f"perfect instance: {len(df)}")
    
    # cp politifact_v1/LinkCorpus.csv politifact_v1_perfect/

if __name__ == '__main__':
   
    data_path ="politifact_v1"
 
    extract_perfect(data_path)
     