from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
num = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    global num
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        namepass = f"('{name}', '{password}')"

        now = []
        ids = -1
        allid = []

        con = sqlite3.connect('login.db')
        cur = con.cursor()
        result = cur.execute("""SELECT name, password, id FROM user""").fetchall()
        for elem in result:
            name1 = elem[0]
            password1 = elem[1]
            id1 = elem[2]
            allid.append(id1)
            now1 = f"('{name1}', '{password1}')"
            now.append(now1)

        for i in range(len(now)):
            ids += 1
            if str(namepass) == str(now[i]):
                rooms = f'/room/{allid[ids]}'
                num = allid[ids]
                return redirect(rooms)
        return 'Неверный логин или пароль'

    else:
        return render_template('login.html')


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    global num
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User(name=name, password=password)
        now = []

        con = sqlite3.connect('login.db')
        cur = con.cursor()
        result = cur.execute("""SELECT name, id FROM user""").fetchall()
        for elem in result:
            now.append(elem[0])
            ids = elem[1]

        if name in now:
            return 'Имя уже занято'
        else:
            try:
                db.session.add(user)
                db.session.commit()
                rooms = f'/room/{ids + 1}'
                num = ids + 1
                return redirect(rooms)
            except:
                return 'Одно из параметров указано неверно'
    else:
        return render_template('reg.html')


@app.route('/room/<int:id>')
def room(id):
    if id == 105:
        return render_template('room105.html', num=num)
    if id == 308:
        return render_template('room308.html', num=num)
    else:
        return render_template('rooms.html', num=num)


@app.route('/room/<int:num>/screen')
def screen(num):
    return render_template('screen.html')


@app.route('/room/105/screen')
def screen105():
    return render_template('screen105.html')


@app.route('/room/308/screen')
def screen308():
    return render_template('screen308.html')


@app.route('/room/<int:num>/horoscope')
def galack(num):
    return render_template('galack.html')

@app.route('/room/105/horoscope')
def galack105():
    return render_template('galack105.html')


@app.route('/room/308/horoscope')
def galack308():
    return render_template('galack308.html')


if __name__ == '__main__':
    app.run(debug=True)