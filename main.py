import pygame
from mainmenu import MainMenu

if __name__ == '__main__':
    run = True
    main_menu = MainMenu()
    main_menu.set_active()

    while run:
        if main_menu.is_active():
            main_menu.process()
        else:
            run = False

    pygame.quit()