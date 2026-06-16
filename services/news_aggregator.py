def get_all_news():

    from data.news.us_news import get_us_news
    from data.news.hk_news import get_hk_news
    from data.news.mainland_news import get_mainland_news

    news = {
        "us": get_us_news(),
        "hk": get_hk_news(),
        "mainland": get_mainland_news()
    }

    return news