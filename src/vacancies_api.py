from abc import ABC, abstractmethod


class VacanciesAPI(ABC):
    """Абстрактный класс для получения вакансий по API"""

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        """Загрузка вакансий с платформы"""
        pass
