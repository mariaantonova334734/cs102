import time
import typing as tp
import homework05.vkapi.config as config
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """
    base_url: str
    timeout: float
    max_retries: int
    backoff_factor: float
    http: Retry
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url #передается аргумент base_url в параметр класса  self.base_url
        self.timeout = timeout
        self.session = requests.Session()
        errors = []
        for i in range(400, 600):
            errors.append(i)

        retry = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=errors,
            method_whitelist=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        response = self.session.get(
            self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs
        )

        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        response = self.session.post(
            self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs
        )
        return response

    #     self.http = requests.Session()
    #     self.http.mount("https://", adapter)
    #     self.http.mount("http://", adapter)
    #
    # def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
    #     response = self.http.get(url, timeout=self.timeout)
    #     response.raise_for_status()
    #     return response
    # def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
    #     response = self.http.post(url, timeout=self.timeout)
    #     response.raise_for_status()
    #     return response

if __name__ == "__main__":
    session = Session("https://en.wikipedia.org")
    session.get("w/api.php")