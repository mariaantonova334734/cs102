import requests
from bs4 import BeautifulSoup


def extract_news(parser1: BeautifulSoup):
    """ Extract news from a given web page """
    news_list = []

    #print(parser.head.title.text)
    all_things = parser1.find_all("tr", {"class": "athing"})

    #find_ch = parser1.findChildren()
    for a_thing in all_things:
        find_athing = a_thing.find_all("td", {"class": "title"})

        news_list.append(find_athing[1].a.text)

    return news_list


def extract_next_page(parser1: BeautifulSoup):
    """ Extract next page URL """
    link = parser1.select(".morelink")[0]["href"]
    #print(str(link))
    return str(link)


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__=="__main__":
    print(get_news("https://news.ycombinator.com/newest", n_pages=3)) #выдает заголовки на 3-х страницах