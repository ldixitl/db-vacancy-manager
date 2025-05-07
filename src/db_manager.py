import os
from typing import List, Tuple

import psycopg2
from dotenv import load_dotenv

from src.logger_config import add_logger
from src.models import Employer, Vacancy

# Загрузка переменных окружения
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

# Настройка логирования
logger = add_logger("db_manager.log", "db_manager")


class DBManager:
    """Класс для управления подключением и операциями с БД."""

    def __init__(self) -> None:
        """Инициализация подключения к базе данных с заданными параметрами."""
        self.params = {
            "dbname": DATABASE_NAME,
            "user": DATABASE_USER,
            "password": DATABASE_PASSWORD,
            "host": DATABASE_HOST,
            "port": DATABASE_PORT,
        }
        self.conn = psycopg2.connect(**self.params)
        logger.info(f"Подключение к БД '{DATABASE_NAME}' установлено.")

    def create_tables(self) -> None:
        """Метод для создания таблиц employers и vacancies."""
        logger.info(f"Запущен метод 'create_tables' в классе '{type(self).__name__}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employers (
	                    emp_id INTEGER PRIMARY KEY,
	                    name TEXT NOT NULL, 
	                    vac_count INTEGER, 
	                    url TEXT
                    );
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vac_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        city TEXT,
                        url TEXT,
                        emp_id INTEGER REFERENCES employers(emp_id) ON DELETE CASCADE
                    );
                    """
                )
                logger.info("Таблицы employers и vacancies созданы успешно.")

    def close_conn(self) -> None:
        """Метод для закрытия соединения с БД."""
        self.conn.close()
        logger.info("Соединение с БД успешно закрыто.")

    def insert_employers(self, employers: List[Employer]) -> None:
        """
        Метод для добавления списка работодателей в БД.

        :param employers: Список работодателей.
        """
        logger.info(f"Запущен метод 'insert_employers'. Количество работодателей: '{len(employers)}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO employers(emp_id, name, vac_count, url) VALUES (%s, %s, %s, %s)
                    ON CONFLICT (emp_id) DO NOTHING;
                    """,
                    [(emp.emp_id, emp.name, emp.vac_count, emp.url) for emp in employers],
                )
        logger.info("Работодатели успешно добавлены.")

    def insert_vacancies(self, vacancies: List[Vacancy]) -> None:
        """
        Метод для добавления списка вакансий в БД.

        :param vacancies: Список вакансий.
        """
        logger.info(f"Запущен метод 'insert_vacancies'. Количество вакансий: '{len(vacancies)}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO vacancies(vac_id, title, salary_from, salary_to, emp_id, city, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vac_id) DO NOTHING;
                    """,
                    [
                        (vac.vac_id, vac.title, vac.salary_from, vac.salary_to, vac.emp_id, vac.city, vac.url)
                        for vac in vacancies
                    ],
                )
        logger.info("Вакансии успешно добавлены.")

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Метод для получения списка всех компаний и количество вакансий у каждой компании."""
        logger.info(f"Запущен метод 'get_companies_and_vacancies_count' в классе '{type(self).__name__}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, COUNT(v.vac_id) as vacancy_count 
                    FROM employers e
                    LEFT JOIN vacancies v USING (emp_id)
                    GROUP BY e.name
                    ORDER BY vacancy_count;
                    """
                )
                employers = cur.fetchall()
                logger.info("Список компаний и количества вакансий получен успешно.")
                return employers

    def get_all_vacancies(self) -> List[Tuple]:
        """Метод для получения списка всех вакансий с указанием компании, зарплаты и ссылки."""
        logger.info(f"Запущен метод 'get_all_vacancies' в классе '{type(self).__name__}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e USING (emp_id)
                    ORDER BY e.name;
                    """
                )
                vacancies = cur.fetchall()
                logger.info(f"Всего получено '{len(vacancies)}' вакансий.")
                return vacancies

    def get_avg_salary(self) -> float:
        """Метод для получения средней зарплаты по всем вакансиям."""
        logger.info(f"Запущен метод 'get_avg_salary' в классе '{type(self).__name__}'.")
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(
                        CASE
                            WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2
                            WHEN salary_from IS NOT NULL THEN salary_from
                            WHEN salary_to IS NOT NULL THEN salary_to
                            ELSE NULL
                        END
                    ) AS avg_salary
                    FROM vacancies;
                    """
                )
                avg_salary = cur.fetchone()[0]
                logger.info(f"Средняя зарплата по вакансиям: {avg_salary}.")
                return round(avg_salary, 2)

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Метод для получения списка вакансий с зарплатой выше средней по всем вакансиям."""
        logger.info(f"Запущен метод 'get_vacancies_with_higher_salary' в классе '{type(self).__name__}'.")
        avg_salary = self.get_avg_salary()
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e USING (emp_id)
                    WHERE (salary_from IS NOT NULL AND salary_from > %s)
                        OR (salary_to IS NOT NULL AND salary_to > %s)
                    ORDER BY salary_from DESC, salary_to DESC;
                    """,
                    (avg_salary, avg_salary),
                )
                vacancies = cur.fetchall()
                logger.info(f"Получено '{len(vacancies)}' вакансий с зарплатой выше средней ({avg_salary}).")
                return vacancies

    def get_vacancies_with_keyword(self, keywords: List[str]) -> List[Tuple]:
        """
        Метод для получения списка вакансий, в названии которых содержатся ключевые слова.

        :param keywords: Список ключевых слов для поиска в названии вакансии.
        :return: Список вакансий.
        """
        logger.info(
            f"Запущен метод 'get_vacancies_with_keyword' в классе '{type(self).__name__}' с параметром: '{keywords}'."
        )
        with self.conn:
            with self.conn.cursor() as cur:
                like_string = " OR ".join(["title ILIKE %s"] * len(keywords))
                params = tuple(f"%{keyword}%" for keyword in keywords)
                cur.execute(
                    f"""
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e USING (emp_id)
                    WHERE {like_string}
                    ORDER BY v.title;
                    """,
                    params,
                )
                vacancies = cur.fetchall()
                logger.info(f"Найдено '{len(vacancies)}' вакансий по ключевым словам: {keywords}.")
                return vacancies
