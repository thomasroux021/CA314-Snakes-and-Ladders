import random
from typing import Counter

class Board:
    def __init__(self, nb_snake, nb_ladder):
        # board List
        self.square = 100
        self.countarr = [self.square, 1]
        self.boardarr = self.generateBoard()
        self.snakes = self.generateSnake(nb_snake)
        self.ladders = self.generateLadder(nb_ladder)

    def generateBoard(self):
        board = []
        isLeftRight = True
        for i in range(0, 10):
            temp = []
            for j in range(0, 10):
                if (not isLeftRight):
                    x = (9 - j) * 60
                else:
                    x = j * 60
                y = i * 60
                temp.append((x, y, self.square - (i * 10 + j)))
            if (not isLeftRight):
                temp.reverse()
            board.append(temp)
            isLeftRight = not isLeftRight
        return board

    def generateSnake(self, nb_snake):
        snakes = []
        for i in range(nb_snake):
            val = True
            while val:
                rand1 = random.randint(2, self.square)
                rand2 = random.randint(1, rand1 - 1)
                diff = rand1-rand2
                if diff > 10 or diff < -10:
                    if rand1 not in self.countarr and rand2 not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand1 == y[2]:
                        a = y[2]
                    if rand2 == y[2]:
                        b = y[2]
            snakes.append([a, b])
        return snakes

    def generateLadder(self, nb_ladder):
        ladders = []
        for i in range(nb_ladder):
            val = True
            while val:
                rand1 = random.randint(1, self.square - 1)
                rand2 = random.randint(rand1 + 1, self.square)
                diff = rand1-rand2
                if diff > 10 or diff < -10:
                    if rand1 not in self.countarr and rand2 not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand1 == y[2]:
                        a = y[2]
                    if rand2 == y[2]:
                        b = y[2]
            ladders.append([a, b])
        return ladders
