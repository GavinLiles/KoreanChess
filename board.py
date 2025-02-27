# board.py
import pygame
import os
import button
#pygame.draw.rect(screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
# Main menu loop
class Board:
    def __init__(self, screen):
        self.screen = screen
        self.run = True

        # Set the background image
        
    def display(self):
        while self.run:
            #Gets current screen width and height
            screen_width, screen_height = self.screen.get_size()
            #makes background image conform to current screen size
            self.background = pygame.image.load('assets/Janggi_Board.png').convert()
            self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
            self.screen.blit(self.background, (0, 0))
            #pygame.draw.rect(self.screen, 'green', [screen_width/2-50,screen_height/2-50,100,100])
            #Buttons
            QuitGame = button.TextButton(self.screen,screen_width/2-(screen_width/10)/2,screen_height/2-(screen_height/10)/2, screen_width/10 ,screen_height/10 , 'green' ,"Back" )
            QuitGame.render()
            #Detects and event that happens such as a click on screen or a key being pressed on the keyboard
            for event in pygame.event.get():
                #allows the user to close the game with the x in the top right corner
                if event.type == pygame.QUIT:
                    self.run = False
                elif QuitGame.is_clicked(event):
                    print("quit pressed")
                    return
                #If the user presses escape on the keyboard return them to the last menu
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("esc pressed")
                        return
            # Update the display
            pygame.display.update()

        # Quit Pygame
        pygame.quit()