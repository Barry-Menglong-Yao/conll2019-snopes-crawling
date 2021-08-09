from newspaper import Article
import pandas as pd
def print_img_url(url):
        
    
    article = Article(url)
    article.download()
    # print(article.html)
    article.parse()
     

    # print(article.authors)


    # print(article.publish_date)


    # print(article.text)


    # print(article.top_image)

    filtered_imgs=[]
    for img_url in article.images:
        if ".svg" not in img_url:
            filtered_imgs.append(img_url)

    print(filtered_imgs)


def test2():
    urls = pd.read_csv( "util/tried_image_crawler/test_url.csv",encoding="utf8")
    for _,row in urls.iterrows():
        print_img_url(row["url"])



test2()