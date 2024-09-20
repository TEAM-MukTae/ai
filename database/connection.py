import pymysql, os
from database.query_constant import *

# IP = os.environ['DB_HOST']
# ID = os.environ['DB_ID']
# PW = os.environ['DB_PW']

IP = 'mukdb.cti6eowgm07w.ap-northeast-2.rds.amazonaws.com'; 
PORT = 3306

ID = 'admin'    
PW = 'ajrxo123'
def get_connection():
    return pymysql.connect(host = IP, user = ID, password=PW, db = 'muktae', charset='utf8')