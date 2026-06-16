import feedparser

def get_mainland_news():

    feeds = [
        "https://www.cs.com.cn/rss/ss/rss_1.xml",  # 上证报
    ]

    news_list = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "source": "Mainland Media"
            })

    return news_list