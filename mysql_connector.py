from colorama import Cursor
import keyconfig as senv
import mysql.connector

def set_connection():
    db = mysql.connector.connect(
    host="localhost",
    user=senv.MYSQL_USERNAME,
    password=senv.MYSQL_PASSWORD,
    database = senv.DATABASE
    )
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS amazon_data (
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            price INT,
            image_url VARCHAR(255)
            """)
    return db,cursor

def add_value(db,cursor,data):
    sql = "INSERT INTO customers (title, description, price , image_url) VALUES (%s, %s)"
    for info_dict in data:
        val = (info_dict['title'],info_dict['product_details'],info_dict['price'],info_dict['image_url'])
        cursor.execute(sql, val)
        db.commit()
    print("Data inserted")
