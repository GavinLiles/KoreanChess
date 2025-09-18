import pygame
from button import TextButton
from states.state import State
import container

class MainMenu(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager) # call parent init
        self.title = self.DEFAULT_FONT.render('Korean Chess', False, (0,0,0))
        self.background = pygame.transform.scale(pygame.image.load('assets/bg.jpg').convert(), self.screen_size)
        self.container = container.Container()

        button_size = (150, 70)

        button_traits = {
            'play': lambda: self.manager.change_state('pregame_swap'),
            'settings': lambda: self.manager.change_state('settings'),
            'exit': lambda: exit(),  # or pygame.quit()
            'test': lambda: self.manager.change_state('test'),
        }
        
        # create buttons from dict, add to list
        for label, function in button_traits.items():
            self.container.add_item(TextButton((0, 0), button_size, label, func=function))

        x = self.screen_size[0]/2 - self.container.get_size()[0]/2
        y = self.screen_size[1]/3
        self.container.set_pos((x, y))

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        self.container.process(event, mouse_pos)

        if event.type == pygame.VIDEORESIZE:
            self.screen_size = self.screen.get_size()
            self.background = pygame.transform.scale(pygame.image.load('assets/bg.jpg').convert(), self.screen_size)
            x = self.screen_size[0]/2 - self.container.get_size()[0]/2
            y = self.screen_size[1]/3
            self.container.set_pos((x, y))

    def render(self):
        pygame.draw.rect(self.screen, (255,255,0), (0, 0, self.screen_size[0], self.screen_size[1]))
        self.screen.blit(self.background, (0,0))
        self.container.render(self.screen)

        # render title
        title_size = self.DEFAULT_FONT.size('Korean Chess')
        self.screen.blit(self.title, (self.screen_size[0]/2-(title_size[0]/2), 100))

    def set_state_manager(self, manager):
        self.manager = manager

def dummy():
    print('dummy')