
import os
import pandas as pd

from statistic import count_claim_without_relevant_document, get_claim_with_relevant_document_set
from sklearn.model_selection import train_test_split
def split_corpus_by_completeness(df,data_path):
    # claim_with_relevant_document_set=get_claim_with_relevant_document_set(data_path)
     
    without_evidence_idx=df[df['Evidence'].isna()].index  
    df_without_evidence=df.iloc[without_evidence_idx]
    df_with_evidence=df.drop(without_evidence_idx)  
    
    without_ruling_outline_idx=df_with_evidence[df_with_evidence['ruling_outline'].isna()].index 
    df_without_ruling_outline=df_with_evidence.iloc[without_ruling_outline_idx]
    df_with_ruling_outline=df_with_evidence.drop(without_ruling_outline_idx)
    
    # without_relevant_document_idx=df_with_ruling_outline[~df_with_ruling_outline['claim_id'].isin(list(claim_with_relevant_document_set))].index
    # df_without_relevant_document=df_with_ruling_outline[without_relevant_document_idx]
    # df_with_relevant_document=df_with_ruling_outline.drop(without_relevant_document_idx)
    
    return df_without_evidence,df_without_ruling_outline,df_with_ruling_outline
   
def merge_df(df1,df2):
    frames=[df1,df2]
    df= pd.concat(frames)
    return df
    
    
def split_df_without_ruling_outline_by_claim_id(df_without_ruling_outline):    
    claim_id_list=list(set(df_without_ruling_outline["claim_id"].to_list()))
    claim_id_train_val, claim_id_test = train_test_split(claim_id_list, test_size=0.1102)
    claim_id_train, claim_id_val = train_test_split(claim_id_train_val, test_size=0.267)
    df_train=df_without_ruling_outline[df_without_ruling_outline['claim_id'].isin(claim_id_train)]
    df_test =df_without_ruling_outline[df_without_ruling_outline['claim_id'].isin(claim_id_test)] 
    df_val =df_without_ruling_outline[df_without_ruling_outline['claim_id'].isin(claim_id_val)] 
    
    return df_train,df_val,df_test

def split_corpus2(data_path):
    train_path=os.path.join(data_path,"train")
    val_path=os.path.join(data_path,"val")
    test_path=os.path.join(data_path,"test")
    train_corpus=os.path.join(train_path,"Corpus2.csv")
    val_corpus=os.path.join(val_path,"Corpus2.csv")
    test_corpus=os.path.join(test_path,"Corpus2.csv")
    
    df = pd.read_csv(os.path.join(data_path,"Corpus2.csv") ,encoding="utf8")
    df_without_evidence,df_without_ruling_outline,df_with_ruling_outline=split_corpus_by_completeness(df,data_path)
    df_without_ruling_outline_train,df_without_ruling_outline_val,df_without_ruling_outline_test=split_df_without_ruling_outline_by_claim_id(df_without_ruling_outline)
    df_train=merge_df(df_without_evidence,df_without_ruling_outline_train)
    df_val= df_without_ruling_outline_val
    df_test=merge_df(df_without_ruling_outline_test,df_with_ruling_outline)
    
    train_df=df_train.reset_index(drop=True)
    val_df=df_val.reset_index(drop=True)
    test_df=df_test.reset_index(drop=True)
    train_df.to_csv(train_corpus,index=False)
    val_df.to_csv(val_corpus,index=False)
    test_df.to_csv(test_corpus,index=False)
    
def split_corpus3_for_one_split(data_path,splited_data_path,claim_id_list):
    whole_df = pd.read_csv(os.path.join(data_path,"Corpus3.csv") ,encoding="utf8")    
    splited_df=whole_df[whole_df['claim_id'].isin(claim_id_list)]
    splited_df=splited_df.reset_index(drop=True)
    splited_df.to_csv(os.path.join(splited_data_path,"Corpus3.csv"),index=False)
    print("finish split_corpus3_for_one_split")
    
def split_image_for_one_split(data_path,splited_data_path,claim_id_list)    :
    image_corpus=os.path.join(data_path ,"images") 
    img_names=os.listdir(image_corpus)
    for filepath in  img_names:
        prefix=filepath[:14]
        ids=prefix.split("-")
        claim_id_in_image= int(ids[0])  
        if claim_id_in_image in claim_id_list:
            
            source_path=os.path.join(image_corpus,filepath)
            target_path=os.path.join(os.path.join(splited_data_path ,"images") ,filepath)
            os.rename(source_path,target_path )
    print("finish split_image_for_one_split")
    
def split_corpus3_and_image_for_one_split(data_path,splited_data_path):
    df = pd.read_csv(os.path.join(splited_data_path,"Corpus2.csv") ,encoding="utf8")
    claim_id_list= list(set(df["claim_id"].to_list()))
    split_corpus3_for_one_split(data_path,splited_data_path,claim_id_list)
    split_image_for_one_split(data_path,splited_data_path,claim_id_list)

def split_corpus3_and_image(data_path):
    split_corpus3_and_image_for_one_split(data_path,os.path.join(data_path,"train"))
    split_corpus3_and_image_for_one_split(data_path,os.path.join(data_path,"val"))
    split_corpus3_and_image_for_one_split(data_path,os.path.join(data_path,"test"))


def split_politifact(data_path):
    evidence__for_generation_corpus="Corpus2_for_controlled_generation2.csv"
    out_path= data_path+""
    out_train_corpus=os.path.join(out_path,"train_Corpus2_for_controlled_generation2.csv")
    out_val_corpus=os.path.join(out_path,"val_Corpus2_for_controlled_generation2.csv")
    df_evidence = pd.read_csv(os.path.join(data_path,evidence__for_generation_corpus) ,encoding="utf8")
    

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
 
    split_politifact(data_path)
     