class UsersModel:
    """Сущность пользователей"""

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class genre_Book:
    """Сущность книжных жанров"""

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS genres 
                            (genre_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             infoganre VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, infoganre):
        """Добавление Жанра"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO genres 
                          (name, infoganre) 
                          VALUES (?,?)''',
                       (name, infoganre))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск жанра по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM genres WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, genre_id):
        """Запрос жанра по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM genres WHERE genre_id = ?", (str(genre_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех жанров"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM genres")
        rows = cursor.fetchall()
        return rows

    def delete(self, genre_id):
        """Удаление жанра"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM genres WHERE genre_id = ?''', (str(genre_id)))
        cursor.close()
        self.connection.commit()


class Book:
    """Сущность книг"""

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                            (book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             model VARCHAR(20),
                             price INTEGER,
                             power INTEGER,
                             color VARCHAR(20),
                             genre INTEGER,
                             rating VARCHAR(20),
                             col INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, model, price, power, color, genre):
        """Добавление книг"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books 
                          (model, price, power, color, genre, rating,col) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (model, str(price), str(power), color, str(genre), '0', '0'))
        cursor.close()
        self.connection.commit()

    def exists(self, model):
        """Поиск книг по модели"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE model = ?",
                       model)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, book_id):
        """Поиск книг по id"""
        print(book_id)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (str(book_id),))
        row = cursor.fetchone()
        print(row)
        return row

    def get_all(self):
        """Запрос всех книг"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, book_id, power FROM books")
        rows = cursor.fetchall()
        return rows

    def delete(self, book_id):
        """Удаление книг"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM books WHERE book_id = ?''', (str(book_id),))
        cursor.close()
        self.connection.commit()

    def get_by_price(self, start_price, end_price):
        """Запрос книг по цене"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, book_id FROM books WHERE price >= ? AND price <= ?",
                       (str(start_price), str(end_price)))
        row = cursor.fetchall()
        return row

    def get_by_genre(self, genre_id):
        """Запрос книг по жанру"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, book_id FROM books WHERE genre = ?", (str(genre_id),))
        row = cursor.fetchall()
        return row

    def redak(self, book_id, colorp):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (str(book_id),))
        row = cursor.fetchone()
        print(row)
        id, model, price, power, color, genre, rating, col = row
        color = colorp
        cursor.execute('''DELETE FROM books WHERE book_id = ?''', (str(book_id),))
        cursor.execute('''INSERT INTO books 
                          (model, price, power, color, genre, rating,col) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (model, str(price), str(power), color, str(genre), rating, str(col)))
        cursor.close()
        self.connection.commit()

    def sred(self, book_id, ratin):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (str(book_id),))
        row = cursor.fetchone()
        id, model, price, power, color, genre, rating, col = row
        col += 1
        print(row)
        rating = str(round((float(rating) * (col - 1) + int(ratin)) / col, 15))
        cursor.execute('''DELETE FROM books WHERE book_id = ?''', (str(book_id),))
        cursor.execute('''INSERT INTO books 
                          (model, price, power, color, genre, rating,col) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (model, str(price), str(power), color, str(genre), rating, str(col)))
        cursor.close()
        self.connection.commit()
