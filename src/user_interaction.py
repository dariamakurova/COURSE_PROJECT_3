from typing import Any

from data.top_employers import top_employers
from src.config import config
from src.db_manager import DBManager
from src.utils import create_database, get_employer_with_vacancies, save_data_to_database


def get_user_choice(database_name: str, params) -> list | Any:
    """Функция обработки пользовательского выбора"""

    db = DBManager(database_name, params)
    result = None

    while True:
        user_choice = input(
            "Выберите необходимый пункт меню:\n"
            "1. Вывести список компаний с количеством активных вакансий\n"
            "2. Вывести список всех открытых вакансий\n"
            "3. Показать среднюю заработную плату по всем вакансиям\n"
            "4. Вывести список вакансий с заработной платой выше среднего\n"
            "5. Найти вакансии по ключевому слову\n"
            "Ваш выбор: "
        ).strip()

        available_options = ["1", "2", "3", "4", "5"]
        if user_choice in available_options:

            if int(user_choice) == 1:
                result = db.get_vacancies_amount_per_employer()
            elif int(user_choice) == 2:
                result = db.get_all_vacancies()
            elif int(user_choice) == 3:
                result = db.get_avg_salary()
            elif int(user_choice) == 4:
                result = db.get_vacancies_higher_than_avg()
            elif int(user_choice) == 5:
                keywords = input("Введите ключевые слова для фильтрации вакансий: ")
                result = db.get_vacancies_by_keyword(keywords)
                if len(result) == 0:
                    result = "Ничего не найдено"
            break

        else:
            print("Введите 1, 2, 3, 4 или 5")

    return result


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""

    print(
        "Сейчас я сформирую базу данных с информацией о 10 топовых работодателях и их открытых вакансиях.\n"
        "Для этого потребуется некоторое время...\n"
    )

    params = config()
    database_name = "hh_vacancies"

    # создаем базу данных
    create_database(database_name, params)

    # получаем данные
    data = []
    for key, value in top_employers.items():
        data.append(get_employer_with_vacancies(value))

    # заносим полученнные данные в базу данных
    save_data_to_database(data, database_name, params)

    # запускаем взаимодействие с пользователем:

    while True:
        result = get_user_choice(database_name, params)
        print(result)

        user_choice_2 = input("\nХотите посмотреть еще какую-то информацию? Да/Нет: \n").strip().lower()
        if user_choice_2 != "да":
            break
