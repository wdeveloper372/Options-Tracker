import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host = "localhost",
    port = 3306,
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")

)

print(mydb)
cursor = mydb.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trades (id INT AUTO_INCREMENT " \
"PRIMARY KEY, ticker VARCHAR(255))")

sql = "INSERT INTO trades (ticker) VALUES (%s)"
trade_data = ("AAPL",)

cursor.execute(sql, trade_data)

mydb.commit()


cursor.close()
mydb.close()