import os
from PIL import Image

def test1():
    out_dir="out/running/run8/images"
    imgs=next(os.walk(out_dir))[2]
    for img in imgs:
        try:
            image=Image.open(os.getcwd()+"/"+out_dir+"/"+img)
            width, height = image.size
            print(f'{img} size:{width} {height}')
        except:
            print()



test1()