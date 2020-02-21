import sqlite3
import os.path
class dbManager:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "eco.db")
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def addUser(self, username, name, password, email):
        print("ADD USER", username, name, password, email)
        self.c.execute("INSERT INTO users (login, Name, Password, email) VALUES(?, ?, ?, ?)", (username, name, password, email))
        self.conn.commit()
    
    def checkUser(self, username, password):
        self.c.execute("SELECT * FROM users WHERE login=? AND password=?", (username, password))
        return self.c.fetchone()
