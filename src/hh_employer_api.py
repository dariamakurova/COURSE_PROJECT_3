
import requests

from src.employer_api import EmployerAPI


class HeadHunterEmployerAPI(EmployerAPI):
    """Класс для получения информации о работодателе с платформы HeadHunter"""

    def __init__(self):
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}

    def __connect(self, employer_id: str):
        """Метод для подключения к сервису HH по API"""

        company_url = self.__url + f"/{employer_id}"
        response = requests.get(url=company_url, headers=self.__headers)
        response.raise_for_status()
        return response.json()

    def get_employer_info(self, employer_id: str):
        """Метод для получения информации о работодателе с HH"""

        data = self.__connect(employer_id)
        return {
            "employer_id" : data.get("id"),
            "employer_name" : data.get("name")
        }