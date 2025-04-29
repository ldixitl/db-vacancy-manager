import logging
import os
import time

from tqdm import tqdm

from src.db_manager import DBManager
from src.external_api import HeadHunterAPI
from src.utils import parse_employers, parse_vacancies

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/main.log", mode="w", encoding="UTF-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main() -> None:
    """Главная функция, запускающая все реализованные модули проекта."""
    db_manager = None
    try:
        logger.info("Начало работы приложения.")
        print("🔎 Добро пожаловать в систему поиска вакансий!")
        time.sleep(0.5)

        # Получение данных с API
        logger.info("Получение данных от API HeadHunter")
        print("\n🔄 Получаем данные о вакансиях...")

        api = HeadHunterAPI()
        employers_data = api.get_employers()
        vacancies_data = []
        for employer in tqdm(employers_data, desc="Получение данных о вакансиях"):
            vacancies_data.extend(api.get_vacancies(int(employer.get("id"))))

        # Преобразовываем полученные данные
        logger.info("Обработка полученных данных.")
        employers = parse_employers(employers_data)
        vacancies = parse_vacancies(vacancies_data)

        # Инициализация базы данных
        logger.info("Инициализация базы данных")
        print("💾 Сохраняем данные в базу...")

        db_manager = DBManager()
        db_manager.create_tables()
        db_manager.insert_employers(employers)
        db_manager.insert_vacancies(vacancies)

        print("✅  Данные успешно загружены!")
        time.sleep(0.5)

        # Пользовательский интерфейс
        while True:
            print("\nМеню управления вакансиями:")
            print("1 - 🏢 Список компаний и количество вакансий")
            print("2 - 📜 Список всех вакансий")
            print("3 - 💲 Средняя зарплата по вакансиям")
            print("4 - ⬆️ Вакансии с зарплатой выше средней")
            print("5 - 🔎 Поиск вакансий по ключевому слову")
            print("0 - 🚪 Выход")

            logger.info("Пользователь выбирает действие в меню управления вакансиями.")
            user_choice = input("Выберите действие: ").strip()
            time.sleep(0.5)
            logger.info(f"Пользователь ввёл: {user_choice}.")

            if user_choice == "1":
                print("\nКомпании и количество вакансий:")
                for company in db_manager.get_companies_and_vacancies_count():
                    print(f"➢ {company[0]}: {company[1]} вакансий.")
            elif user_choice == "2":
                print("\nСписок вакансий:")
                for vacancy in db_manager.get_all_vacancies():
                    if vacancy[2] and vacancy[3]:
                        if vacancy[2] == vacancy[3] and vacancy[2] > 0:
                            salary_text = f"{vacancy[2]} ₽"
                        else:
                            salary_text = f"{vacancy[2]} — {vacancy[3]} ₽"
                    elif vacancy[2] and vacancy[2] > 0:
                        salary_text = f"от {vacancy[2]} ₽"
                    elif vacancy[3] and vacancy[3] > 0:
                        salary_text = f"до {vacancy[3]} ₽"
                    else:
                        salary_text = "Зарплата не указана"
                    print(f"➢ {vacancy[1]} | Компания: {vacancy[0]} | {salary_text} | {vacancy[4]}")
            elif user_choice == "3":
                avg = db_manager.get_avg_salary()
                print(f"\n➢ Средняя зарплата по вакансиям: {avg} руб.")
            elif user_choice == "4":
                print("\nВакансии с зарплатой выше средней:")
                for vacancy in db_manager.get_vacancies_with_higher_salary():
                    if vacancy[2] and vacancy[3]:
                        if vacancy[2] == vacancy[3] and vacancy[2] > 0:
                            salary_text = f"{vacancy[2]} ₽"
                        else:
                            salary_text = f"{vacancy[2]} — {vacancy[3]} ₽"
                    elif vacancy[2] and vacancy[2] > 0:
                        salary_text = f"от {vacancy[2]} ₽"
                    elif vacancy[3] and vacancy[3] > 0:
                        salary_text = f"до {vacancy[3]} ₽"
                    else:
                        salary_text = "Зарплата не указана"
                    print(f"➢ {vacancy[1]} | Компания: {vacancy[0]} | {salary_text} | {vacancy[4]}")
            elif user_choice == "5":
                while True:
                    keywords = input("\nВведите ключевые слова через пробел: ").strip().split()
                    time.sleep(0.5)
                    if keywords:
                        vacancies = db_manager.get_vacancies_with_keyword(keywords)
                        print(f"\nНайдено {len(vacancies)} вакансий по запросу '{keywords}':")
                        time.sleep(1)
                        if vacancies:
                            for vacancy in vacancies:
                                if vacancy[2] and vacancy[3]:
                                    if vacancy[2] == vacancy[3] and vacancy[2] > 0:
                                        salary_text = f"{vacancy[2]} ₽"
                                    else:
                                        salary_text = f"{vacancy[2]} — {vacancy[3]} ₽"
                                elif vacancy[2] and vacancy[2] > 0:
                                    salary_text = f"от {vacancy[2]} ₽"
                                elif vacancy[3] and vacancy[3] > 0:
                                    salary_text = f"до {vacancy[3]} ₽"
                                else:
                                    salary_text = "Зарплата не указана"
                                print(f"➢ {vacancy[1]} | Компания: {vacancy[0]} | {salary_text} | {vacancy[4]}")
                            break
                        else:
                            print("\n⚠️ По вашему запросу ничего не найдено.")
                            time.sleep(0.5)
                            break
                    else:
                        logger.info("Пользователь не ввёл слова для поиска. Пользователю предложено повторить ввод.")
                        print("⚠️ Пожалуйста, введите ключевые слова для поиска.")
                        time.sleep(0.5)

            elif user_choice == "0":
                print("\n👋🏻 Выход из программы.")
                time.sleep(0.5)
                break
            else:
                logger.info(f"Некорректный ответ: {user_choice}. Пользователю предложено повторить ввод.")
                print("⚠️ Некорректный ответ. Повторите ввод.")
                time.sleep(0.5)

    except Exception as e:
        logger.error(f"Произошла ошибка при работе программы: {e}.", exc_info=True)
        print(f"⚠️ Произошла ошибка: {e}")
    finally:
        logger.info("Завершение работы программы.")
        if db_manager:
            db_manager.close_conn()


if __name__ == "__main__":
    main()
