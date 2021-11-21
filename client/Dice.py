import pygame
from Constant import *
import random

class Dice:
    def __init__(self, gameDisplay, x = 605, y = 100, w = 190, h = 190) -> None:
        self.value = 1
        self.isServResp = False
        self.rollDiceAnimation = False
        self.gameDisplay = gameDisplay
        self.size = 25
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.blit = None

    def roll_dice_animation(self, data):
        self.rollDiceAnimation = True

    def setServResp(self, value):
        self.value = value
        self.isServResp = True

    def reset(self):
        self.isServResp = False
        self.rollDiceAnimation = False

    def one(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//2)), (y+(h//2))), self.size)


    def two(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(h//2))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//2))), self.size)


    def three(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(3*h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//2)), (y+(h//2))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//4))), self.size)


    def four(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(3*h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(3*h//4))), self.size)


    def five(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//2)), (y+(h//2))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(3*h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//4))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(3*h//4))), self.size)


    def six(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.blit = pygame.draw.rect(self.gameDisplay, Constant.darkback, (x, y, w, h))
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(h//2))), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//2))), self.size)

        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(h//4))-10), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(w//4)), (y+(3*h//4))+10), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(h//4))-10), self.size)
        pygame.draw.circle(self.gameDisplay, Constant.forg, ((x+(3*w//4)), (y+(3*h//4))+10), self.size)

    def get_blit(self):
        return self.blit

    def event(self, event, rollDice):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            diceBlit = self.get_blit()
            if (diceBlit and diceBlit.collidepoint(pos)):
                rollDice()

    def draw(self):
        # if (self.showDice):
        no = random.randint(1,6) if (not self.isServResp and self.rollDiceAnimation) else self.value
        if no == 1:
            self.one()
        elif no == 2:
            self.two()
        elif no == 3:
            self.three()
        elif no == 4:
            self.four()
        elif no == 5:
            self.five()
        elif no == 6:
            self.six()
        if (self.rollDiceAnimation):
            pygame.time.wait(50)
            pygame.display.update()
