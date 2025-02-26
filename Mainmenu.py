import pygame
import os
# Initialize Pygame
pygame.init()
#get screen information
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
fullscreen_width, fullscreen_height = info.current_w, info.current_h


# Set up the display window and make is resizeable
screen = pygame.display.set_mode((fullscreen_width - 10, fullscreen_height - 50), pygame.RESIZABLE)  # width x height
pygame.display.set_caption("Pygame Window")

#set the font
# font = pygame.font.Font('freesansbold.ttf', 20)
# big_font = pygame.font.Font('freesansbold.ttf', 50)
#game vars and img

#pygame.draw.rect(screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
# Main menu loop
def main_menu():
    run = True
    background = pygame.image.load('clote0.bmp').convert()
    while run:
        screen_width, screen_height = screen.get_size()
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

main_menu()