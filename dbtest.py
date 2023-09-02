from operator import concat
import mariadb as db

dic = {
    "user": "z2z63",
    "password": "681769",
    "host": "localhost",
    "port": 3306,
    "database": "bili_recsys_dataset",
}

connection = db.connect(**dic)
cursor = connection.cursor()
cursor.execute(
    "insert ignore artist (artist_163_id, name) VALUE (?,?)", (123456789, "张三")
)
connection.commit()
