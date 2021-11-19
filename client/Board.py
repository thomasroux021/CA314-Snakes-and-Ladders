from typing import List
from Constant import *

from Square import Square
from Snake import Snake
from Ladder import Ladder


class Board:
    def __init__(self, gameDisplay):
        # board List
        self.board: List[List[Square]] = []
        self.snakes: List[Snake] = []
        self.ladders: List[Ladder] = []
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

    def event_add_snakes_ladders(self, snakes, ladders):
        for snake in snakes:
            self.snakes.append(Snake(snake[0], snake[1], self.gameDisplay, self))
        for ladder in ladders:
            self.ladders.append(Ladder(ladder[0], ladder[1], self.gameDisplay, self))

    def draw(self):
        for i in self.board:
            for j in i:
                if int(j.pos) % 2 == 0:
                    colorb = Constant.boardclr
                else:
                    colorb = Constant.boardclr2
                j.draw(colorb)
        for snake in self.snakes:
            snake.draw()
        for ladder in self.ladders:
            ladder.draw()

                
