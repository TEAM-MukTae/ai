from database.connection import get_connection
from database.query_constant import INSERT_SUMMARIES

def insert_summaries(r_id: int, summary: str) -> tuple:
    with get_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_SUMMARIES, (r_id, summary,))
                connection.commit()
                return cursor.lastrowid
            
        except Exception as e:
            print(f'Error occurred while fetching records: {e}')
            connection.rollback()
            return -1