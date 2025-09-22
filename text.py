# text.py
import pygame

class Text:
    def __init__(self, pos=(0,0), text:str='', font='comic sans ms', size=50, color=(0,0,0), antialias=True):
        self._aa = antialias
        self._pos = pos
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(font, size)
        self._text_surface = self._font.render(text, antialias, color)
        self.rect = self._text_surface.get_rect()

    def render(self, surface):
        surface.blit(self._text_surface, self._pos)

    def set_text(self, text:str):
        self._text = text
        self._text_surface = self._font.render(self._text, self._aa, self._color)
        self.rect = self._text_surface.get_rect()

    def set_pos(self, pos:tuple[int,int]):
        self._pos = pos