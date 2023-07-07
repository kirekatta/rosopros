import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget
from check_db import *

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main.ui", self)
        self.pushButton.clicked.connect(self.restart)

    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)




class AuthForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("auth.ui", self)
        self.pushButton.clicked.connect(self.reg)
        self.ui.pushButton_2.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)
        self.mainForm = MainForm()

    # Проверка правильности ввода
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper


    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)


    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_login(name, passw, self.mainForm, self.ui)


    @check_input
    def reg(self):
        login = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        surname = self.ui.lineEdit_4.text()
        patronymic = self.ui.lineEdit_5.text()
        self.check_db.thr_register(login, passw, name, surname, patronymic)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = AuthForm()
    mywin.show()
    sys.exit(app.exec_())