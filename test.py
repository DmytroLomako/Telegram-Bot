import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS Orders')

connection.commit()
connection.close()