import pygame

class Image:
    def __init__(self, gameDisplay, path, x, y, w = 0, h = 0, rotation = 0, here = None) -> None:
        self.path = path
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.here = here
        self.rotation = rotation
        self.game_display = gameDisplay

        if self.here is None:
            self.image = pygame.image.load(self.path)
            if (self.w != 0 and self.h != 0):
                self.image = pygame.transform.scale(self.image, (self.w, self.h))
            if (self.rotation != 0):
                self.image = pygame.transform.rotate(self.image, self.rotation + 90)
        else:
            self.image = pygame.image.load(self.path)
            imageRect = self.image.get_rect()
            self.route = pygame.Surface((imageRect.w, imageRect.h))
            self.route.set_colorkey(0)
            self.route.blit(self.image, (0,0), area=self.route.get_rect())
            self.route = pygame.transform.scale(self.route, (30, self.h))
            self.route = pygame.transform.rotate(self.route, self.rotation + 90 )
    
    def get_rect(self):
        return self.image.get_rect()
    
    def draw(self):
        if (self.here):
            self.game_display.blit(self.route, self.here)
        else:
            self.game_display.blit(self.image, (self.x, self.y))