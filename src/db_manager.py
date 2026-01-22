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