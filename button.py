# button.py
# potential subclass: Piece 
import pygame
from text import Text
DEFAULT_IMAGE = 'assets/missing_image.png'

class Button:

    def __init__(self, pos, size, func=None, color='white', hover_color='grey'):
        self.hover_color = hover_color
        self.normal_color = color
        self.color = color
        self.pos = pos
        self.width, self.height = size
        self._rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.func = self._default_func if func is None else func # use deaf func if one not def

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self._rect)

    def is_left_click(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def is_right_click(self, event, mouse_pos):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 3

    def is_clicked(self, event, mouse_pos):
        return self._rect.collidepoint(mouse_pos) and self.is_left_click(event)

    def is_right_clicked(self, event, mouse_pos):
        return self._rect.collidepoint(mouse_pos) and self.is_right_click(event)

    def is_hovered(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)

    def process(self, event, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.normal_color
        if self.is_clicked(event, mouse_pos):
            self.func()

    def set_pos(self, pos):
        self.pos = pos
        self._rect = pygame.Rect(pos[0], pos[1], self.width, self.height)

    def _default_func(self):
        print('default button function')

class TextButton(Button):
    
    def __init__(self, pos, size, text="", func=None, color='white', hover_color='grey', font_size=30):
        super().__init__(pos, size, func, color, hover_color)
        pygame.font.init()
        self.text = Text(pos=pos, text=text, size=font_size)

    def render(self, surface):
        super().render(surface)
        self.text.render(surface)

    def set_pos(self, pos):
        super().set_pos(pos)
        text_pos = (pos[0]+self.width/2-self.text.width/2, pos[1]+self.height/2-self.text.height/2)
        self.text.set_pos(text_pos)

class TextureButton(Button):

    def __init__(self, pos, size, image_file, func=None, color='white', hover_color='grey'):
        super().__init__(pos, size, func, color, hover_color)
        self.set_image(image_file)
        
    def set_image(self, image_file):
        try:
            self.image = pygame.image.load(image_file).convert_alpha()
        except OSError:
            print(f'file {image_file} not found. using a default image')
            self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def set_size(self, size):
        self.image = pygame.transform.scale(self.image, size)
            
    def render(self, surface):
        surface.blit(self.image, self.pos)