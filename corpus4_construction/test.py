from newspaper import Article

def test1():
        
    url = 'https://www.instagram.com/p/CH8je5ght9b/?utm_source=ig_embed&ig_rid=1a8c2d2c-867d-4c0a-a744-695e4b33d480'
    article = Article(url)
    article.download()
    # print(article.html)
 
    print(article.parse())

    print(article.authors)


    print(article.publish_date)


    print(article.text)


    print(article.top_image)

    print(article.images)

    print(article.movies)


def test2():
    pass 



test1()