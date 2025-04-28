from typing import Union

from src.logger_config import add_logger

# Настройка логирования
logger = add_logger("models.log", "models")


class Employer:
    """Класс для представления работодателя."""

    __slots__ = ("__emp_id", "__name", "__vac_count", "__url")

    def __init__(self, emp_id: int, name: str, vac_count: int, url: str) -> None:
        """
        Инициализация объекта работодателя.

        :param emp_id: Идентификатор работодателя.
        :param name: Название компании.
        :param vac_count: Количество открытых вакансий.
        :param url: Ссылка на страницу работодателя.
        """
        self.__emp_id = emp_id if emp_id is not None else -1
        self.__name = name.strip() if name else "Без названия"
        self.__vac_count = vac_count if vac_count is not None else 0
        self.__url = url.strip() if url else "Ссылка не указана"
        logger.info(f"Создан объект класса Employer для компании - {self.__name}.")

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Employer."""
        return f"{self.__name} (ID - {self.__emp_id}) | Вакансий — {self.__vac_count} | {self.__url}"

    @property
    def emp_id(self) -> int:
        """Геттер для получения идентификатора работодателя."""
        return self.__emp_id

    @property
    def name(self) -> str:
        """Геттер для получения названия компании."""
        return self.__name

    @property
    def vac_count(self) -> int:
        """Геттер для получения количества открытых вакансий."""
        return self.__vac_count

    @property
    def url(self) -> str:
        """Геттер для получения ссылки на страницу работодателя."""
        return self.__url


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("__vac_id", "__title", "__salary_from", "__salary_to", "__emp_id", "__city", "__url")

    def __init__(
        self,
        vac_id: int,
        title: str,
        salary_from: Union[int, None],
        salary_to: Union[int, None],
        emp_id: int,
        city: str,
        url: str,
    ) -> None:
        """
        Инициализирует объект вакансии.

        :param vac_id: ID вакансии.
        :param title: Название вакансии.
        :param salary_from: Нижняя граница зарплаты.
        :param salary_to: Верхняя граница зарплаты.
        :param emp_id: ID компании.
        :param city: Город.
        :param url: Ссылка на вакансию.
        """
        self.__vac_id = vac_id if vac_id is not None else -1
        self.__title = title.strip() if title else "Без названия"
        self.__salary_from = salary_from if salary_from is not None else 0
        self.__salary_to = salary_to if salary_to is not None else 0
        self.__emp_id = emp_id if emp_id is not None else -1
        self.__city = city.strip() if city else "Город не указан"
        self.__url = url.strip() if url else "Ссылка не указана"
        logger.info(f"Создан объект класса Vacancy для вакансии - {self.__title} (ID:{self.__vac_id}).")

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Vacancy."""
        salary_text = "Зарплата не указана"

        if self.__salary_from and self.__salary_to:
            if self.__salary_from == self.__salary_to:
                salary_text = f"{self.__salary_from} ₽"
            else:
                salary_text = f"{self.__salary_from} — {self.__salary_to} ₽"
        elif self.__salary_from:
            salary_text = f"от {self.__salary_from} ₽"
        elif self.__salary_to:
            salary_text = f"до {self.__salary_to} ₽"

        return f"{self.__title} | ID работодателя: {self.__emp_id} | {self.__city} | {salary_text} | {self.__url}"

    @property
    def vac_id(self) -> int:
        """Геттер для получения ID вакансии."""
        return self.__vac_id

    @property
    def title(self) -> str:
        """Геттер для получения названия вакансии."""
        return self.__title

    @property
    def salary_from(self) -> int:
        """Геттер для получения нижней границы зарплаты."""
        return self.__salary_from

    @property
    def salary_to(self) -> int:
        """Геттер для получения верхней границы зарплаты."""
        return self.__salary_to

    @property
    def emp_id(self) -> int:
        """Геттер для получения идентификатора вакансии."""
        return self.__emp_id

    @property
    def city(self) -> str:
        """Геттер для получения города вакансии."""
        return self.__city

    @property
    def url(self) -> str:
        """Геттер для получения ссылки на вакансию."""
        return self.__url
