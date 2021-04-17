import sqlite3


class Item:
    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items WHERE name = ?", (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'id': row['id'], 'name': row['name'], 'price': row['price']}
        else:
            return None

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (null, ?, ?)", (name, price))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price = ? where name = ?", (price, name))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items where name = ?", (name,))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items")
        rows = result.fetchall()
        connection.close()
        if rows:
            return [{'id': row['id'], 'name': row['name'], 'price': row['price']} for row in rows]
        else:
            return None
