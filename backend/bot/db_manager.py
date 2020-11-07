import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, username):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `delivery` WHERE `username` = ?', (username,)).fetchall()
            return bool(len(result))
    def add_user(self, username, name, surname, phone, adress):
        with self.connection:
            return self.cursor.execute("INSERT INTO `delivery` (`username`, `name`, `surname`, `phone-number`, `adress`) VALUES(?,?)", (username, name, surname, phone, adress))
    def get_user_data(self, username):
        with self.connection:
            return self.cursor.execute("")