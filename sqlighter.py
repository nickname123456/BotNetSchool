import sqlite3


class SQLighter:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students ( 
                id INT,
                login TEXT,
                password TEXT,
                isFirstLogin BIT,
                week INT,
                day INT,
                lesson INT,
                correctData INT,
                link TEXT,
                school TEXT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS schedule ( 
                day INT,
                photo INT)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS chats ( 
                id INT,
                week INT,
                day INT,
                lesson INT,
                login TEXT,
                password TEXT,
                link TEXT,
                school TEXT)""")

    

    def commit(self):
        self.connection.commit()
    



    def get_schedule(self, day):
        with self.connection:
            return self.cursor.execute('SELECT photo FROM `schedule` WHERE `day` = ?', (day,)).fetchone()
    
    def edit_schedule(self, day, photo):
        with self.connection:
            return self.cursor.execute("UPDATE `schedule` SET `photo` = ? WHERE `day` = ?", (photo, day))




    
    def get_account_id(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT id FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_login(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT login FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_password(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT password FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_isFirstLogin(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT isFirstLogin FROM `students` WHERE `id` = ?', (account_id,)).fetchone()

    def get_account_day(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT day FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_lesson(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT lesson FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]
    
    def get_account_correctData(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT correctData FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_link(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT link FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_school(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT school FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]



    def add_user(self, user_id, login, password, link, school):
        with self.connection:
            return self.cursor.execute('INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)',(user_id, login, password, 1, 0, 0, 0, 0, link, school))



    def edit_account_id(self, new_id, account_id):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `id` = ? WHERE `id` = ?", (new_id, account_id))

    def edit_account_login(self, account_id, login):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `login` = ? WHERE `id` = ?", (login, account_id))

    def edit_account_password(self, account_id, password):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `password` = ? WHERE `id` = ?", ( password, account_id))

    def edit_account_isFirstLogin(self, account_id, isFirstLogin):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `isFirstLogin` = ? WHERE `id` = ?", (isFirstLogin, account_id))

    def edit_account_day(self, account_id, day):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `day` = ? WHERE `id` = ?", (day, account_id))

    def edit_account_lesson(self, account_id, lesson):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `lesson` = ? WHERE `id` = ?", (lesson,account_id))

    def edit_account_correctData(self, account_id, correctData):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `correctData` = ? WHERE `id` = ?", (correctData, account_id))
    
    def edit_account_week(self, account_id, week):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `week` = ? WHERE `id` = ?", (week, account_id))
    
    def edit_account_link(self, account_id, link):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `link` = ? WHERE `id` = ?", (link, account_id))
    
    def edit_account_school(self, account_id, school):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `school` = ? WHERE `id` = ?", (school, account_id))
            



    
    def get_chat_id(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT id FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_login(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT login FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_password(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT password FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_day(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT day FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_lesson(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT lesson FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_link(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT link FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_school(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT school FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]



    def add_chat(self, chat_id, login, password, link, school):
        with self.connection:
            return self.cursor.execute('INSERT INTO chats VALUES (?,?,?,?,?,?,?,?)',(chat_id, 0, 0, 0, login, password, link, school))



    def edit_chat_id(self, new_id, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `id` = ? WHERE `id` = ?", (new_id, chat_id))

    def edit_chat_login(self, chat_id, login):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `login` = ? WHERE `id` = ?", (login, chat_id))

    def edit_chat_password(self, chat_id, password):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `password` = ? WHERE `id` = ?", ( password, chat_id))

    def edit_chat_day(self, chat_id, day):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `day` = ? WHERE `id` = ?", (day, chat_id))

    def edit_chat_lesson(self, chat_id, lesson):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `lesson` = ? WHERE `id` = ?", (lesson,chat_id))

    def edit_chat_week(self, chat_id, week):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `week` = ? WHERE `id` = ?", (week, chat_id))
    
    def edit_chat_link(self, chat_id, link):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `link` = ? WHERE `id` = ?", (link, chat_id))
    
    def edit_chat_school(self, chat_id, school):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `school` = ? WHERE `id` = ?", (school, chat_id))
            


