from database.connection import get_connection
from database.query_constant import INSERT_KEYWORDS

def insert_keywords(r_id, rs_id: int, names: list) -> tuple:
    with get_connection() as connection:
        try:
            with connection.cursor() as cursor:
                print(INSERT_KEYWORDS(r_id, rs_id, names))
                cursor.execute(INSERT_KEYWORDS(rs_id, names), (names))
                connection.commit()
            
        except Exception as e:
            print(f'Error occurred while fetching records: {e}')
            connection.rollback()
            return -1
            
        finally:
            return rs_id