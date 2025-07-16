from mainmenu import MainMenu
from settings import Settings
from game import Game
from game_over import GameOver

class StateManager:
    def __init__(self):
        self.current_state = None
        self.states = {
            'main_menu':MainMenu(self),
            'game':Game(self),
            'settings':Settings(self),
            'game_over':GameOver(self),
        }
        self.current_state = self.states['main_menu']
        self.current_state.set_active()

    def process(self, event, mouse_pos):
        self.current_state.process(event, mouse_pos)

    def render(self):
        self.current_state.render()
    
    def change_state(self, state):
        self.current_state.set_inactive()
        self.current_state = self.states[state]
        self.current_state.set_active()


if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    run = True

    manager = StateManager()
    # manager.change_state('settings')

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
