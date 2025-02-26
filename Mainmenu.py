import pygame
import os
import button

# Initialize Pygame
pygame.init()
#get screen information
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h


# Set up the display window and make is resizeable
screen = pygame.display.set_mode((screen_width - 10, screen_height - 50), pygame.RESIZABLE)  # width x height
pygame.display.set_caption("Pygame Window")
#set the font
# font = pygame.font.Font('freesansbold.ttf', 20)
# big_font = pygame.font.Font('freesansbold.ttf', 50)
#game vars and img

# defining a button
button = button.Button(screen, 'red', 50, 50, 100, 50)

# Main game loop
run = True
while run:
    #draw a rectangle thats at pos 200 200 and make it 100 by 100 big
    pygame.draw.rect(screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
    button.render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if button.is_clicked(event):
            print("FNSKAJDGBSJKD")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
