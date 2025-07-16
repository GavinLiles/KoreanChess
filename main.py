import pygame
from statemanager import StateManager

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    run = True

    manager = StateManager()
    manager.change_state('game')

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
