import sqlite3
from uuid import uuid4
import bcrypt
import time
import os

class DatabaseManager:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS tokens (timestamp int, token varchar(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS login (username varchar(255), password varchar(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pages (name varchar(255), id int)")
        self.connection.commit()
        #self.create_login("Jetvac2", "Password")

    def hash(self, token, salt_level=12):
        salt = bcrypt.gensalt(salt_level)
        return bcrypt.hashpw(token.encode("utf-8"), salt)


    def finish(self):
        self.connection.close()


    #Token
    def generate_token(self):
        token = uuid4().hex
        self.cursor.execute('''INSERT INTO tokens 
                            (timestamp, token)
                            VALUES
                            (?, ?)
                            ''',
                            (time.time(), self.hash(token)))

        self.connection.commit()
        return token
    
    def verify_token(self, token):
        self.cursor.execute("DELETE FROM tokens Where timestamp < ?", (time.time() - 480,))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM tokens")
        users = self.cursor.fetchall()

        for user in users:
            try:
                if bcrypt.checkpw(token.encode("utf-8"), user[1]):
                    return True
            except ValueError:
                pass
        
        return False

    def removeToken(self, token):
        self.cursor.execute("SELECT * FROM tokens")
        users = self.cursor.fetchall()

        for user in users:
            try:
                if bcrypt.checkpw(token.encode("utf-8"), user[1]):
                    self.cursor.execute("DELETE FROM tokens Where token = ?", (user[1],))
                    self.connection.commit()
                    return True
            except ValueError:
                pass
        
        self.connection.commit()
        return False

    #Save log in information
    def create_login(self, username, password):
        self.cursor.execute('''INSERT INTO login 
                            (username, password)
                            VALUES
                            (?, ?)
                            ''',
                            (self.hash(username), self.hash(password)))
        self.connection.commit()
        
    def verify_login(self, username, password):
        self.cursor.execute("SELECT * FROM login")
        all_info = self.cursor.fetchall()

        for info in all_info:
            try:
                if bcrypt.checkpw(username.encode("utf-8"), info[0]) and bcrypt.checkpw(password.encode("utf-8"), info[1]):
                    return True
            except ValueError:
                pass
        
        return False

    
    def savePage(self, name):
        self.cursor.execute('''INSERT INTO pages 
                            (name, id)
                            VALUES
                            (?, ?)
                            ''',
                            (name, self.getNextPageId()))
        self.connection.commit()

    def getNextPageId(self):
        self.cursor.execute("SELECT id FROM pages")
        all_IDs = self.cursor.fetchall()
        max = 0
        for id in all_IDs:
            if int(id[0]) > max:
                max = int(id[0])

        self.connection.commit()
        return max+1

    def getListOfPageIds(self):
        self.cursor.execute("SELECT * FROM pages")
        listOfPages = self.cursor.fetchall()
        ids = []
        for pageId in listOfPages:
            ids.append(int(pageId[1]))
            ids.append(pageId[0])

        return ids

    def createPage(self, name):
        try:
          page = open("templates/" + name + ".html", "x")
          page.write("<h1>" + name + "</h1>")
          self.savePage(page.name)
        except FileExistsError:
            pass

    def delPage(self, name):
        self.cursor.execute("DELETE FROM pages Where name = ?", ("templates/" + name + ".html",))
        try:
          os.remove("templates/" + name + ".html")
        except FileExistsError:
            pass

    def getPageById(self, id):
        self.cursor.execute("SELECT * FROM pages")
        pages = self.cursor.fetchall()
        print(id)
        for i in range(len(pages)):
            print(pages[i][1])
            if(pages[i][1] == int(id[1:2])):
                return pages[i][0]

        self.connection.commit()
        return "No Matching ID"

    def printPages(self):
        self.cursor.execute("SELECT * FROM pages")
        print(self.cursor.fetchall())
        self.connection.commit()

    def print_database(self):
        self.cursor.execute("SELECT * FROM tokens")
        print(self.cursor.fetchall())
        self.connection.commit()

    '''
        Make the plus button create a new file
        And save files created files into a database
        Then send a post get request from the js to get a list of every file path
        Create an a tag for each page and add then to the navbar
        Make the subtract button remove a file based on the name inputed, simeler to the add menue just with deleation instead of creation
    '''