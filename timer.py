# timer.py
import pygame
from misc_functions import add_tuples
BG_MARG = 10

class BaseTimer():
    def __init__(self, pos:tuple[int,int], font=None, size=50, font_color='black', background_color='white'):
        self.counter = 0
        self.pos = pos
        self.font_color = font_color
        self.background_color = background_color
        self.text = format_time(self.counter)
        self.font = pygame.font.Font(font, size=size)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def process(self):
        pass

    def render(self, surface):
        self.text_to_render = self.font.render(self.text, True, self.font_color)
        self.font_size = self.font.size(self.text)
        self.background = pygame.rect.Rect(self.pos[0], self.pos[1],
                                           self.font_size[0]+BG_MARG, self.font_size[1]+BG_MARG)
        
        pygame.draw.rect(surface, self.background_color, self.background)
        # surface.blit(self.text_to_render, add_tuples(self.background.center, self.pos))
        surface.blit(self.text_to_render, add_tuples(self.pos, (BG_MARG/2, BG_MARG/2)))

class IncTimer(BaseTimer):
    def __init__(self, pos, font=None, size=50, font_color='black', background_color='white'):
        super().__init__(pos, font, size, font_color, background_color)

    def render(self, surface):
        return super().render(surface)
    
    def process(self, event, mouse_pos):
        if event.type == pygame.USEREVENT:
            self.counter += 1
            self.text =  format_time(self.counter)


class DecTimer(BaseTimer):
    def __init__(self, starting_time, pos:tuple[int,int],
                 font=None, size=50, font_color='black', background_color='white'):
        super().__init__(pos, font, size, font_color, background_color)
        self.counter = starting_time
        self.text = format_time(self.counter)

    def render(self, surface):
        return super().render(surface)
        
    def process(self, event, mouse_pos):
        if event.type == pygame.USEREVENT:
            self.counter -= 1
            self.text =  format_time(self.counter) if self.counter > 0 else 'BOOM!'

def format_time(time_in_seconds:int):
    minute_counter = 0
    while time_in_seconds >= 60:
        time_in_seconds -= 60
        minute_counter += 1
    return f'{minute_counter:{0}>2}:{time_in_seconds:{0}>2}'
