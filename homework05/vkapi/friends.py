import dataclasses
import math
import time
import typing as tp 

session = Session(VK_CONFIG["domain"])  # запуск сессии
# from session import session #config,
# from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    fields = ", ".join(fields) if fields else ""
    # user_id = 274205023  #номер страницы
    if not user_id:
        query = f"{domain}/friends.get?access_token={access_token}&fields={fields}&v={v}"
    else:
        query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = session.get(query)
    response_json = response.json()
    list_of_friends = response_json["response"]["items"]
    # обращаемся к объекту класса response
    return list_of_friends


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    # генерация запроса в зависимости от данных
    query = f"{domain}/friends.getMutual?access_token={access_token}"
    if source_uid:
        query += f"&source_uid={source_uid}"
    if not target_uids and not target_uid:
        raise "Error"
    list_of_mutualfriends = []
    if target_uids:
        count1 = len(target_uids)
        # query += f"&target_uids={','.join(list(map(str, target_uids)))}&v={v}"
        for offset1 in range(0, count1, 100):
            target_uids_str = ",".join(list(map(str, target_uids)))
            query += f"&target_uids={target_uids_str}&count={count1}&offset={offset1}&v={v}"
            count1 -= 100
            response = session.get(query)  # указывваем формат запроса это get запрос
            if response.status_code != 200:
                raise ValueError("Ошибка", response.status_code)
            response_json = response.json()
            if "error" in response_json:
                raise ValueError("Ошибка", response_json["error"])
            list_of_mutualfriends += response_json["response"]
    if (
        target_uid
    ):  # получаем список идентификаторов пользователей, с которыми мы хотим найти общих друзей если дан target_uids на вход
        query += f"&target_uid={target_uid}&v={v}"
        response = session.get(query)  # указывваем формат запроса это get запрос
        if response.status_code != 200:
            raise ValueError("Ошибка", response.status_code)
        response_json = response.json()
        if "error" in response_json:
            raise ValueError("Ошибка", response_json["error"])
        list_of_mutualfriends = response_json["response"]
    return list_of_mutualfriends


if __name__ == "__main__":
    # print(get_friends(274205023, count = 10,offset = 10,  fields= 'bdate'))
    print(get_mutual(274205023, 289180780))  # общие друзья
    print(get_mutual(274205023, target_uids=[133985865, 289180780, 145904017]))
    # print(get_friends(None, count=10, offset=10, fields='bdate'))
