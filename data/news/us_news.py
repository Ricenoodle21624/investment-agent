import feedparser

def get_us_news():

    feeds = [
        "https://www.reuters.com/markets/us/rss",
        "https://www.reuters.com/technology/rss",
    ]

    news_list = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "time": entry.published if hasattr(entry, "published") else "",
                "source": "Reuters"
            })

    return news_list