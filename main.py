#libraries 
import pygame
import os

from Mainmenu import MainMenu

def main():
    # use user's machine's screen size as reference to screen width/height
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # initialize pygame instance
    pygame.init()

    #Frame rate
    clock = pygame.time.Clock()
    fps = 60

    #get screen information
    info = pygame.display.Info()
    fullscreen_width, fullscreen_height = info.current_w, info.current_h


    # Set up the display window and make is resizeable
    screen = pygame.display.set_mode((fullscreen_width - 10, fullscreen_height - 50), pygame.RESIZABLE)  # width x height
    pygame.display.set_caption("Pygame Window")

    #start game loop
    run = True
    while True:
# find matching event calls by player to pygame event calls
        for event in pygame.event.get():
			# if player closes window
            if event.type == pygame.QUIT:
				# halt execution
                run = False
        menu = MainMenu(screen)
        menu.display()
        clock.tick(fps)


        # Update the display
        pygame.display.update()

main()