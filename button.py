# button.py
# potential subclass: Piece 
import pygame
DEFAULT_IMAGE = 'assets/missing_image.png'

class Button:

    def __init__(self, pos, size, func=None, color='white', hover_color='grey'):
        self.hover_color = hover_color
        self.normal_color = color
        self.color = color
        self.pos = pos
        self.width, self.height = size
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.func = self._default_func if func is None else func # use deaf func if one not def

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def is_left_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

    def is_clicked(self, event, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.is_left_click(event):
            return True
        return False

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def process(self, event, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.normal_color
        if self.is_clicked(event, mouse_pos):
            self.func()

    def _default_func(self):
        print('default button function')



class TextButton(Button):
    
    def __init__(self, pos, size, text="", func=None, color='white', hover_color='grey', font_size=30):
        super().__init__(pos, size, func, color, hover_color)
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text_surface = self.font.render(text, False, 'black')
        self.text_rect = self.text_surface.get_rect(center=(self.pos[0] + self.width/2, self.pos[1] + self.height/2))

    def render(self, surface):
        super().render(surface)
        surface.blit(self.text_surface, self.text_rect)

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
            
    def render(self, surface):
        surface.blit(self.image, self.pos)
