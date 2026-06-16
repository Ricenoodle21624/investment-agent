import requests
from bs4 import BeautifulSoup

def get_hk_news():

    url = "https://www.hkex.com.hk/News"
    r = requests.get(url, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    for a in soup.find_all("a")[:10]:
        title = a.text.strip()
        if len(title) > 5:
            items.append({
                "title": title,
                "source": "HKEX"
            })

    return items