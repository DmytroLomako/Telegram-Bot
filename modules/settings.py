import sqlite3, aiogram

api_token = ''

ID_ADMIN = 
user_status = {}
new_product = {
    'name': '',
    'price': 0,
    'description': ''
}


connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, description TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, cart_id INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS Carts (id INTEGER PRIMARY KEY, user_id INTEGER, products_id TEXT)')
connection.commit()

bot = aiogram.Bot(token = api_token)
dispatcher = aiogram.Dispatcher()