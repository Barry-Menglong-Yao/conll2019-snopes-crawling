import trafilatura
downloaded = trafilatura.fetch_url('https://www.gettyimages.com/detail/news-photo/paris-hilton-wearing-chick-by-nicky-hilton-during-nicky-news-photo/121066647')
print(trafilatura.bare_extraction(downloaded,include_images=True ))