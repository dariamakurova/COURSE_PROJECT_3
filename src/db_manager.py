import psycopg2


class DBManager():
    """Класс для работы с базой данных о работодателях и вакансиях"""

    def __init__(self, db_name: str, params):
        self.__db_name = db_name
        self.__params = params

    def get_vacancies_amount_per_employer(self):
        """Метод для получения списка всех компаний и количества вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers.name, COUNT(vacancies.vacancy_id) AS active_vacancies
                FROM employers 
                JOIN vacancies USING(employer_id)
                GROUP BY employers.name""")
                return cur.fetchall()
        finally:
            conn.close()

    def get_all_vacancies(self):
        """Метод для получения списка всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.salary_currency, v.url
                FROM employers AS e
                JOIN vacancies AS v USING(employer_id)
                ORDER BY e.name""")
                return cur.fetchall()
        finally:
            conn.close()

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT AVG(v.salary_to) AS avg_salary
                FROM vacancies AS v""")
                return cur.fetchall()
        finally:
            conn.close()

    def get_vacancies_higher_than_avg(self):
        """Метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT * 
                FROM vacancies AS v
                WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)""")
                return cur.fetchall()
        finally:
            conn.close()

    def get_vacancies_by_keyword(self, keyword):
        """Метод для получения списка всех вакансий, в названии которых содержатся переданные в метод слова"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                SELECT * 
                FROM vacancies AS v
                WHERE v.name ILIKE '%{keyword}%'""")
                return cur.fetchall()
        finally:
            conn.close()