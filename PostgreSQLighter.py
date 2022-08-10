import psycopg2
from settings import DATABASE_URL


class SQLighter:
    def __init__(self, db):
        # Подключаемся к бд
        self.connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students ( 
                id INT,
                login TEXT,
                password TEXT,
                studentId INT,
                isFirstLogin INT,
                week INT,
                day INT,
                lesson INT,
                correctData INT,
                link TEXT,
                school TEXT,
                class TEXT,
                mark_notification INT,
                announcements_notification INT,
                schedule_notification INT,
                homework_notification INT,
                old_mark TEXT,
                old_announcements TEXT,
                correction_lesson TEXT,
                correction_mark INT,
                isAdmin INT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS schedule ( 
                school TEXT,
                class TEXT,
                day TEXT,
                photo TEXT
                )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS chats ( 
                id INT,
                week INT,
                day INT,
                lesson INT,
                login TEXT,
                password TEXT,
                studentId INT,
                link TEXT,
                school TEXT,
                class TEXT,
                mark_notification INT,
                announcements_notification INT,
                schedule_notification INT,
                homework_notification INT,
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
            self.cursor.execute('SELECT homework FROM homeworks WHERE school = %s AND class = %s AND lesson = %s', (school, clas, lesson))
            return self.cursor.fetchone()[0]
    
    def get_lessons_with_homework(self, school, clas):
        with self.connection:
            self.cursor.execute('SELECT lesson FROM homeworks WHERE school = %s AND class = %s', (school, clas))
            return self.cursor.fetchall()
    
    def get_upd_date(self, school, clas, lesson):
        with self.connection:
            self.cursor.execute('SELECT upd_date FROM homeworks WHERE school = %s AND class = %s AND lesson = %s', (school, clas, lesson))
            return self.cursor.fetchone()[0]


    def add_lesson_with_homework(self, lesson, school, clas, homework, upd_date):
        with self.connection:
            return self.cursor.execute('INSERT INTO homeworks VALUES (%s,%s,%s,%s,%s)',(lesson, school, clas, homework, upd_date))


    def edit_homework(self, school, clas, lesson, homework):
        with self.connection:
            return self.cursor.execute("UPDATE homeworks SET homework = %s WHERE school = %s AND class = %s AND lesson = %s", (homework, school, clas, lesson))

    def edit_upd_date(self, school, clas, lesson, upd_date):
        with self.connection:
            return self.cursor.execute("UPDATE homeworks SET upd_date = %s WHERE school = %s AND class = %s AND lesson = %s", (upd_date, school, clas, lesson))




    def get_schedule(self, school, clas, day):
        with self.connection:
            self.cursor.execute('SELECT photo FROM schedule WHERE day = %s AND class = %s AND school = %s', (day, clas, school))
            return self.cursor.fetchone()[0]

    def edit_schedule(self, school, clas, day, photo):
        with self.connection:
            return self.cursor.execute("UPDATE schedule SET photo = %s WHERE day = %s AND class = %s AND school = %s", (photo, day, clas, school))

    def add_schedule(self, school, clas, day, photo):
        with self.connection:
            return self.cursor.execute('INSERT INTO schedule VALUES (%s,%s,%s,%s)',(school, clas, day, photo))





    
    def get_account_id(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT id FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_login(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT login FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_password(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT password FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_studentId(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT studentId FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_isFirstLogin(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT isFirstLogin FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()

    def get_account_day(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT day FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_lesson(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT lesson FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]
    
    def get_account_correctData(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT correctData FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_link(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT link FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_school(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT school FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_class(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT class FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]
    
    def get_account_mark_notification(self, account_id):
            with self.connection:
                self.cursor.execute('SELECT mark_notification FROM students WHERE id = %s', (account_id,))
            return bool(self.cursor.fetchone()[0])

    def get_account_announcements_notification(self, account_id):
            with self.connection:
                self.cursor.execute('SELECT announcements_notification FROM students WHERE id = %s', (account_id,))
            return bool(self.cursor.fetchone()[0])

    def get_account_schedule_notification(self, account_id):
            with self.connection:
                self.cursor.execute('SELECT schedule_notification FROM students WHERE id = %s', (account_id,))
            return bool(self.cursor.fetchone()[0])

    def get_account_homework_notification(self, account_id):
            with self.connection:
                self.cursor.execute('SELECT homework_notification FROM students WHERE id = %s', (account_id,))
            return bool(self.cursor.fetchone()[0])

    def get_account_old_mark(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT old_mark FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_old_announcements(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT old_announcements FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]
    
    def get_account_correction_lesson(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT correction_lesson FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_correction_mark(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT correction_mark FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_isAdmin(self, account_id):
        with self.connection:
            self.cursor.execute('SELECT isAdmin FROM students WHERE id = %s', (account_id,))
            return self.cursor.fetchone()[0]

    def get_account_any_with_filter(self, column, filter_name, filter_value):
        with self.connection:
            self.cursor.execute(f'SELECT {column} FROM students WHERE {filter_name} = %s', (filter_value,))
            return self.cursor.fetchall()

    def get_account_all(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM students')
            return self.cursor.fetchall()

    def get_account_all_admins(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM students WHERE isAdmin = 1')
            return self.cursor.fetchall()

    def get_account_all_with_id(self, id):
        with self.connection:
            self.cursor.execute('SELECT * FROM students WHERE id = %s', (id,))
            return self.cursor.fetchall()


    def add_user(self, user_id, login, password, link, school, clas, studentId):
        with self.connection:
            return self.cursor.execute('INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(user_id, login, password, studentId, 1, 0, 0, 0, 0, link, school, clas, 0, 0, 0, 0, '[]','[]',0,0,0))



    def edit_account_id(self, new_id, account_id):
        with self.connection:
            return self.cursor.execute("UPDATE students SET id = %s WHERE id = %s", (new_id, account_id))

    def edit_account_login(self, account_id, login):
        with self.connection:
            return self.cursor.execute("UPDATE students SET login = %s WHERE id = %s", (login, account_id))

    def edit_account_password(self, account_id, password):
        with self.connection:
            return self.cursor.execute("UPDATE students SET password = %s WHERE id = %s", (password, account_id))

    def edit_account_studentId(self, account_id, studentId):
        with self.connection:
            return self.cursor.execute("UPDATE students SET studentId = %s WHERE id = %s", (studentId, account_id))

    def edit_account_isFirstLogin(self, account_id, isFirstLogin):
        with self.connection:
            return self.cursor.execute("UPDATE students SET isFirstLogin = %s WHERE id = %s", (isFirstLogin, account_id))

    def edit_account_day(self, account_id, day):
        with self.connection:
            return self.cursor.execute("UPDATE students SET day = %s WHERE id = %s", (day, account_id))

    def edit_account_lesson(self, account_id, lesson):
        with self.connection:
            return self.cursor.execute("UPDATE students SET lesson = %s WHERE id = %s", (lesson,account_id))

    def edit_account_correctData(self, account_id, correctData):
        with self.connection:
            return self.cursor.execute("UPDATE students SET correctData = %s WHERE id = %s", (correctData, account_id))
    
    def edit_account_week(self, account_id, week):
        with self.connection:
            return self.cursor.execute("UPDATE students SET week = %s WHERE id = %s", (week, account_id))
    
    def edit_account_link(self, account_id, link):
        with self.connection:
            return self.cursor.execute("UPDATE students SET link = %s WHERE id = %s", (link, account_id))
    
    def edit_account_school(self, account_id, school):
        with self.connection:
            return self.cursor.execute("UPDATE students SET school = %s WHERE id = %s", (school, account_id))
    
    def edit_account_class(self, account_id, account_class):
        with self.connection:
            return self.cursor.execute("UPDATE students SET class = %s WHERE id = %s", (account_class, account_id))

    def edit_account_mark_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET mark_notification = %s WHERE id = %s", (value, account_id))

    def edit_account_announcements_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET announcements_notification = %s WHERE id = %s", (value, account_id))

    def edit_account_schedule_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET schedule_notification = %s WHERE id = %s", (value, account_id))

    def edit_account_homework_notification(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET homework_notification = %s WHERE id = %s", (value, account_id))

    def edit_account_old_mark(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET old_mark = %s WHERE id = %s", (str(value), account_id))

    def edit_account_old_announcements(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET old_announcements = %s WHERE id = %s", (str(value), account_id))
      
    def edit_account_correction_lesson(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET correction_lesson = %s WHERE id = %s", (str(value), account_id))
            
    def edit_account_correction_mark(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET correction_mark = %s WHERE id = %s", (str(value), account_id))
    
    def edit_account_isAdmin(self, account_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE students SET isAdmin = %s WHERE id = %s", (str(value), account_id))




    
    def get_chat_id(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT id FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_login(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT login FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_password(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT password FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_studentId(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT studentId FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_day(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT day FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_lesson(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT lesson FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_link(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT link FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_school(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT school FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_class(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT class FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_mark_notification(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT mark_notification FROM chats WHERE id = %s', (chat_id,))
            return bool(self.cursor.fetchone()[0])

    def get_chat_announcements_notification(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT announcements_notification FROM chats WHERE id = %s', (chat_id,))
            return bool(self.cursor.fetchone()[0])

    def get_chat_schedule_notification(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT schedule_notification FROM chats WHERE id = %s', (chat_id,))
            return bool(self.cursor.fetchone()[0])

    def get_chat_homework_notification(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT homework_notification FROM chats WHERE id = %s', (chat_id,))
            return bool(self.cursor.fetchone()[0])

    def get_chat_old_mark(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT old_mark FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_old_announcements(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT old_announcements FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_correction_lesson(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT correction_lesson FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_correction_mark(self, chat_id):
        with self.connection:
            self.cursor.execute('SELECT correction_mark FROM chats WHERE id = %s', (chat_id,))
            return self.cursor.fetchone()[0]

    def get_chat_any_with_filter(self, column, filter_name, filter_value):
        with self.connection:
            self.cursor.execute(f'SELECT {column} FROM chats WHERE {filter_name} = %s', (filter_value,))
            return self.cursor.fetchall()



    def add_chat(self, chat_id, login, password, link, school, clas, studentId):
        with self.connection:
            return self.cursor.execute('INSERT INTO chats VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(chat_id, 0, 0, 0, login, password,studentId, link, school, clas, 0, 0, 0, 0,'[]','[]',0,0))



    def edit_chat_id(self, new_id, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET id = %s WHERE id = %s", (new_id, chat_id))

    def edit_chat_login(self, chat_id, login):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET login = %s WHERE id = %s", (login, chat_id))

    def edit_chat_password(self, chat_id, password):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET password = %s WHERE id = %s", (password, chat_id))

    def edit_chat_studentId(self, chat_id, studentId):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET studentId = %s WHERE id = %s", (studentId, chat_id))

    def edit_chat_day(self, chat_id, day):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET day = %s WHERE id = %s", (day, chat_id))

    def edit_chat_lesson(self, chat_id, lesson):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET lesson = %s WHERE id = %s", (lesson,chat_id))

    def edit_chat_week(self, chat_id, week):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET week = %s WHERE id = %s", (week, chat_id))
    
    def edit_chat_link(self, chat_id, link):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET link = %s WHERE id = %s", (link, chat_id))
    
    def edit_chat_school(self, chat_id, school):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET school = %s WHERE id = %s", (school, chat_id))
    
    def edit_chat_class(self, chat_id, clas):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET class = %s WHERE id = %s", (clas, chat_id))
    
    def edit_chat_mark_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET mark_notification = %s WHERE id = %s", (value, chat_id))

    def edit_chat_announcements_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET announcements_notification = %s WHERE id = %s", (value, chat_id))

    def edit_chat_schedule_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET schedule_notification = %s WHERE id = %s", (value, chat_id))

    def edit_chat_homework_notification(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET homework_notification = %s WHERE id = %s", (value, chat_id))

    def edit_chat_old_mark(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET old_mark = %s WHERE id = %s", (str(value), chat_id))

    def edit_chat_old_announcements(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET old_announcements = %s WHERE id = %s", (str(value), chat_id))

    def edit_chat_correction_lesson(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET correction_lesson = %s WHERE id = %s", (str(value), chat_id))

    def edit_chat_correction_mark(self, chat_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET correction_mark = %s WHERE id = %s", (str(value), chat_id))



    def get_accounts_mark_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE mark_notification = %s", (1,))
            return self.cursor.fetchall()

    def get_chats_mark_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM chats WHERE mark_notification = %s", (1,))
            return self.cursor.fetchall()


    def get_accounts_announcements_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE announcements_notification = %s", (1,))
            return self.cursor.fetchall()

    def get_chats_announcements_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM chats WHERE announcements_notification = %s", (1,))
            return self.cursor.fetchall()


    def get_accounts_schedule_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE schedule_notification = %s", (1,))
            return self.cursor.fetchall()

    def get_chats_schedule_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM chats WHERE schedule_notification = %s", (1,))
            return self.cursor.fetchall()


    def get_accounts_homework_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE homework_notification = %s", (1,))
            return self.cursor.fetchall()

    def get_chats_homework_notification(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM chats WHERE homework_notification = %s", (1,))
            return self.cursor.fetchall()


db = SQLighter('')