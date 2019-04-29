from flask import Flask, session, redirect, render_template, flash, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, Book, genre_Book
from forms import LoginForm, RegisterForm, AddbookForm, SearchPriceForm, SearchgenreForm, AddgenreForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
Book(db.get_connection()).init_table()
genre_Book(db.get_connection()).init_table()


@app.route('/redak/<int:book_id>', methods=['POST', 'GET'])
def redak(book_id=1):
    # редактирование записей кидаем на главную
    p = book_id
    if request.method == 'GET':
        return render_template('text.html')
    elif request.method == 'POST':
        Book(db.get_connection()).redak(p, request.form['about'].strip())
        books = Book(db.get_connection()).get_all()
        return render_template('Book_admin.html', username=session['username'], title='Просмотр базы', books=books)


@app.route('/')
@app.route('/index')
def index():
    # Главная страница Основная страница сайта, либо редирект на авторизацю
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # если обычный пользователь, то его на свою
    books = Book(db.get_connection()).get_all()
    return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Страница авторизации переадресация на главную, либо вывод формы авторизации
    form = LoginForm()
    if form.validate_on_submit():  # ввели логин и пароль
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        # проверяем наличие пользователя в БД и совпадение пароля
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password) or True:
            session['username'] = user_name  # запоминаем в сессии имя пользователя и кидаем на главную
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    # Выход из системы
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Форма регистрации
    form = RegisterForm()
    if form.validate_on_submit():
        # создать пользователя
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            # редирект на главную страницу
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


"""Работа с Книгами"""


@app.route('/Book_admin', methods=['GET'])
def Book_admin():
    # Вывод всей информации об всех книгах информация для авторизованного пользователя
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # если обычный пользователь, то его на свою
    books = Book(db.get_connection()).get_all()
    return render_template('Book_admin.html',
                           username=session['username'],
                           title='Просмотр книг',
                           books=books)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Добавление книги
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        return redirect('index')
    form = AddbookForm()
    available_genres = [(i[0], i[1]) for i in genre_Book(db.get_connection()).get_all()]
    form.genre_id.choices = available_genres
    if form.validate_on_submit():
        # создать книгу
        books = Book(db.get_connection())
        books.insert(model=form.model.data,
                     price=form.price.data,
                     power=form.power.data,
                     color=form.color.data,
                     genre=form.genre_id.data)
        # редирект на главную страницу
        return redirect(url_for('Book_admin'))
    return render_template("add_book.html", title='Добавление книги', form=form)


@app.route('/book/<int:book_id>', methods=['GET'])
def book(book_id):
    # Просмотр книги информация для авторизованного пользователя
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если  админ, то его на спец страницу с возможностью менять описание
    book = Book(db.get_connection()).get(book_id)
    genre = genre_Book(db.get_connection()).get(book[5])
    if session['username'] == 'admin':
        # странца админа с кнопкой редактирования
        return render_template('book_infoad.html',
                               username=session['username'],
                               title='Просмотр книги',
                               book=book,
                               genre=genre[1])
    # иначе выдаем информацию

    return render_template('book_info.html',
                           username=session['username'],
                           title='Просмотр книги',
                           book=book,
                           genre=genre[1])


@app.route('/bookdel/<int:book_id>', methods=['GET'])
def bookdel(book_id):
    # Удаление книги
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если  админ, то его на спец страницу с возможностью менять описание
    Book(db.get_connection()).delete(book_id)
    if session['username'] == 'admin':
        books = Book(db.get_connection()).get_all()
        return render_template('Book_admin.html',
                               username=session['username'],
                               title='Просмотр книг',
                               books=books)
    # иначе выдаем информацию
    books = Book(db.get_connection()).get_all()
    return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    # Запрос книг, удовлетворяющих определенной цене
    form = SearchPriceForm()
    if form.validate_on_submit():
        # получить все книги по определенной цене
        books = Book(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        # редирект на страницу с результатами
        books = sorted(books, key=lambda x: x[1])
        return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_mo', methods=['GET'])
def search_mo():
    # Запрос книг, удовлетворяющих определенной цене
    # получить все книги по определенной цене
    books = Book(db.get_connection()).get_all()
    # редирект на страницу с результатами
    books = sorted(books, key=lambda x: x[3])
    return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)


@app.route('/rating/<int:book_id>', methods=['GET', 'POST'])
def rating(book_id):
    # Запрос книг, продающихся в определенном жанре
    form = SearchgenreForm()
    form.genre_id.choices = [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    if form.validate_on_submit():
        #
        if form.genre_id.data != '0':
            Book(db.get_connection()).sred(book_id, form.genre_id.data)
        # редирект на главную страницу
        books = Book(db.get_connection()).get_all()
        return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)
    return render_template("search_genre.html", title='Подбор по цене', form=form)


@app.route('/search_genre', methods=['GET', 'POST'])
def search_genre():
    # Запрос книг, продающихся в определенном жанре
    form = SearchgenreForm()
    available_genres = [(i[0], i[1]) for i in genre_Book(db.get_connection()).get_all()]
    form.genre_id.choices = available_genres
    if form.validate_on_submit():
        #
        books = Book(db.get_connection()).get_by_genre(form.genre_id.data)
        # редирект на главную страницу
        return render_template('book_user.html', username=session['username'], title='Просмотр базы', books=books)
    return render_template("search_genre.html", title='Подбор по цене', form=form)


'''Работа с жанром'''


@app.route('/genre_admin', methods=['GET'])
def genre_admin():
    # Вывод всей информации об всех жанрах информация для авторизованного пользователя
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # иначе это админ
    genres = genre_Book(db.get_connection()).get_all()
    return render_template('genre_admin.html',
                           username=session['username'],
                           title='Просмотр жанров',
                           genres=genres)


@app.route('/genre/<int:genre_id>', methods=['GET'])
def genre(genre_id):
    # Вывод всей информации о жанре нформация для авторизованного пользователя
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # иначе выдаем информацию
    genre = genre_Book(db.get_connection()).get(genre_id)
    return render_template('genre_info.html',
                           username=session['username'],
                           title='Просмотр информации о жанре',
                           genre=genre)


@app.route('/delat/<int:genre_id>', methods=['GET'])
def delat(genre_id):
    # Вывод всей информации о жанре информация для авторизованного пользователя
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # иначе выдаем информацию
    books = Book(db.get_connection()).get_by_genre(genre_id)
    for i in books:
        Book(db.get_connection()).delete(i[2])
    genre_Book(db.get_connection()).delete(genre_id)
    genres = genre_Book(db.get_connection()).get_all()
    return render_template('genre_admin.html',
                           username=session['username'],
                           title='Просмотр жанров',
                           genres=genres)


@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    # Добавление жанра и вывод на экран информации о нем
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        form = AddgenreForm()
        if form.validate_on_submit():
            # создать жанр
            genres = genre_Book(db.get_connection())
            genres.insert(name=form.name.data, infoganre=form.infoganre.data)
            # редирект на главную страницу
            return redirect(url_for('index'))
        return render_template("add_genre.html", title='Добавление жанра', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
