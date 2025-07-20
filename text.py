# text.py
import pygame

class Text:
    def __init__(self, text:str, font='comic sans ms', size=50, color=(0,0,0), antialias=True):
        self.size, self.color, self.antialias = size, color, antialias
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, antialias, color)
        self.size = self.font.size(text)

    def render(self, surface, position:tuple):
        surface.blit(self.text, position)

    def change_text(self, text):
        self.text = self.font.render(text, True, self.antialias, self.color)