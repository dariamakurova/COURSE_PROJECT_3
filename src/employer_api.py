from abc import ABC, abstractmethod


class EmployerAPI(ABC):
    """Абстрактный класс для получения информации о работодателе по API"""

    @abstractmethod
    def get_employer_info(self, *args, **kwargs):
        """Загрузка информации о работодателе с платформы"""
        pass
