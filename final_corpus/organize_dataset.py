import os
import pandas as pd
from statistic import get_claim_with_relevant_document_set
from utils.merge_snopes_politifact import increase_politifact_id, merge, merge_one_file
from utils.relevant_document_percent import get_claim_id_in_percentage_range
from utils.splitor import split_corpus2, split_corpus3_and_image
from utils.statistic_helper import gen_cleaned_truthfulness

def generate_id(data_path):
    out_path= data_path+"_temp"
    out_corpus=os.path.join(out_path,"LinkCorpus.csv")
    corpus=os.path.join(data_path,"LinkCorpus.csv")
    claim_id=-1
    evidence_id=-1
    cur_snopes_url=""
    claim_id_list = []
    relevant_document_id_list=[]
    df = pd.read_csv(corpus ,encoding="utf8")
    for i,row in df.iterrows():
        snopes_url=row["Snopes URL"]
        if cur_snopes_url!=snopes_url:
            claim_id+=1
            cur_snopes_url=snopes_url
        relevant_document_id_list.append(i)
        claim_id_list.append(claim_id)
    df.insert(0, "claim_id",claim_id_list )
    # df.insert(1, "evidence_id",evidence_id_list )
    # df["claim_id"]=claim_id_list
    # df["evidence_id"]=evidence_id_list
    df.to_csv(corpus,index_label="relevant_document_id")


def read_link_corpus(data_path):
    corpus=os.path.join(data_path,"LinkCorpus.csv")
    df = pd.read_csv(corpus ,encoding="utf8")
    return df


def generate_id_for_corpus2(data_path):
    out_path= data_path+"_temp"
    out_corpus=os.path.join(out_path,"Corpus2.csv")
    corpus=os.path.join(data_path,"Corpus2.csv")
    df_link=read_link_corpus(data_path)
    removed_num=0
    claim_id_list=[]
    df = pd.read_csv(corpus ,encoding="utf8")  
    for i,row in df.iterrows():
        snopes_url=row["Snopes URL"]
        found=df_link.loc[df_link['Snopes URL'] ==snopes_url]
        if len(found)>0:
            claim_id=found.head(1)["claim_id"].values[0]  
        else:
            print(f"can not find {snopes_url}")
            claim_id=-1
            removed_num+=1
        claim_id_list.append(claim_id)
    df.insert(0, "claim_id",claim_id_list )
    df.to_csv(corpus,index=False)
    print(removed_num)



    
    
# def generate_id_for_corpus3():
    
#     data_path ="final_corpus/mode1_old/"
#     out_path="final_corpus/mode1_old_temp/"
#     out_corpus=os.path.join(out_path,"Corpus3.csv")
#     corpus=os.path.join(data_path,"Corpus3.csv")
#     df_link=read_link_corpus(data_path)

#     claim_id_list=[]
#     relevant_document_id_list=[]
#     df = pd.read_csv(corpus ,encoding="utf8")  
#     for i,row in df.iterrows():
#         snopes_url=row["Snopes URL"]
#         found=df_link.loc[df_link['Snopes URL'] ==snopes_url]
#         if len(found)>0:
#             claim_id=found.head(1)["claim_id"].values[0]  
#             relevant_document_id=found.head(1)["evidence_id"].values[0]  
#         else:
#             claim_id=-1
#             relevant_document_id=-1
#         claim_id_list.append(claim_id)
#         relevant_document_id_list.append(relevant_document_id)
#     df.insert(1, "relevant_document_id",relevant_document_id_list )
#     df.insert(0, "claim_id",claim_id_list )
#     df.to_csv(out_corpus,index=False)




