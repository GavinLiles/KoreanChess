import pygame, sys
from states.statemanager import StateManager

if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    run = True

    manager = StateManager(screen)
    manager.change_state('main_menu')

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

