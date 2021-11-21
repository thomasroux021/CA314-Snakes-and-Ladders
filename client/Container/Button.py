import pygame

DESACTIVATE_COLOR = pygame.Color('DarkSlateGray')

class Button:
    def __init__(self, x, y, w, h, max_width, color, status, text='', font_size=40):
        self.width = max_width
        self.font = pygame.font.Font(None, font_size)
        self.box = pygame.Rect(x, y, w, h)
        self.active_color = color
        self.color = color if status else DESACTIVATE_COLOR
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = status

    def set_status(self, status):
        self.active = status
        self.color = self.active_color if status else DESACTIVATE_COLOR

    def handle_event(self, event, fct=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.active and self.box.collidepoint(event.pos) and fct:
                fct()

    def center_w(self, w, object):
        return (w / 2) - (object.get_rect().width / 2)

    def center_h(self, h, object):
        return (h / 2) - (object.get_rect().height / 2)

    def draw(self, screen):
        self.txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(self.txt_surface, (self.box.x + self.center_w(self.box.w, self.txt_surface), self.box.y + self.center_h(self.box.h, self.txt_surface)))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.box, 2)

