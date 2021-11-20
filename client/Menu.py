import pygame

from Container.InputBox import InputBox
from Container.Button import Button

class Menu:
    def __init__(self, gameDisplay, quit_fct, play_fct):
        self.gameDisplay = gameDisplay
        self.quit_fct = quit_fct
        self.play_fct = play_fct
        self.width = gameDisplay.get_rect().width
        self.font_title = pygame.font.SysFont(None, 80)
        self.font = pygame.font.SysFont(None, 40)
        self.input_box = InputBox((self.width / 2) - (150 / 2), 235, 150, 32, self.width)
        self.play_button = Button((self.width / 2) - (240 / 2), 340, 240, 50, self.width, pygame.Color('red'), False, 'Play')
        self.quit_button = Button((self.width / 2) - (240 / 2), 430, 240, 50, self.width, pygame.Color('red'), True, 'Quit game')

    def center(self, object):
        return (self.width / 2) - (object.get_rect().width / 2)

    def handle_event(self, event):
        self.input_box.handle_event(event)
        self.play_button.handle_event(event, self.play_fct)
        self.quit_button.handle_event(event, self.quit_fct)
        if self.play_button.active and self.play_fct and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.play_fct()

    def get_username(self):
        return self.input_box.text

    def draw(self):
        title = self.font_title.render('Snakes and Ladders', False, (0, 0, 0))
        self.gameDisplay.blit(title, (self.center(title), 50))
        user_text = self.font.render('Username:', False, (0, 0, 0))
        self.gameDisplay.blit(user_text, (self.center(user_text), 200))
        self.input_box.update()
        self.input_box.draw(self.gameDisplay)
        if (len(self.input_box.text) == 0):
            self.play_button.set_status(False)
        else:
            self.play_button.set_status(True)
        self.play_button.draw(self.gameDisplay)
        self.quit_button.draw(self.gameDisplay)