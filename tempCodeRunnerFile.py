import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((500, 500))  # width x height
pygame.display.set_caption("Pygame Window")

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
