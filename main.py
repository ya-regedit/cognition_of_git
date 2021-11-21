import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.result = None
        self.titles = None
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.get_inf)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

    def get_inf(self):
        self.result = self.cur.execute("""SELECT * FROM coffeeeeee""").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Window()
    w1.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
