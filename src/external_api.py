from typing import Dict, List

import requests
from tqdm import tqdm

from src.base import VacancyAPI
from src.logger_config import add_logger

# Настройка логирования
logger = add_logger("e_api.log", "e_api")


class HeadHunterAPI(VacancyAPI):
    """Класс для взаимодействия с API HeadHunter."""

    def __init__(self) -> None:
        """Инициализация базового URL и заголовков для запросов."""
        logger.info("Создан объект класса 'HeadHunterAPI'.")
        self.__base_url = "https://api.hh.ru"
        self.__headers = {"User-Agent": "db-vacancy-manager"}

    def _connect(self) -> None:
        """Проверка доступности API по базовому URL."""
        logger.info("Запущена проверка доступности API.")
        try:
            response = requests.get(f"{self.__base_url}/employers", headers=self.__headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Ошибка подключения к API: {e}.", exc_info=True)
            raise

    def get_employers(self) -> List[Dict]:
        """
        Метод для получения информации о работодателях по заданным названиям.

        :return: Список словарей с краткой информацией.
        """
        logger.info("Запущен метод для получения информации о работодателях.")
        try:
            self._connect()
        except requests.exceptions.RequestException:
            logger.error("Прекращена работа метода get_employers из-за ошибки подключения.")
            return []

        employer_names = [
            "Сбер для экспертов",
            "Яндекс",
            "VK",
            "Ozon",
            "Ланит",
            "Лаборатория Касперского",
            "МедРокет",
            "X5 Tech",
            "Тензор",
            "Альфа-Банк",
        ]
        employers = []

        for name in tqdm(employer_names, desc="Получение данных о работодателях", colour="#19ff19"):
            logger.info(f"Отправка запроса на получение данных о работодателе '{name}'.")
            params = {"text": name, "only_with_vacancies": "true", "per_page": 1}
            try:
                response = requests.get(f"{self.__base_url}/employers", headers=self.__headers, params=params)
                response.raise_for_status()
                items = response.json().get("items", [])
                if not items:
                    logger.warning(f"Работодатель '{name}' не найден.")
                    continue
                employers.append(items[0])
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка запроса по работодателю '{name}': {e}", exc_info=True)
                continue

        logger.info(f"Количество работодателей о которых получена информация: {len(employers)}.")
        return employers

    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """
        Метод для получения всех вакансий по ID работодателя.

        :param employer_id: Идентификатор работодателя
        :return: Список словарей с вакансиями
        """
        logger.info(f"Запущен метод для получения вакансий работодателя '{employer_id}'.")
        vacancies = []
        params = {"employer_id": employer_id, "page": 0, "per_page": 100}

        while params["page"] < 20:
            try:
                response = requests.get(f"{self.__base_url}/vacancies", headers=self.__headers, params=params)
                response.raise_for_status()
                items = response.json().get("items", [])
                if not items:
                    break
                vacancies.extend(items)
                params["page"] += 1
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка при получении вакансий (стр. {params['page']}): {e}", exc_info=True)
                break

        logger.info(f"Количество полученных вакансий работодателя '{employer_id}': {len(vacancies)}.")
        return vacancies
