from abc import ABC, abstractmethod
from typing import Dict, List


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса вакансий."""

    @abstractmethod
    def _connect(self) -> None:
        """Абстрактный метод для отправки запроса на базовый URL и проверки статус-кода."""
        pass

    @abstractmethod
    def get_employers(self) -> List[Dict]:
        """Абстрактный метод для получения списка работодателей."""
        pass

    @abstractmethod
    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """
        Абстрактный метод для получения списка вакансий по ID работодателя.

        :param employer_id: Идентификатор работодателя.
        :return: Список словарей с информацией о вакансиях.
        """
        pass
