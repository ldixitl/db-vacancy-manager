# Проект *DB Vacancy Manager*

## Описание

*DB Vacancy Manager* — это консольное приложение на Python, предназначенное для получения, обработки и анализа данных о работодателях и вакансиях с платформы hh.ru. Программа автоматически собирает данные, создает объекты компаний и вакансий, обеспечивает логирование и взаимодействие с базой данных.

### Реализованные функции:
#### Взаимодействие с API (модуль `external_api.py`)
- **Класс `HeadHunterAPI`** — реализация абстрактного интерфейса `VacancyAPI` для подключения к API hh.ru.
- **Получение работодателей (`get_employers`)** — ищет компании по заданным названиям, используя файл `user_settings.json`.
- **Получение вакансий (`get_vacancies`)** — загружает вакансии по ID работодателя с постраничной загрузкой и логированием.
#### Модели данных (модуль `models.py`)
- **Класс `Employer`** — описывает работодателя с полями `emp_id`, `name`, `vac_count`, `url`, поддерживает валидацию и логирование.
- **Класс `Vacancy`** — описывает вакансию с полями `vac_id`, `title`, `salary_from`, `salary_to`, `emp_id`, `city`, `url`.
#### Абстрактные классы (модуль `base.py`)
- **`VacancyAPI`** — абстрактный интерфейс для реализации клиентов API платформ вакансий. Определяет обязательные методы `_connect()`, `get_employers()` и `get_vacancies()`.
#### Логгирование (модуль `logger_config.py`)
- **Функция `add_logger()`** — создает логгер с именем и файлом лога, сохраняемым в папке `logs/`.
#### Обработка данных (модуль `utils.py`)
- **Функция `parse_employers()`** — преобразует сырые данные работодателей из API в список объектов `Employer` с валидацией и логированием ошибок.
- **Функция `parse_vacancies()`** — парсит данные вакансий, обрабатывает зарплаты и создает объекты `Vacancy`.
#### Управление БД (модуль `db_manager.py`)
- **Класс `DBManager`** — обеспечивает подключение к PostgreSQL и операции с вакансиями:
  - Создание таблиц (`employers`, `vacancies`)
  - Заполнение данными (`insert_employers`, `insert_vacancies`)
  - Получение статистики (средняя зарплата, вакансии по ключевым словам)
#### Главный скрипт (`main.py`)
- **Консольный интерфейс** — предоставляет меню для:
  - Поиска вакансий по ключевым словам
  - Просмотра компаний и количества вакансий
  - Анализа зарплат (средняя, выше средней)
  - Просмотра вакансий

## Примеры работы функций
### Инициализация базы данных и загрузка данных
```python
from src.external_api import HeadHunterAPI
from src.db_manager import DBManager
from src.utils import parse_employers, parse_vacancies

# Получение данных с API
api = HeadHunterAPI()
employers_data = api.get_employers()
vacancies_data = []
for employer in employers_data:
    vacancies_data.extend(api.get_vacancies(employer['id']))

# Подготовка данных
employers = parse_employers(employers_data)
vacancies = parse_vacancies(vacancies_data)

# Загрузка в БД
db = DBManager()
db.create_tables()
db.insert_employers(employers)
db.insert_vacancies(vacancies)
```

### Получение аналитики по вакансиям
```python
# Список компаний с количеством вакансий
companies = db.get_companies_and_vacancies_count()
for company in companies:
    print(f"{company[0]}: {company[1]} вакансий")

# Средняя зарплата
avg_salary = db.get_avg_salary()
print(f"Средняя зарплата: {avg_salary} руб.")

# Вакансии с зарплатой выше средней
high_salary_vacancies = db.get_vacancies_with_higher_salary()
for vacancy in high_salary_vacancies:
    print(vacancy[1], vacancy[2], vacancy[3])
```

### Поиск вакансий по ключевым словам
```python
# Поиск по нескольким ключевым словам
python_vacancies = db.get_vacancies_with_keyword(["python", "django"])
for vac in python_vacancies:
    print(f"{vac[1]} ({vac[0]}) | Зарплата: {vac[2]} - {vac[3]} | {vac[4]}")
```

### Пример работы с моделями данных
```python
from src.models import Employer, Vacancy

# Создание объекта работодателя
employer = Employer(
    emp_id=123,
    name="Яндекс",
    vac_count=42,
    url="https://hh.ru/employer/123"
)

# Создание объекта вакансии
vacancy = Vacancy(
    vac_id=456,
    title="Python разработчик",
    salary_from=150000,
    salary_to=200000,
    emp_id=123,
    city="Москва",
    url="https://hh.ru/vacancy/456"
)
print(vacancy)  # Автоматическое форматирование зарплаты
```

## Установка:
1. Клонируйте репозиторий:
```
git clone https://github.com/ldixitl/db-vacancy-manager.git
```
2. Установите зависимости:
Используется Poetry для управления зависимостями. Убедитесь, что Poetry установлен.
После установки выполните:
```
poetry install
```
3. Создайте файл переменных окружения `.env` - [**шаблон такого файла**](.env.sample).

## Использование:
Для запуска приложения необходимо выполнить команду:
```sh
python main.py
```
Программа автоматически загрузит данные о вакансиях с HeadHunter API, сохранит их в базу данных и откроет интерактивное меню с возможностями:
- Просмотр списка компаний и количества вакансий
- Анализ зарплат (средняя, выше средней)
- Поиск вакансий по ключевым словам
- Полный список вакансий с детализацией

## Лицензия
Этот проект лицензирован по [лицензии MIT](LICENSE).
