from PyQt5 import QtCore, QtGui, QtWidgets
from handler.db_handler import *
import re


class CheckThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, passw, mainForm, authForm):
        if not re.match(r'^[a-zA-Z0-9]+$', name):
            self.mysignal.emit("Логин должен содержать только латинские буквы и цифры.")
        else:
            login(name, passw, self.mysignal, mainForm, authForm)

    def thr_register(self, login, passw, name, surname, patronymic):
        if not re.match(r'^[a-zA-Z0-9]+$', login):
            self.mysignal.emit("Логин должен содержать только латинские буквы и цифры.")
        else:
            if not re.match(r'^[а-яА-Я]+$', name) and not re.match(r'^[а-яА-Я]+$', surname) and \
                    not re.match(r'^[а-яА-Я]+$', patronymic) and name != 0 and surname != 0 and patronymic != 0 and \
                    (' ' in name) and (' ' in surname) and (' ' in patronymic):
                self.mysignal.emit("Поля ФИО должны быть все обязательно заполнены и содержать только русские символы.")
            else:
                register(login, passw, name, surname, patronymic, self.mysignal)