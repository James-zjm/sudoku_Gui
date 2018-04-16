# coding:utf-8
# python2.7

import solve_all_sudoku
import create_sudoku
import random
from copy import deepcopy


class Genarate():
    hoels = 0
    lev = -1
    temp = [[0 for i in range(9)]for j in range(9)]
    sudoku = [[0 for i in range(9)]for j in range(9)]

    def __init__(self, level):
        num = random.randint(0, 100)  # 从一百个中随机挑一个
        sudokus = create_sudoku.Create(100)#生成一百个终局
        self.sudoku = deepcopy(sudokus.sudoku_map[num])
        self.dig_based()
        self.temp = deepcopy(self.sudoku)
        while True:
            self.dig_hole()
            if (self.hoels > 30):
                if (self.lev > level*30):  # 猜测次数0~30位简单，30~60为中等，60~无穷为困难
                    break
                if self.hoels > 30+level*10:  # 30~40空为简单 40~50为中等 50~60为困难
                    break

    def check_repeat(self):  # 查看解是否唯一
        ans = solve_all_sudoku.Solve(self.sudoku)
        ans.calc()
        if ans.count != 1:
            return True
        else:
            self.lev = ans.guess_times
            return False

    def dig_based(self):  # 每个九宫格至少挖两个
        for i in range(3):
            for j in range(3):
                # 每个方格挖两个
                while True:
                    pos = random.randint(0, 8)
                    row = int(pos/3)+i*3
                    col = int(pos % 3)+j*3
                    temp = self.sudoku[row][col]
                    if self.sudoku[row][col] != 0:
                        self.sudoku[row][col] = 0
                        if self.check_repeat():
                            self.sudoku[row][col] = temp
                        else:
                            self.hoels = self.hoels+1
                            break
                while True:
                    pos = random.randint(0, 8)
                    row = int(pos/3)+i*3
                    col = int(pos % 3)+j*3
                    temp = self.sudoku[row][col]
                    if self.sudoku[row][col] != 0:
                        self.sudoku[row][col] = 0
                        if self.check_repeat():
                            self.sudoku[row][col] = temp
                        else:
                            self.hoels = self.hoels+1
                            break

    def dig_hole(self):  # 挖洞
        while True:
            pos = random.randint(0, 80)
            row = int(pos/9)
            col = int(pos % 9)
            temp = self.sudoku[row][col]
            if self.sudoku[row][col] != 0:
                self.sudoku[row][col] = 0
                if self.check_repeat():
                    self.sudoku[row][col] = temp
                else:
                    self.hoels = self.hoels+1
                    break
