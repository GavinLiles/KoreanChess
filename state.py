import pygame

class State:
    def __init__(self, manager):
        pygame.init()
        pygame.font.init()
        self.manager = manager
        self.DEFAULT_FONT = pygame.font.SysFont('Arial', 50)
        self.screen = pygame.display.set_mode((1000, 1000))
        self.screen_size = pygame.display.get_surface().get_size() # size of screen
        self.run = False
        print(f'{type(self)} initialized!!')

    def process(self, event, mouse_pos):
        pass

    def render(self):
        pass

    def activate_state(self, state):
        state.set_active()