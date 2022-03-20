import datetime as dt
import statistics
import typing as tp

from homework05.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    list_of_friends = get_friends(user_id, fields="bdate")
    age = []
    date_today = dt.date.today()
    for friend in list_of_friends:
        try:
            b_date_str = friend["bdate"]
            b_date = dt.datetime.strptime(
                b_date_str, "%d.%m.%Y"
            ).date()  # дата рождения только дата в формате даты, без времени
            age_of_fr = date_today - b_date
            age.append(age_of_fr.days // 365)  # добавляем возраст друзей в список
        except:
            continue  # если нет возраста в вк
    age = sorted(age)
    return age[len(age) // 2]  # возвращает медианный возраст


# age_predict(274205023)
