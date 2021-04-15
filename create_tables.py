import sqlite3

connection = sqlite3.connect('../data.db')  # pylint: disable=no-member

cursor = connection.cursor()

# cursor.execute("DROP TABLE items")
# connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARYKEY , username TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARYKEY , name TEXT, price real)")
cursor.execute("INSERT INTO items VALUES (null, 'item1', 10.3)")


connection.commit()

connection.close()
