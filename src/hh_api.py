
import requests

from src.vacancies_api import VacanciesAPI


class HeadHunterAPI(VacanciesAPI):
    """Класс для получения вакансий с платформы HeadHunter"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "only_with_salary": True, "employer_id": ""}
        self.__vacancies = []

    def __connect(self, employer_id: str, page: int):
        """Метод для подключения к сервису HH по API"""
        self.__params["employer_id"] = employer_id
        self.__params["page"] = page
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, keyword: str):
        """Метод для получения вакансий с HH"""
        page = 0
        data = self.__connect(keyword, page)
        pages_total = data.get("pages", 0)

        while page < pages_total:
            vacancies_json = data["items"]
            for vacancy in vacancies_json:
                if vacancy.get("salary") and vacancy.get("salary").get("currency") == "RUR":
                    self.__vacancies.append(self.simplify_vacancy(vacancy))
            page += 1
            if page < pages_total:
                data = self.__connect(keyword, page)
        return self.__vacancies

    @classmethod
    def simplify_vacancy(cls, vacancy: dict):
        """Оставляет только рабочие параметры вакансии"""

        return {
            "vac_id": vacancy.get("id"),
            "name": vacancy.get("name"),
            "employer": vacancy.get("employer", {}).get("name"),
            "employer_id": vacancy.get("employer", {}).get("id"),
            "url": vacancy.get("alternate_url"),
            "salary": vacancy.get("salary"),
            "requirement": vacancy.get("snippet", {}).get("requirement"),
        }
