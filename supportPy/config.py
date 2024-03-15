from pymysql import connect
from playhouse.pool import MySQLDatabase

host = 'localhost'
user = 'root'
password = ''
db_name = 'week4'

conn = connect(host=host,
               user=user,
            password=password)

conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
conn.close()

db = MySQLDatabase(db_name, user=user, password=password, host=host)


