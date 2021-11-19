from typing import List
import pygame
import Constant
from Utils import Utils
from Piece import *

class Square:
    def __init__(self, x, y, position, gameDisplay) -> None:
        self.x = x
        self.y = y
        self.pos = position
        self.pieces: List[Piece] = []
        self.gameDisplay = gameDisplay
    
    def add_piece(self, piece):
        self.pieces.append(piece)
    
    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def draw(self, colorb):
        pygame.draw.rect(self.gameDisplay, (colorb), (self.x, self.y, 59, 59))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = Utils.text_objects(str(self.pos), smallText, Constant.darkback)
        textRect.center = ((self.x+(60/2)), (self.y+(60/2)))
        self.gameDisplay.blit(textSurf, textRect)
        for idx, piece in enumerate(self.pieces):
            x = 0
            if (len(self.pieces) >= 2):
                x = -(60 / len(self.pieces))
                x += (idx) * (60 / len(self.pieces))
            piece.draw(x)