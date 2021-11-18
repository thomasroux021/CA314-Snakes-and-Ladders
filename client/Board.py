from typing import List
from Constant import *
from Utils import *
import pygame

from Square import *


class Board:
    def __init__(self, gameDisplay):
        # board List
        self.board: List[List[Square]] = []
        self.gameDisplay = gameDisplay
        isLeftRight = True
        for i in range(0, 10):
            temp = []
            for j in range(0, 10):
                if (not isLeftRight):
                    x = (9 - j) * 60
                else:
                    x = j * 60
                y = i * 60
                temp.append(Square(x, y, 100 - (i * 10 + j), self.gameDisplay))
            if (not isLeftRight):
                temp.reverse()
            self.board.append(temp)
            isLeftRight = not isLeftRight

    def get_square(self, position):
        for i in range(0, 10):
            for j in range(0, 10):
                if self.board[i][j].pos == position:
                    return self.board[i][j]

    def draw(self):
        for i in self.board:
            for j in i:
                if int(j.pos) % 2 == 0:
                    colorb = Constant.boardclr
                else:
                    colorb = Constant.boardclr2
                j.draw(colorb)

                
