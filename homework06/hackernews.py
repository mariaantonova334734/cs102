import string

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    get_zapros = request.query.decode()
    id = int(get_zapros["id"])
    label = get_zapros["label"]
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    s = session()
    news = s.query(News).filter(News.id == id)
    # 3. Изменить значение метки записи на значение label
    news.update({News.label: label})
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # сначала получаем список новостей
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=5)
    # подключаемся к базе данных и записываем в нее
    s = session()  # session из db
    for novost in news_list:
        news = News(
            title=novost[0], author=novost[1], url=novost[2], comments=novost[3], points=novost[4]
        )
        # проверяем, нет ли такой новости в базе данных
        samenews = (
            s.query(News).filter(News.title == news.title).filter(News.author == news.author).all()
        )
        if samenews == []:
            s.add(news)
    s.commit()
    # переводим на страницу с новостями
    redirect("/news")


colors = {"good": "#00ff6a", "never": "#d10000", "maybe": "#ffb700"}


@route("/classify")
def classify_news():
    s = session()
    model = NaiveBayesClassifier()
    set_of_news = (
        s.query(News).filter(News.label != None).all()
    )  # сет новостей, ни которые была реакция
    model.fit(
        [clean(news.title).lower() for news in set_of_news],
        [news.label for news in set_of_news],
    )  # моделирование прогнозов
    set_no_reaction = (
        s.query(News).filter(News.label == None).all()
    )  # сет новостей, ни которые не было реакции
    # сортировка в зависимости от предсказанной реакции
    return template(
        "news_template",
        rows=sorted(
            set_no_reaction,
            key=lambda news: type_of_label(
                model.predict(clean(news.title).lower())
            ),  # получение прогнозов
        ),
    )


def type_of_label(label: str):
    if label == "never":
        return 2
    elif label == "maybe":
        return 1
    elif label == "good":
        return 0
    else:
        raise AssertionError


def clean(s: str) -> str:  # все сообщения к нижнему регистру и избавимся от символов пунктуации:
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    run(host="localhost", port=8080)
