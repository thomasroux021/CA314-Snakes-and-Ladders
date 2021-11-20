import pygame

class Image:
    def __init__(self, gameDisplay, path, x, y) -> None:
        self.path = path
        self.x = x
        self.y = y
        self.game_display = gameDisplay

        self.image = pygame.image.load(self.path)
    
    def draw(self):
        self.game_display.blit(self.image, (self.x, self.y))