from database.query_constant import FETCH_USER
from connection import get_connection

def get_user():
    with get_connection() as connection:
        try:  
            with connection.cursor() as cursor:
                cursor.execute(FETCH_USER, ('1'))
                result = cursor.fetchone()
                return result
                
        except Exception as e:
            print(f'Error occurred while fetching user data: {e}')
            return ()