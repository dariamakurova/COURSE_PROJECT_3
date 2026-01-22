from typing import Any

import psycopg2

from src.hh_api import HeadHunterAPI
from src.hh_employer_api import HeadHunterEmployerAPI


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    employer_id INT NOT NULL,
                    url TEXT NOT NULL,
                    salary_from INT NOT NULL,
                    salary_to INT NOT NULL,
                    salary_currency VARCHAR(10) NOT NULL,
                    requirement TEXT,
                    
                    CONSTRAINT fk_vacancies_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )
            """)

    conn.commit()
    conn.close()

def get_employer_with_vacancies(employer_id: str) -> dict:
    """Формирование словаря с данными о компании и ее вакансиях по id"""

    data = HeadHunterEmployerAPI().get_employer_info(employer_id)
    vacancies = HeadHunterAPI().get_vacancies(employer_id)
    data["vacancies"] = vacancies

    return data


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о работодателях и компаниях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_id = employer["employer_id"]
            employer_name = employer["employer_name"]
            cur.execute("""
            INSERT INTO employers (employer_id, name)
            VALUES (%s, %s)""", (employer_id, employer_name))
            emp_vacancies = employer["vacancies"]
            for vacancy in emp_vacancies:
                vacancy_id = vacancy["vac_id"]
                name = vacancy["name"]
                employer_id = vacancy["employer_id"]
                url = vacancy["url"]
                salary_from = vacancy["salary_from"]
                salary_to = vacancy["salary_to"]
                salary_currency = vacancy["salary_currency"]
                requirement = vacancy["requirement"]
                cur.execute("""
                INSERT INTO vacancies (vacancy_id, name, employer_id, url, salary_from, salary_to, salary_currency, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (vacancy_id, name, employer_id, url, salary_from, salary_to, salary_currency, requirement))

    conn.commit()
    conn.close()