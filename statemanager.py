from mainmenu import MainMenu
from settings import Settings
from game import Game
from pregame_swap import PregameSwap
from test import Test

class StateManager:
    def __init__(self, screen):
        self.current_state = None
        self.states = {
            'main_menu':MainMenu(screen, self),
            'game':Game(screen, self),
            'settings':Settings(screen, self),
            'test':Test(screen, self),
            'pregame_swap':PregameSwap(screen, self)
        }
        self.current_state = self.states['main_menu']

    def process(self, event, mouse_pos):
        self.current_state.process(event, mouse_pos)

    def render(self):
        self.current_state.render()
    
    def change_state(self, state, data=None):
        try:
            self.current_state = self.states[state]
            if data: self.current_state.recieve_data(data)
        except KeyError as e:
            print('State not found.')
            exit()

if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    run = True

    manager = StateManager(screen)

    while run:
        mouse_pos = pygame.mouse.get_pos()
        manager.current_state.render()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            manager.process(event, mouse_pos)

        pygame.display.update()

    # Quit Pygame
    pygame.quit()
