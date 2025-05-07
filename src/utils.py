from typing import Dict, List

from tqdm import tqdm

from src.logger_config import add_logger
from src.models import Employer, Vacancy

# Настройка логирования
logger = add_logger("utils.log", "utils")


def parse_employers(employers_data: List[Dict]) -> List[Employer]:
    """
    Функция для парсинга данных работодателей из API HeadHunter и преобразует их в список объектов Employer.

    :param employers_data: Список словарей с данными работодателей из API.
    :return: Список объектов работодателей.
    """
    logger.info(f"Вызов функции 'parse_employers'. Количество полученных работодателей: {len(employers_data)}.")
    if not employers_data or not isinstance(employers_data, list):
        logger.warning("Получены некорректные данные работодателей.")
        return []

    employers_list = []
    for item in tqdm(employers_data, desc="Обработка работодателей"):
        try:
            employer = Employer(
                emp_id=int(item.get("id")),
                name=item.get("name"),
                vac_count=item.get("open_vacancies"),
                url=item.get("alternate_url"),
            )
            employers_list.append(employer)

        except (KeyError, ValueError, AttributeError) as e:
            logger.error(f"Ошибка при обработке работодателя ({item.get('id')}): {e}.")
            continue

    logger.info(f"Успешно обработано {len(employers_list)}/{len(employers_data)} работодателей.")
    return employers_list


def parse_vacancies(vacancies_data: List[Dict]) -> List[Vacancy]:
    """
    Функция для парсинга данных вакансий из API HeadHunter и преобразует их в список объектов Vacancy.

    :param vacancies_data: Список словарей с данными вакансий из API.
    :return: Список объектов вакансий.
    """
    logger.info(f"Вызов функции 'vacancies_data'. Количество полученных вакансий: {len(vacancies_data)}.")
    if not vacancies_data or not isinstance(vacancies_data, list):
        logger.warning("Получены некорректные данные вакансий.")
        return []

    vacancy_list = []
    for item in tqdm(vacancies_data, desc="Обработка вакансий"):
        try:
            vacancy = Vacancy(
                vac_id=int(item.get("id")),
                title=item.get("name"),
                salary_from=(item.get("salary") or {}).get("from"),
                salary_to=(item.get("salary") or {}).get("to"),
                emp_id=int((item.get("employer") or {}).get("id")),
                city=(item.get("area") or {}).get("name"),
                url=item.get("alternate_url"),
            )
            vacancy_list.append(vacancy)

        except (KeyError, ValueError, AttributeError) as e:
            logger.error(f"Ошибка при обработке вакансии ({item.get('id')}): {e}.")
            continue

    logger.info(f"Успешно обработано {len(vacancy_list)}/{len(vacancies_data)} вакансий.")
    return vacancy_list
