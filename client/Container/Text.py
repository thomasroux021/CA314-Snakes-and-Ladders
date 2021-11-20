import pygame
from Utils import *
from Constant import *

class Text:
    def __init__(self, gameDisplay, text, x, y, size=20, color = Constant.darkback, font="comicsansms") -> None:
        self.x = x
        self.y = y
        self.game_display = gameDisplay
        self.smallText1 = pygame.font.SysFont(font, size)
        self.textSurf, self.textRect = Utils.text_objects(text, self.smallText1, color, Constant.back)
        self.textRect.center = ( self.x, self.y )
        
        self.textBlit = self.game_display.blit(self.textSurf, self.textRect)
    def get_blit(self):
        return self.textBlit

    def draw(self):
	    self.textBlit = self.game_display.blit(self.textSurf, self.textRect)