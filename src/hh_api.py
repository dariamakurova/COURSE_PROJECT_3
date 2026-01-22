
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

    def get_vacancies(self, employer: str):
        """Метод для получения вакансий с HH"""
        page = 0
        data = self.__connect(employer, page)
        pages_total = data.get("pages", 0)

        while page < pages_total:
            vacancies_json = data["items"]
            for vacancy in vacancies_json:
                if vacancy.get("salary") and vacancy.get("salary").get("currency") == "RUR":
                    self.__vacancies.append(self.simplify_vacancy(vacancy))
            page += 1
            if page < pages_total:
                data = self.__connect(employer, page)
        return self.__vacancies

    @classmethod
    def simplify_vacancy(cls, vacancy: dict):
        """Оставляет только рабочие параметры вакансии"""

        rur_currencies = {"RUR": "RUR", "RUB": "RUR", "РУБ": "RUR", "РУБ.": "RUR"}
        salary = vacancy.get("salary")
        salary_from = 0
        salary_to = 0
        salary_currency = None

        if salary:
            if isinstance(salary, dict):
                salary_from = salary["from"] if salary.get("from") else 0
                salary_to = salary["to"] if salary.get("to") else 0
                salary_currency = (
                    rur_currencies.get(salary["currency"].upper(), salary["currency"])
                    if salary.get("currency")
                    else None
                )

            elif isinstance(salary, str):

                salary_from = 0
                salary_to = 0
                salary_currency = None

                salary_details = salary.split("-")
                if len(salary_details) >= 1 and salary_details[0].strip().isdigit():
                    salary_from = int(salary_details[0])

                if len(salary_details) >= 2 and salary_details[1].split()[0].strip().isdigit():
                    salary_to = int(salary_details[1].split()[0].strip())

                    if len(salary_details[1].split()) >= 2:
                        currency = salary_details[1].split()[1].strip().upper()
                        salary_currency = rur_currencies.get(currency, currency)
        else:
            salary_from = 0
            salary_to = 0
            salary_currency = None

        return {
            "vac_id": vacancy.get("id"),
            "name": vacancy.get("name"),
            "employer_id": vacancy.get("employer", {}).get("id"),
            "url": vacancy.get("alternate_url"),
            "salary_from": salary_from,
            "salary_to": salary_to,
            "salary_currency": salary_currency,
            "requirement": vacancy.get("snippet", {}).get("requirement"),
        }

    @classmethod
    def validate_salary(cls, salary: dict):
        """Приводит зарплату к рабочему формату"""



