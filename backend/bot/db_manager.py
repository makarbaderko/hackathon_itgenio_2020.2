import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, username):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `delivery` WHERE `username` = ?', (username,)).fetchall()
            return bool(len(result))
    def add_user(self, username, name, surname, phone, adress, city):
        with self.connection:
            return self.cursor.execute("INSERT INTO `delivery` (`username`, `name`, `surname`, `phone-number`, `adress`, `city`) VALUES(?,?)", (username, name, surname, phone, adress, city))
    def get_user_data(self, username):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `delivery` WHERE `username` = `?`', (username,)).fetchall()
            return result
    def get_food(self, order):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM restaurant WHERE order_id = {order}").fetchall()
            return result
    def update_status(self, order, status):
        with self.connection:
            result = self.cursor.execute(f"UPDATE delivery SET STATUS = {status} WHERE 'order' = {order};").fetchall()
            print(result)
    def get_all_orders(self):
        with self.connection:
            result = self.cursor.execute("SELECT  order_id, food, courier_id FROM restaurant WHERE STATUS != 'BEEN_DELIVERED';").fetchall()
            return result

