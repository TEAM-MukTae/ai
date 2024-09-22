from database.connection import get_connection
from database.query_constant import FETCH_RECORDS, FETCH_ONE_RECORDS
from pymysql.cursors import DictCursor

def fetch_records_one(id: int) -> tuple:
    with get_connection() as connection:
        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(FETCH_ONE_RECORDS, id)
                return cursor.fetchone()
        
        except Exception as e:
            print(f'Error occurred while fetching records: {e}')
            return {}
        

def fetch_records(idList: list) -> list:
    with get_connection() as connection:
        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(FETCH_RECORDS(len(idList)), (idList))
                return list(cursor)
        
        except Exception as e:
            print(f'Error occurred while fetching records: {e}')
            return []