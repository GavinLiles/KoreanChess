# button.py
# potential subclass: Piece 
import pygame

class Button:

    def __init__(self, surface, pos, size, func=None, color='white', hover_color='grey'):
        self.surface = surface
        self.hover_color = hover_color
        self.normal_color = color
        self.color = color
        self.pos = pos
        self.width, self.height = size
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.func = func

    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def is_left_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

    def is_clicked(self, event, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.is_left_click(event):
            return True
        return False

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def process(self, event, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.normal_color
        if self.is_clicked(event, mouse_pos):
            self.func()


class TextButton(Button):
    
    def __init__(self, surface, pos, size, text="", func=None, color='white', hover_color='grey', font_size=30):
        super().__init__(surface, pos, size, func, color, hover_color)
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text_surface = self.font.render(text, False, 'black')
        self.text_rect = self.text_surface.get_rect(center=(self.pos[0] + self.width/2, self.pos[1] + self.height/2))

    def render(self):
        super().render()
        self.surface.blit(self.text_surface, self.text_rect)

class TextureButton(Button):

    def __init__(self, surface, pos, size, image_file, func, color='white', hover_color='grey'):
        super().__init__(surface, pos, size, func, color, hover_color)
        self.set_image(image_file)
        
    def set_image(self, image_file):
        try:
            self.image = pygame.image.load(image_file).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except OSError:
            print(f'file {image_file} not found. Exiting')
            exit(0)
            
    def render(self):
        self.surface.blit(self.image, self.pos)


def button_func():
    print("presed")

if __name__ == "__main__":
    import pygame
    import os

    # Initialize Pygame
    pygame.init()
    #get screen information
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)  # width x height

    button1 = Button(screen, [50, 50], [50, 50], func=button_func)
    button2 = TextButton(screen, [100, 250], [100, 100], color='green', text="hello", func=button_func)
    button3 = TextureButton(screen, [50, 150], [100, 110], image_file="assets/dog.JPG", func=button_func)

    run = True
    background = pygame.image.load('assets/Janggi_Board.png').convert()

    while run:
        screen_width, screen_height = screen.get_size()
        background = pygame.transform.smoothscale(background, screen.get_size())
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        button1.render()
        button2.render()
        button3.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            button1.process(event, mouse_pos)
            button2.process(event, mouse_pos)
            button3.process(event, mouse_pos)


        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
