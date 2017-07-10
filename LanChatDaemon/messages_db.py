import sqlite3
import os

DATA_BASE_NAME = "/messages_db.db"
TABLE_NAME = "user_messages"


class MessagesDB:
    full_db_path = ""
    cursor = None
    db_conn = None

    def __init__(self, db_name):
        """Init class members"""
        self.full_db_path = os.getcwd()
        self.full_db_path += db_name
        self.db_conn = sqlite3.connect(self.full_db_path)
        self.cursor = self.db_conn.cursor()
        self.__create_table_if_not_exist()
	self.cursor.execute('DELETE FROM {0};'.format(TABLE_NAME))

    def __del__(self):
        """close db connection when finish work"""
        self.db_conn.close()

    def __create_table_if_not_exist(self):
        """Function create new table in db, if not exist"""
        query = 'create TABLE IF NOT EXISTS {} (user_name char(255), time_stamp DATE, message char(255));'.format(TABLE_NAME)
        try:
            self.cursor.execute(query)
        except sqlite3.DatabaseError as err:
            # print error message to display
            print ("Error: ", err)
        else:
            self.db_conn.commit()

    def add_message_to_db(self, user_name, date_time, message):
        """Function insert @user_name and @message into db table"""
        try:
            self.cursor.execute('INSERT INTO {0} (user_name, time_stamp, message) VALUES (?,?,?);'.format(TABLE_NAME),
                                (user_name, date_time, message))
        except sqlite3.DatabaseError as err:
            print ("Error: ", err)
        else:
            # fetch all return empty list if no error
            print(self.cursor.fetchall())
            # commit changes in database
            self.db_conn.commit()

    def get_messages(self, user_name, select_all=False):
        """Function return all messages in table by @user_name"""
        search_name = (user_name, )
        try:
            if select_all:
                # execute this query only for user name 'backdoor'
                self.cursor.execute('SELECT * FROM {};'.format(TABLE_NAME))
            else:
                self.cursor.execute('SELECT * FROM {0} WHERE user_name=?;'.format(TABLE_NAME), search_name)
        except sqlite3.DatabaseError as err:
            print ("Error: ", err)
        return self.cursor.fetchall()

    def del_messages(self, user_name):
        """Function delete all messages in table by @user_name"""
        search_name = (user_name, )
        try:
            self.cursor.execute('DELETE FROM {0} WHERE user_name=?;'.format(TABLE_NAME), search_name)
        except sqlite3.DatabaseError as err:
            print ("Error: ", err)
        else:
            # commit changes in database
            self.db_conn.commit()
        return self.cursor.fetchall()
