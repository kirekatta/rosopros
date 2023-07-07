import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash



def login(login, passw, signal, mainForm, authForm):
    con = sqlite3.connect('rosopros.db')
    cur = con.cursor()

    # Проверяем есть ли такой пользователь
    cur.execute(f'SELECT * FROM users WHERE login="{login}";')
    value = cur.fetchall()
    
    if value != [] and check_password_hash(value[0][2], passw):
        signal.emit('Успешная авторизация!')
        mainForm.show()
        authForm.hide()
    else:
        signal.emit('Проверьте правильность ввода данных!')

    cur.close()
    con.close()


def register(login, passw, name, surname, patronymic, signal):
    con = sqlite3.connect('rosopros.db')
    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE login="{login}";')
    value = cur.fetchall()

    if value != []:
        signal.emit('Такой логин уже используется!')

    elif value == []:
        cur.execute(f"INSERT INTO users (login, password, name, surname, patronymic) VALUES ('{login}', '{generate_password_hash(passw)}', '{name}', '{surname}', '{patronymic}')")
        cur.execute(f"INSERT INTO role (login, role) VALUES ('{login}', 'user')")
        signal.emit('Вы успешно зарегистрированы!')
        con.commit()

    cur.close()
    con.close()