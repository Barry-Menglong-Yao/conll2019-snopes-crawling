import os 
from PIL import Image
import cv2
import os
import click
import numpy as np
from sentence_transformers import SentenceTransformer, util
def remove_img():
    data_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest"
    image_corpus=os.path.join(data_path,"images")
    img_names=os.listdir(image_corpus)
    
    for img_name in  img_names:
        prefix=img_name[:13]
        ids=prefix.split("-")
        claim_id= int(ids[0]) #+1 #TODO diff by 1
        relevant_document_id=int(ids[1])#+1
        if claim_id>=597:
            os.remove(os.path.join(image_corpus,img_name))

def check_img1() :
    data_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest"
    temp_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest_temp"
    image_corpus=os.path.join(data_path,"images")
    img_names=os.listdir(image_corpus)
    
    for filepath in  img_names:
        
        source_path=os.path.join(image_corpus,filepath)
        im = Image.open(source_path)
        if im is None or len(im.getbands())==4:
            print(f"{len(im.getbands())}, {source_path}")
            os.rename(source_path,os.path.join(temp_path,filepath) )
    

def check_by_clip(data_path,backup_img_path):
    model = SentenceTransformer('clip-ViT-B-32')
    
     
    image_corpus=os.path.join(data_path,"images")
    img_names=os.listdir(image_corpus)
    error_pic_num=0
 
    with open(data_path+"/log.txt","a") as f:
        for filepath in  img_names:
            source_path=os.path.join(image_corpus,filepath)
            print(source_path)
            try:
                model.encode([Image.open(source_path)  ], batch_size=1, convert_to_tensor=True, show_progress_bar=True)
            except Exception as e:
                print(f"clip error: {source_path} ,{e}",file=f)
                print(f"clip error: {source_path} ,{e}" )
                error_pic_num+=1
                os.rename(source_path,os.path.join(backup_img_path,filepath) )
        s=f"{error_pic_num}"
        print(s)
        print(s,file=f)

def check_by_pil(data_path,backup_img_path) :
  
    temp_img_path=backup_img_path
    image_corpus=os.path.join(data_path,"images")
    img_names=os.listdir(image_corpus)
    thresholdWidth=512
    thresholdHeight=512
    good_num,small_pic_num,not_3_num=0,0,0
    p_mode_num,l_mode_num,la_mode_num=0,0,0
    mode_list=set()
    with open("log.txt","a") as f:
        for filepath in  img_names:
            

            source_path=os.path.join(image_corpus,filepath)
            im = Image.open(source_path)
            mode_list.add(im.mode)
            width, height = im.size
            if (width < thresholdWidth or
                    height <  thresholdHeight):
                s=f"small pic: {width}, {height}, {source_path}"
                print(s,file=f)
                print(s)
                small_pic_num+=1
                os.rename(source_path,os.path.join(temp_img_path,filepath) )
            
            elif im is None or len(im.getbands())==4:
                x2 = np.array(im)
                s=f"not 3: {len(im.getbands())}, {source_path} ,{x2[3]}"
                print(s,file=f)
                print(s)
                not_3_num+=1
                os.rename(source_path,os.path.join(temp_img_path,filepath) )
            elif im.mode=="P":
                s=f"P mode: {im.mode},{width}, {height}, {source_path}  "
                print(s,file=f)
                print(s)
                p_mode_num+=1
                os.rename(source_path,os.path.join(temp_img_path,filepath) )
            elif im.mode=="L":
                s=f"L mode: {im.mode},{width}, {height}, {source_path}  "
                print(s,file=f)
                print(s)
                l_mode_num+=1
                os.rename(source_path,os.path.join(temp_img_path,filepath) )
            elif im.mode=="LA":
                s=f"LA mode: {im.mode},{width}, {height}, {source_path}  "
                print(s,file=f)
                print(s)
                la_mode_num+=1
                os.rename(source_path,os.path.join(temp_img_path,filepath) )
            else:
                s=f"good:   {width}, {height}, {source_path} "
                print(s,file=f)
                print(s)
                good_num+=1
        s=f"{good_num},small_pic_num {small_pic_num},not_3_num { not_3_num},p_mode_num:{p_mode_num},l_mode_num:{l_mode_num},la_mode_num:{la_mode_num},mode_list:{mode_list}"
        print(s,file=f)
        print(s)
        
                # os.rename(source_path,os.path.join(temp_path,filepath) )
    


def check_img3(data_path,backup_img_path) :
    
    image_corpus=os.path.join(data_path,"images")
    img_names=[ "565-3792-0-image.jpg"]
    img_list=[]
    for filepath in  img_names:
        
        source_path=os.path.join(image_corpus,filepath)
        os.rename(source_path,os.path.join(backup_img_path,filepath) )
        # im = Image.open(source_path)
        # img_list.append(im)
    print("")

def check_img():
    data_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest"
    image_corpus=os.path.join(data_path,"images")
    img_names=os.listdir(image_corpus)
    
    for filepath in  img_names:
        

        im = cv2.imread(os.path.join(image_corpus,filepath))
        
        if im is None :
            print(filepath)
            
            os.remove(os.path.join(image_corpus,filepath))
        elif im.shape[2]!=3 :
            print(f"{im.shape},  {filepath}")
   
            os.remove(os.path.join(image_corpus,filepath))

@click.command()
@click.pass_context
@click.option('--data_path', help='input', required=True, metavar='DIR',default="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/politifact_v1")
@click.option('--backup_img_path', help='input', required=True, metavar='DIR',default="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/politifact_v1_backup/images")
def test(ctx,   **config_kwargs):
    # data_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest_v2"
    # backup_img_path="/home/menglong/workspace/code/referred/conll2019-snopes-crawling/final_corpus/mode3_latest_v2_backup/images"
    data_path=config_kwargs["data_path"]
    backup_img_path=config_kwargs["backup_img_path"] #mode1_old_v2_backup
    # check_by_pil(data_path,backup_img_path) 
    check_by_clip(data_path,backup_img_path) 
   

if __name__ == "__main__":
    
     
    test()