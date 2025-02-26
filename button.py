# button.py
# potential subclass: Piece 
import pygame

class Button:

    def __init__(self, surface, color, x, y, width, height):
        self.surface = surface
        self.color = color
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)

    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def is_left_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

    def is_clicked(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.is_left_click(event):
            return True
        return False
    
class TextButton(Button):
    
    def __init__(self, surface, color, text, x, y, width, height):
        super().__init__(surface, color, x, y, width, height)
        
        # creating the text to render on button
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = self.font.render(text, False, 'black')
    
    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.surface.blit(self.text_surface, (self.x, self.y))


if __name__ == "__main__":
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

    button1 = Button(screen, 'red', 50, 50, 50, 50)
    button2 = TextButton(screen, 'green', "hello", 50, 100, 100, 50)

    run = True
    background = pygame.image.load('assets/Janggi_Board.png').convert()

    while run:
        screen_width, screen_height = screen.get_size()
        background = pygame.transform.smoothscale(background, screen.get_size())
        screen.blit(background, (0, 0))
        
        button1.render()
        button2.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()