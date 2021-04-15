
import sqlite3

connection = sqlite3.connect('../data2.db')  # pylint: disable=no-member

cursor = connection.cursor()

cursor.execute('DROP TABLE users')
cursor.execute("CREATE TABLE users (id int, username text, password text)")
cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, 'Tony', 'TonyTony'))
connection.commit()
cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", [
                   (2, 'Tony2', 'TonyTony2'), (4, 'Tony3', 'TonyTony3')])
connection.commit()

for row in cursor.execute("SELECT ALL * FROM users"):
    print(row)

connection.commit()

connection.close()
