import sqlite3

connection = sqlite3.connect('../data.db')  # pylint: disable=no-member

cursor = connection.cursor()

# cursor.execute("DROP TABLE users")
# connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARYKEY , username TEXT, password TEXT)")

connection.commit()

connection.close()