def generate_id_for_corpus3(data_path):
    out_path= data_path+"_temp"
    out_corpus=os.path.join(out_path,"Corpus3.csv")
    corpus=os.path.join(data_path,"Corpus3.csv")
    df_link=read_link_corpus(data_path)

    claim_id_list=[]
    relevant_document_id_list=[]
    df = pd.read_csv(corpus ,encoding="utf8")  
    for i,row in df.iterrows():
        relevant_document_url=row["Link URL"]
        found=df_link.loc[df_link['Original Link URL'] ==relevant_document_url]
        if len(found)>0:
            claim_id=found.head(1)["claim_id"].values[0]  
            relevant_document_id=found.head(1)["relevant_document_id"].values[0]  
        else:
            print(f"can not find {relevant_document_url}")
            claim_id=-1
            relevant_document_id=-1
        claim_id_list.append(claim_id)
        relevant_document_id_list.append(relevant_document_id)
    df.insert(0, "relevant_document_id",relevant_document_id_list )
    df.insert(0, "claim_id",claim_id_list )
    df.to_csv(corpus,index=False)

def generate_cleaned_truthfulness(data_path): 
    corpus=os.path.join(data_path,"Corpus2.csv")
    out_path= data_path+"_temp"
    out_corpus=os.path.join(out_path,"Corpus2.csv")
   
    cleaned_truthfulness_list=[]
    df = pd.read_csv(corpus ,encoding="utf8")  
    for i,row in df.iterrows():
        truthfulness=row["Truthfulness"]
        cleaned_truthfulness=gen_cleaned_truthfulness(truthfulness)
        cleaned_truthfulness_list.append(cleaned_truthfulness)
    df.insert(11, "cleaned_truthfulness",cleaned_truthfulness_list )
    df.to_csv(corpus,index=False)
    #test


