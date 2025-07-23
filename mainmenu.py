import pygame
from button import TextButton
from state import State

class MainMenu(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager) # call parent init
        self.buttons = []
        self.title = self.DEFAULT_FONT.render('Korean Chess', False, (0,0,0))
        self.background = pygame.transform.scale(pygame.image.load('assets/bg.jpg').convert(), self.screen_size)
        
        button_size = (150, 70)
        x_pos = (self.screen_size[0]/2)-(button_size[0]/2)

        button_traits = {
            'play': lambda: self.manager.change_state('pregame_swap'),
            'settings': lambda: self.manager.change_state('settings'),
            'exit': lambda: exit(),  # or pygame.quit()
            'test': lambda: self.manager.change_state('test'),
        }
        
        # create buttons from dict, add to list
        button_spacing, y_pos_factor, y_offset = button_size[1]+10, 2, 200
        for label, function in button_traits.items():
            y = y_offset + (button_spacing * y_pos_factor)
            self.buttons.append(TextButton((x_pos, y), button_size, label, func=function))
            y_pos_factor += 1

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        for button in self.buttons:
            button.process(event, mouse_pos)

    def render(self):
        pygame.draw.rect(self.screen, (255,255,0), (0, 0, self.screen_size[0], self.screen_size[1]))
        self.screen.blit(self.background, (0,0))
        for button in self.buttons:
            button.render(self.screen)

        # render title
        title_size = self.DEFAULT_FONT.size('Korean Chess')
        self.screen.blit(self.title, (self.screen_size[0]/2-(title_size[0]/2), 100))

    def set_state_manager(self, manager):
        self.manager = manager

def dummy():
    print('dummy')