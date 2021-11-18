import pygame
import random
from Board import *

class Piece:
    def __init__(self, gameDisplay, colour, board, userUid):
        self.gameDisplay = gameDisplay
        self.colour = colour
        self.size = 10
        self.position = 1
        self.board: Board = board
        square: Square = self.board.get_square(self.position)
        self.x = square.x
        self.y = square.y
        self.userUid = userUid
        square.add_piece(self)

    def move(self, diceNumber):
        oldPosition = self.position
        if self.position + diceNumber <= 100:
            self.position += diceNumber
        else:
            print("You can not move")
        if self.position == 100:
            print("+=+"*10+" YOU WIN "+"+=+"*10)
        
        oldSquare = self.board.get_square(oldPosition)
        oldSquare.remove_piece(self)

        square = self.board.get_square(self.position)
        self.x = square.x
        self.y = square.y
        square.add_piece(self)

    def draw(self, x = 0, y = 0):
        pygame.draw.circle(self.gameDisplay, (self.colour), (self.x + 30 + x, self.y + 30 + y), self.size)
