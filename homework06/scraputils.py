import requests
from bs4 import BeautifulSoup


def extract_news(parser1: BeautifulSoup):
    """ Extract news from a given web page """
    news_list = [] #для title
    title_list = []
    url_list = []
    comments_list = []
    point_list =[]
    author_list = []
    #title url comments  points author

    subtext_line = parser1.select(".subtext")

    # сбор для title_list
    all_things = parser1.find_all("tr", {"class": "athing"})
    for a_thing in all_things:
        find_athing = a_thing.find_all("td", {"class": "title"})
        title_list.append(find_athing[1].a.text)
        url_list.append(find_athing[1].a["href"])

    print(url_list)
    for index in range(len(subtext_line)):
        points = subtext_line[index].select(".score")
        if points == []:
            points = 0
        else:
            points = int(points[0].text.split()[0])
        point_list.append(points)

        author = subtext_line[index].select(".hnuser")
        if author == []:
            author = "Anonymous"
        else:
            author = author[0].text
        author_list.append(author)

        comments = subtext_line[index].find_all("a")[4].text
        if comments == "discuss":
            comments_list.append(0)
        else:
            comments_list.append(int(comments.split()[0]))
    print(comments_list)
    ###TODO: запись в news_list


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