from flask import Flask, redirect, url_for, session, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/new_user   ')
def new_user():
    return render_template('new_user.html')


@app.route('/search_user', methods=['POST'])
def search_user():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    # Отримання даних з форми
    login = request.form['newlogin']
    password = request.form['newpassword']

    # Перевірка наявності логіну в базі
    cursor.execute('SELECT * FROM user WHERE login = ?', (login,))
    user = cursor.fetchone()

    if user:
        # Логін вже існує
        # Тут можна вивести повідомлення про помилку користувачу
        return 'Логін вже зайнятий'+new_user()
    else:
        # Додавання нового користувача
        cursor.execute('INSERT INTO user (login, password) VALUES (?, ?)', (login, password))
        conn.commit()
        return first()
    conn.close()


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        with sqlite3.connect('blog.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            user = cursor.execute('SELECT * FROM user WHERE login = ? AND password = ?', (login, password)).fetchone()

        if user is not None:
            return first()
        else:
            return 'Неправильний логін або пароль'+index()
    

if __name__ == '__main__':
    app.run(debug=True)