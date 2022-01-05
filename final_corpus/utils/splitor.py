
import os
import pandas as pd


def split(data_path):
    evidence__for_generation_corpus="Corpus2_for_controlled_generation2.csv"
    out_path= data_path+""
    out_train_corpus=os.path.join(out_path,"train_Corpus2_for_controlled_generation2.csv")
    out_val_corpus=os.path.join(out_path,"val_Corpus2_for_controlled_generation2.csv")
    df_evidence = pd.read_csv(os.path.join(data_path,evidence__for_generation_corpus) ,encoding="utf8")
    from sklearn.model_selection import train_test_split

    train_df, val_df = train_test_split(df_evidence, test_size=0.15)
    
    
    train_df=train_df.reset_index(drop=True)
    val_df=val_df.reset_index(drop=True)
    train_df.to_csv(out_train_corpus,index=False)
    val_df.to_csv(out_val_corpus,index=False)
    print(f" instance: {len(train_df)}")
    print(f" instance: {len(val_df)}")
    
    # cp politifact_v1/LinkCorpus.csv politifact_v1_perfect/

if __name__ == '__main__':
   
    data_path ="politifact_v1_perfect"
 
    split(data_path)
     