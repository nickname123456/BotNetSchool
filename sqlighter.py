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
                school TEXT,
                class TEXT,
                mark_notification BIT,
                announcements_notification BIT,
                schedule_notification BIT,
                old_mark TEXT,
                old_announcements TEXT,
                correction_lesson TEXT,
                correction_mark INT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS schedule ( 
                school TEXT,
                class TEXT,
                day INT,
                photo INT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS chats ( 
                id INT,
                week INT,
                day INT,
                lesson INT,
                login TEXT,
                password TEXT,
                link TEXT,
                school TEXT,
                class TEXT,
                mark_notification BIT,
                announcements_notification BIT,
                schedule_notification BIT,
                old_mark TEXT,
                old_announcements TEXT,
                correction_lesson TEXT,
                correction_mark INT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS homeworks ( 
                lesson TEXT,
                school TEXT,
                class TEXT,
                homework TEXT,
                upd_date TEXT
                )""")

    

    def commit(self):
        self.connection.commit()




    def get_homework(self, school, clas, lesson):
        with self.connection:
            return self.cursor.execute('SELECT homework FROM `homeworks` WHERE `school` = ? AND `class` = ? AND `lesson` = ?', (school, clas, lesson)).fetchone()[0]
    
    def get_upd_date(self, school, clas, lesson):
        with self.connection:
            return self.cursor.execute('SELECT upd_date FROM `homeworks` WHERE `school` = ? AND `class` = ? AND `lesson` = ?', (school, clas, lesson)).fetchone()[0]


    def edit_homework(self, school, clas, lesson, homework):
        with self.connection:
            return self.cursor.execute("UPDATE `homeworks` SET `homework` = ? WHERE `school` = ? AND `class` = ? AND `lesson` = ?", (homework, school, clas, lesson))

    def edit_upd_date(self, school, clas, lesson, upd_date):
        with self.connection:
            return self.cursor.execute("UPDATE `homeworks` SET `upd_date` = ? WHERE `school` = ? AND `class` = ? AND `lesson` = ?", (upd_date, school, clas, lesson))




    def get_schedule(self, school, clas, day):
        with self.connection:
            return self.cursor.execute('SELECT photo FROM `schedule` WHERE `day` = ? AND `class` = ? AND `school` = ?', (day, clas, school)).fetchone()
    
    def edit_schedule(self, school, clas, day, photo):
        with self.connection:
            return self.cursor.execute("UPDATE `schedule` SET `photo` = ? WHERE `day` = ? AND `class` = ? AND `school` = ?", (photo, day, clas, school))

    def add_schedule(self, school, clas, day, photo):
        with self.connection:
            return self.cursor.execute('INSERT INTO EXISTS VALUES (?,?,?,?)',(school, clas, day, photo))





    
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

    def get_account_class(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT class FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]
    
    def get_account_mark_notification(self, account_id):
            with self.connection:
                return bool(self.cursor.execute('SELECT mark_notification FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0])

    def get_account_announcements_notification(self, account_id):
            with self.connection:
                return bool(self.cursor.execute('SELECT announcements_notification FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0])

    def get_account_schedule_notification(self, account_id):
            with self.connection:
                return bool(self.cursor.execute('SELECT schedule_notification FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0])

    def get_account_old_mark(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT old_mark FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_old_announcements(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT old_announcements FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]
    
    def get_account_correction_lesson(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT correction_lesson FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]

    def get_account_correction_mark(self, account_id):
        with self.connection:
            return self.cursor.execute('SELECT correction_mark FROM `students` WHERE `id` = ?', (account_id,)).fetchone()[0]



    def add_user(self, user_id, login, password, link, school, clas):
        with self.connection:
            return self.cursor.execute('INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(user_id, login, password, 1, 0, 0, 0, 0, link, school, clas, 0, 0, 0, '[]','[]',0,0))



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
    
    def edit_account_class(self, account_id, account_class):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `class` = ? WHERE `id` = ?", (account_class, account_id))

    def edit_account_mark_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `mark_notification` = ? WHERE `id` = ?", (value, account_id))

    def edit_account_announcements_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `announcements_notification` = ? WHERE `id` = ?", (value, account_id))

    def edit_account_schedule_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `schedule_notification` = ? WHERE `id` = ?", (value, account_id))

    def edit_account_old_mark(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `old_mark` = ? WHERE `id` = ?", (str(value), account_id))

    def edit_account_old_announcements(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `old_announcements` = ? WHERE `id` = ?", (str(value), account_id))
      
    def edit_account_correction_lesson(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `correction_lesson` = ? WHERE `id` = ?", (str(value), account_id))
            
    def edit_account_correction_mark(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `students` SET `correction_mark` = ? WHERE `id` = ?", (str(value), account_id))




    
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

    def get_chat_class(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT class FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_mark_notification(self, chat_id):
        with self.connection:
            return bool(self.cursor.execute('SELECT mark_notification FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0])

    def get_chat_announcements_notification(self, chat_id):
        with self.connection:
            return bool(self.cursor.execute('SELECT announcements_notification FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0])

    def get_chat_schedule_notification(self, chat_id):
        with self.connection:
            return bool(self.cursor.execute('SELECT schedule_notification FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0])

    def get_chat_old_mark(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT old_mark FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_old_announcements(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT old_announcements FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_correction_lesson(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT correction_lesson FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]

    def get_chat_correction_mark(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT correction_mark FROM `chats` WHERE `id` = ?', (chat_id,)).fetchone()[0]



    def add_chat(self, chat_id, login, password, link, school, clas):
        with self.connection:
            return self.cursor.execute('INSERT INTO chats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(chat_id, 0, 0, 0, login, password, link, school, clas, 0, 0, 0,'[]','[]',0,0))



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
    
    def edit_chat_class(self, chat_id, clas):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `class` = ? WHERE `id` = ?", (clas, chat_id))
    
    def edit_chat_mark_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `mark_notification` = ? WHERE `id` = ?", (value, chat_id))

    def edit_chat_announcements_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `announcements_notification` = ? WHERE `id` = ?", (value, chat_id))

    def edit_chat_schedule_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `schedule_notification` = ? WHERE `id` = ?", (value, chat_id))

    def edit_chat_old_mark(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `old_mark` = ? WHERE `id` = ?", (str(value), chat_id))

    def edit_chat_old_announcements(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `old_announcements` = ? WHERE `id` = ?", (str(value), chat_id))

    def edit_chat_correction_lesson(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `correction_lesson` = ? WHERE `id` = ?", (str(value), chat_id))

    def edit_chat_correction_mark(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `chats` SET `correction_mark` = ? WHERE `id` = ?", (str(value), chat_id))



    def get_accounts_mark_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `students` WHERE `mark_notification` = ?", (1,)).fetchall()

    def get_chats_mark_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `chats` WHERE `mark_notification` = ?", (1,)).fetchall()


    def get_accounts_announcements_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `students` WHERE `announcements_notification` = ?", (1,)).fetchall()

    def get_chats_announcements_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `chats` WHERE `announcements_notification` = ?", (1,)).fetchall()


    def get_accounts_schedule_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `students` WHERE `schedule_notification` = ?", (1,)).fetchall()

    def get_chats_schedule_notification(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `chats` WHERE `schedule_notification` = ?", (1,)).fetchall()
