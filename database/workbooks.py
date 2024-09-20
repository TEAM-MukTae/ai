from database.connection import get_connection
from database.query_constant import INSERT_WORKBOOKS

def insert_workbooks(u_id: int, title: str, problem_set: str) -> int:
    with get_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_WORKBOOKS, (u_id, title, problem_set,))
                connection.commit()
                return cursor.lastrowid
            
        except Exception as e:
            print(f'Error occurred while fetching records: {e}')
            connection.rollback()
            return -1