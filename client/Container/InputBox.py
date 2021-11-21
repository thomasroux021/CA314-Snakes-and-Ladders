import pygame

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class InputBox:

    def __init__(self, x, y, w, h, max_width, text=''):
        self.width = max_width
        self.font = pygame.font.Font(None, 40)
        self.box = pygame.Rect(x, y, w, h)
        self.rect = pygame.Rect(x, y + h, w, 0)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.box.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if (len(self.text) <= 15):
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, COLOR_ACTIVE)
    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.x = (self.width / 2) - (self.rect.w / 2)
        self.box.w = width
        self.box.x = (self.width / 2) - (self.box.w / 2)

    def center(self, object):
        return (self.width / 2) - (object.get_rect().width / 2)

    def draw(self, screen):
        self.txt_surface = self.font.render(self.text, True, self.color)
        # Blit the text.
        screen.blit(self.txt_surface, (self.center(self.txt_surface), self.box.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)