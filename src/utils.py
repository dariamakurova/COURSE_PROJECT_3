import psycopg2

def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    employer_id INT  NOT NULL,
                    employer VARCHAR(50) NOT NULL,
                    url TEXT NOT NULL,
                    salary INT NOT NULL,
                    requirement TEXT,
                    
                    CONSTRAINT fk_vacancies_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )
            """)

    conn.commit()
    conn.close()