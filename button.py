# button.py
# potential subclass: Piece 
import pygame

class Button:

    def __init__(self, surface, color, x, y, width, height):
        self.surface = surface
        self.color = color
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)

    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def is_left_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

    def is_clicked(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.is_left_click(event):
            return True
        return False