import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.result = None
        self.titles = None
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.get_inf)
        self.openw2.clicked.connect(self.open_w2)
        self.w2 = None
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.current_id = None

    def get_inf(self):
        self.result = self.cur.execute("""SELECT * FROM coffeeeeee""").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_w2(self):
        try:
            self.current_id = self.tableWidget.item((
                self.tableWidget.selectedItems()[0].row()), 0).text()
        except IndexError:
            self.current_id = None
        self.w2 = Window2(self.current_id)
        self.w2.show()


class Window2(QWidget):
    def __init__(self, c_id):
        super(Window2, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.do_add.clicked.connect(self.add_inf)
        self.do_edit.clicked.connect(self.edit_inf)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.c_id = c_id
        if self.c_id:
            self.current = self.cur.execute("""SELECT * from coffeeeeee
            WHERE ID = ?""", (self.c_id,))
            n, name, degree, hummer, description, cost, size = list(self.current)[0]
            self.edit1.setText(name)
            self.edit2.setText(str(degree))
            self.edit3.setText(hummer)
            self.edit4.setText(description)
            self.edit5.setText(str(cost))
            self.edit6.setText(str(size))

    def add_inf(self):
        name, degree, hummer, description, cost, size = self.add1.text(), self.add2.text(), \
                                                        self.add3.text(), self.add4.text(), \
                                                        self.add5.text(), self.add6.text()
        self.cur.execute('''INSERT INTO coffeeeeee (Name_of_the_variety, Degree_of_roasting, 
        Crushed, Taste_description, Cost, Packing_size) VALUES(?,?,?,?,?,?)''',
                         (name, degree, hummer, description, cost, size))
        self.con.commit()
        self.add1.clear()
        self.add2.clear()
        self.add3.clear()
        self.add4.clear()
        self.add5.clear()
        self.add6.clear()

    def edit_inf(self):
        self.cur.execute("""UPDATE coffeeeeee
        SET Name_of_the_variety = ?, Degree_of_roasting = ?, 
        Crushed = ?, Taste_description = ?, Cost = ?, Packing_size = ?
        WHERE ID = ?""", (self.edit1.text(), self.edit2.text(),
                          self.edit3.text(), self.edit4.text(),
                          self.edit5.text(), self.edit6.text(), self.c_id))
        self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Window()
    w1.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
