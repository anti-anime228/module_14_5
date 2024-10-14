import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )''')


initiate_db()


# Для наполнения таблицы
# for i in range(1, 5):
#     cursor.execute('INSERT INTO  Products(title, description, price) VALUES (?, ?, ?)',
#                    (f'Product{i}', f'Описание{i}', i * 100,))


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    return all_products


def add_user(username, email, age):
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, 1000)', (username, email, age,))
    connection.commit()

# добавить test в bd
# add_user('test', 'test', 'test')
def is_included(username):
    lst1 = []
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user in users:
        lst1.append(user[1])
    return username in lst1



cursor.execute('SELECT COUNT(*) FROM Products')
count_str = cursor.fetchone()[0]

connection.commit()
# connection.close()
