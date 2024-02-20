import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()
    #sadsds
    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res: return res
        except:
            print("Error get data from DataBase")
        return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cursor.execute("INSERT INTO posts VALUES(NULL,?,?,?)", (title, text,tm))
            self.__db.commit()
            return True
        except:
            print("Error adding post")
            return False