def fix_cleaned_truthfulness(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    df=df.drop(columns=['cleaned_truthfulness' ])
    df.to_csv(corpus,index=False)
    
    generate_cleaned_truthfulness(data_path)
    
def get_ruling_outline(ruling_article):
    ruling_outline=""
    if not pd.isna(ruling_article):
        position=ruling_article.lower().find("In sum".lower())
        if  position>0:
            ruling_outline=ruling_article[position:]
        else:
            position=ruling_article.find("Conclusion" )
            if  position>0:
                ruling_outline=ruling_article[position:]
            else:
                position=ruling_article.lower().find("In conclusion".lower())
                if  position>0:
                    ruling_outline=ruling_article[position:]
                else:
                    position=ruling_article.lower().find("In short".lower())
                    if  position>0:
                        ruling_outline=ruling_article[position:]
                    elif len(ruling_article)<1000:
                        ruling_outline=ruling_article
    return ruling_outline
    
def generate_ruling_outline_for_snopes(data_path):    
    if "politifact" not in data_path:
        corpus=os.path.join(data_path,"Corpus2.csv")
        df = pd.read_csv(corpus ,encoding="utf8")  
        df=df.drop(columns=['ruling_outline' ])
        ruling_outline_list=[]
        for i,row in df.iterrows():
            ruling_article=row["Origin"]
            # if row["Snopes URL"] in ["https://www.snopes.com/fact-check/ticketmaster-class-action-free-ticket-giveaway/"]:
            #     print(len(ruling_article))
            ruling_outline=get_ruling_outline(ruling_article)
            # if len(ruling_outline)==0:
            #     print(row["Snopes URL"])
            ruling_outline_list.append(ruling_outline)
        df.insert(15, "ruling_outline",ruling_outline_list )
        df.to_csv(corpus,index=False)
        
def generate_fact_checkor_website(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")
    if "politifact" not in data_path:
        df['fact_checkor_website']="snopes"
    else:
        df['fact_checkor_website']="politifact"
   
    df.to_csv(corpus,index=False)

def generate(data_path):
    generate_id(data_path)
    generate_id_for_corpus2(data_path) 
    generate_id_for_corpus3(data_path) 
    generate_cleaned_truthfulness(data_path) 
    
def clean_by_label(data_path):
 
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    df.drop(df[df['cleaned_truthfulness'] =="other"].index, inplace = True)
    df.to_csv(corpus,index=False)

def clean_row_with_na(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    df=df.dropna(subset=['Evidence']) #'ruling_outline', 'Origin'
    indexes = df[ (df['ruling_outline'].isna()) & (df['Origin'].isna()) ].index
    #droping mutiple rows based on column value
    df.drop(indexes,inplace=True)

    df=df.reset_index(drop=True)
    df.to_csv(corpus,index=False)

def clean_claim_id_equal_minus_1(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    df.drop(df[df['claim_id'] ==-1].index, inplace = True)
    df=df.reset_index(drop=True)
    df.to_csv(corpus,index=False)


def clean_corpus3(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df2 = pd.read_csv(corpus ,encoding="utf8")  
    remaining_claim_id_set=set(df2["claim_id"].tolist() )
    
    temp_path= data_path+"_temp"
    temp_corpus3=os.path.join(temp_path,"Corpus3.csv")
    corpus3=os.path.join(data_path,"Corpus3.csv")
    df3 = pd.read_csv(corpus3 ,encoding="utf8")  
    df3.to_csv(temp_corpus3,index=False)
    df3.drop(df3[~df3['claim_id'].isin(list(remaining_claim_id_set))].index, inplace = True)
    df3=df3.reset_index(drop=True)
    df3.to_csv(corpus3,index=False)


def clean_images(data_path):
    corpus=os.path.join(data_path,"Corpus2.csv")
    df2 = pd.read_csv(corpus ,encoding="utf8")  
    remaining_claim_id_list=list(set(df2["claim_id"].tolist() ))
    
    image_corpus=os.path.join(data_path ,"images") 
    backup_img_path=os.path.join(data_path+"_backup","images") 
    img_names=os.listdir(image_corpus)
    removed_pic_num=0
  
    for filepath in  img_names:
        source_path=os.path.join(image_corpus,filepath)
        prefix=filepath[:14]
        ids=prefix.split("-")
        claim_id_in_image= int(ids[0])  
     
        if claim_id_in_image not in remaining_claim_id_list:
            removed_pic_num+=1
            os.rename(source_path,os.path.join(backup_img_path,filepath) )
    s=f"{removed_pic_num}"
    print(s)
    

def clean_row_without_relevant_document(data_path):    
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    claim_with_relevant_document_set=get_claim_with_relevant_document_set(data_path)
    df.drop(df[~df['claim_id'].isin(list(claim_with_relevant_document_set))].index, inplace = True)
    df=df.reset_index(drop=True)
    df.to_csv(corpus,index=False)
    
    
def clean_row_with_few_relevant_document(data_path):
    _,_,claim_ids_below_20=get_claim_id_in_percentage_range(data_path)
    corpus=os.path.join(data_path,"Corpus2.csv")
    df = pd.read_csv(corpus ,encoding="utf8")  
    df.drop(df[df['claim_id'].isin(list(claim_ids_below_20))].index, inplace = True)
    df=df.reset_index(drop=True)
    df.to_csv(corpus,index=False)
    
def clean_corpus3_na(data_path):
    corpus3=os.path.join(data_path,"Corpus3.csv")
    df3 = pd.read_csv(corpus3 ,encoding="utf8")  
    df3=df3.dropna(subset=['Origin Document'])
    df3=df3.reset_index(drop=True)
    df3.to_csv(corpus3,index=False)

def clean(data_path):
    clean_by_label(data_path)
    clean_row_with_na(data_path)
    clean_row_without_relevant_document(data_path)
    clean_row_with_few_relevant_document(data_path)
    clean_claim_id_equal_minus_1(data_path)
    clean_corpus3(data_path)
    clean_images(data_path)
    
    
    
    
    
import argparse
def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path',type=str,help=" ",default="mocheg") #politifact_v3,mode3_latest_v5
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parser_args()
      #"mode3_latest_v5"
    # generate(data_path)
    # clean(data_path)
    split_corpus3_and_image(args.data_path)
    # merge("mode3_latest_v5","politifact_v3","mocheg")
    # merge_one_file("mode3_latest_v5","politifact_v3","mocheg","Corpus2.csv"   )
    
    # generate_fact_checkor_website(args.data_path)
    # generate_id( args.data_path)
    
    
    
   
     