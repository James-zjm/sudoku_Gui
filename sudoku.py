# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sudoku_face import Ui_Sudoku
import genarate_soduku
import sys

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Face(QMainWindow):
    level = 1
    map = [[0 for i in range(9)]for j in range(9)]
    isyuan = [[0 for i in range(9)]for j in range(9)]
    shu_base = [[0 for i in range(9)] for j in range(9)]
    heng_base = [[0 for i in range(9)] for j in range(9)]
    kuai_base = [[0 for i in range(9)] for j in range(9)]

    def __init__(self, parent=None):
        #QMainWindow.__init__(self, parent)
        super(Face, self).__init__(parent)

        self.ui = Ui_Sudoku()

        self.ui.setupUi(self)
        # self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(self.width(), self.height())

        self.ui.pushButton.setText('START')
        self.ui.lineEdit_2.setText("EASY")
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_2.setStyleSheet(
            "background-color: transparent;")
        self.ui.lineEdit.setText("0")
        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit.setStyleSheet(
            "background-color: transparent;")
        # 设置九宫格方块
        self.show_num = []
        for i in range(9):
            flags = []
            for j in range(9):
                flag = QLineEdit(self.ui.centralwidget)
                flags.append(flag)
                flags[j].setGeometry(QRect(j * 45, i * 45, 44, 44))
                flags[j].setMaxLength(1)
                flags[j].setObjectName((str((i + 1) * (j + 1))))
                flags[j].setText("")
                flags[j].setReadOnly(True)
                flags[j].setFont(QFont("Timers", 31, QFont.Bold))  # 设置字体大小
                flags[j].setStyleSheet(
                    "background-color: #66cccc;")  # 背景颜色
                flags[j].setFocus()
                flags[j].connect(flags[j], SIGNAL(
                    'textChanged(QString)'), self.working)
            self.show_num.append(flags)

        # 链接按钮动作
        self.ui.pushButton.clicked.connect(self.start_game)

        # 菜单功能
        self.ui.actionEasy.connect(
            self.ui.actionEasy, SIGNAL('triggered()'), self.change_easy)
        self.ui.actionMiddle.connect(
            self.ui.actionMiddle, SIGNAL('triggered()'), self.change_middle)
        self.ui.actionHard.connect(
            self.ui.actionHard, SIGNAL('triggered()'), self.change_hard)

    def start_game(self):
        self.ui.pushButton.setText('RESTART')
        self.sudoku = genarate_soduku.Genarate(self.level)  # 获取数独
        for i in range(9):  # 填数
            for j in range(9):
                if self.sudoku.sudoku[i][j] == 0:  # 无数
                    self.show_num[i][j].setReadOnly(False)
                    self.show_num[i][j].setText("")
                    self.show_num[i][j].setStyleSheet(
                        "background-color: white;")
                else:
                    self.isyuan[i][j] = 1
                    self.show_num[i][j].setText(str(self.sudoku.sudoku[i][j]))
                    self.show_num[i][j].setStyleSheet(
                        "background-color: green;"
                        "color:white"
                    )
        self.hoels = self.sudoku.hoels
        self.ui.lineEdit.setText(str(self.hoels))  # 剩余的空格数
        self.ui.pushButton.clicked.connect(self.restart_game)

    def restart_game(self):
        self.ui.pushButton.setText('RESTART')
        self.isyuan = [[0 for i in range(9)]for j in range(9)]
        self.map = [[0 for i in range(9)]for j in range(9)]
        self.start_game()

    def working(self, text):
        sender = self.sender()
        for row in range(9):  # 判断改变数字的位置
            try:
                col = self.show_num[row].index(sender)
            except ValueError:
                continue
            else:
                break
        try:
            self.map[row][col] = int(text)
        except ValueError:
            self.map[row][col] = 0
        if self.map[row][col] == 0:  # 无数
            self.hoels = self.hoels+1
            self.ui.lineEdit.setText(str(self.hoels))
            self.show_num[row][col].setStyleSheet(
                "background-color: white;")
        else:
            self.hoels = self.hoels - 1
            self.ui.lineEdit.setText(str(self.hoels))
            self.check_value(row, col)

    def check_value(self, row, col):
        b_r = int(row/3)*3
        b_c = int(col/3)*3
        # 行
        for i in range(1, 10):
            sum = 0
            record = -1
            for j in range(9):
                if self.map[row][j] == i:
                    sum = sum + 1
                    if sum == 1:
                        record = j  # 有一个
                    elif sum == 2:  # 有两个重复数字
                        if self.isyuan[row][record] != 1:  # 是否为题目数字
                            self.heng_base[row][record] = 1
                            self.show_num[row][record].setStyleSheet(
                                "background-color: red;")
                        record = -1
                        if self.isyuan[row][j] != 1:
                            self.heng_base[row][j] = 1
                            self.show_num[row][j].setStyleSheet(
                                "background-color: red;")
                    elif sum > 2:  # 有更多
                        if self.isyuan[row][j] != 1:
                            self.heng_base[row][j] = 1
                            self.show_num[row][j].setStyleSheet(
                                "background-color: red;")
            if (record != -1):  # 无重复
                self.heng_base[row][record] = 0
                # 在其他方面没有错误
                if (self.shu_base[row][record] == 0) & (self.kuai_base[row][record] == 0):
                    if self.isyuan[row][record] != 1:
                        self.show_num[row][record].setStyleSheet(
                            "background-color: green;")
        # 列

        for i in range(1, 10):
            sum = 0
            record = -1
            for j in range(9):
                if self.map[j][col] == i:
                    sum = sum + 1
                    if sum == 1:
                        record = j
                    elif sum == 2:
                        if self.isyuan[record][col] != 1:
                            self.shu_base[record][col] = 1
                            self.show_num[record][col].setStyleSheet(
                                "background-color: red;")
                        record = -1
                        if self.isyuan[j][col] != 1:
                            self.shu_base[j][col] = 1
                            self.show_num[j][col].setStyleSheet(
                                "background-color: red;")
                    elif sum > 2:
                        if self.isyuan[j][col] != 1:
                            self.shu_base[j][col] = 1
                            self.show_num[j][col].setStyleSheet(
                                "background-color: red;")
            if (record != -1):
                self.shu_base[record][col] = 0
                if (self.heng_base[record][col] == 0) & (self.kuai_base[record][col] == 0):
                    if self.isyuan[record][col] != 1:
                        self.show_num[record][col].setStyleSheet(
                            "background-color: green;")
        # 九宫格
        for i in range(1, 10):
            sum = 0
            record = [-1, -1]
            for jrow in range(3):
                for jcol in range(3):
                    if self.map[jrow+b_r][jcol+b_c] == i:
                        sum = sum + 1
                        if sum == 1:
                            record = [jrow+b_r, jcol+b_c]
                        elif sum == 2:
                            if self.isyuan[record[0]][record[1]] != 1:
                                self.kuai_base[record[0]][record[1]] = 1
                                self.show_num[record[0]][record[1]].setStyleSheet(
                                    "background-color: red;")
                            record = [-1, -1]
                            if self.isyuan[jrow+b_r][jcol + b_c] != 1:
                                self.kuai_base[jrow+b_r][jcol + b_c] = 1
                                self.show_num[jrow+b_r][jcol +
                                                        b_c].setStyleSheet("background-color: red;")
                        elif sum > 2:
                            if self.isyuan[jrow+b_r][jcol + b_c] != 1:
                                self.kuai_base[jrow + b_r][jcol + b_c] = 1
                                self.show_num[jrow+b_r][jcol +
                                                        b_c].setStyleSheet("background-color: red;")
            if (record[0] != -1):
                self.kuai_base[record[0]][record[1]] = 0
                if(self.heng_base[record[0]][record[1]] == 0) & (self.shu_base[record[0]][record[1]] == 0):
                    if self.isyuan[record[0]][record[1]] != 1:
                        self.show_num[record[0]][record[1]].setStyleSheet(
                            "background-color: green;")

    def change_easy(self):
        self.level = 1
        self.ui.lineEdit_2.setText("EASY")
        print self.level

    def change_middle(self):
        self.level = 2
        self.ui.lineEdit_2.setText("MIDDLE")
        print self.level

    def change_hard(self):
        self.level = 3
        self.ui.lineEdit_2.setText("HARD")
        print self.level


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Face()
    myapp.show()
    sys.exit(app.exec_())
