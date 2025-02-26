import pygame
import os
#pygame.draw.rect(screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
# Main menu loop
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.run = True

        # Set the background image
        self.background = pygame.image.load('assets/Janggi_Board.png').convert()
    def display(self):
        while self.run:
            #Gets current screen width and height
            screen_width, screen_height = self.screen.get_size()
            #makes background image conform to current screen size
            self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
            #????
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()