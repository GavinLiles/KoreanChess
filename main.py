#libraries 
import pygame
import os
from board import Board
from button import TextButton

# takes in a board obj and mouse position
# returns false when player closes window
def game(b, mouse_pos, screen) -> bool:
    b.render(screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print(b.background.get_size())
            b.print_grid()
            return False

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if width < WIDTH_LIMIT_MIN:
                width = WIDTH_LIMIT_MIN
            if height < HEIGHT_LIMIT_MAX:
                height = HEIGHT_LIMIT_MAX
            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            b.update(screen)

        
        for piece in b.pieces:
            piece.process(b, event, mouse_pos)
    
    return True

def main_menu(mouse_pos, screen, button) -> bool:
    button.render(screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print(b.background.get_size())
            b.print_grid()
            return False

        button.process(event, mouse_pos)
    return True

        
def add_tuples(x:tuple, y:tuple) -> tuple:
    try:
        return tuple(map(lambda i, j: i + j, x, y))
    except TypeError:
        print('types are incompatible to add.')
        return None

def divide_tuple(x:tuple, divisor) -> tuple:
    try:
        return (x[0]/divisor, x[1]/divisor)
    except TypeError:
        exit(0)

if __name__ == '__main__':
    import pygame

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((1000, 1000))#, pygame.RESIZABLE)
    run = True
    WIDTH_LIMIT_MIN, HEIGHT_LIMIT_MAX = 800, 800

    b = Board(screen)
    b.update(screen)
    button_pos = screen.get_size()
    button = TextButton((0, 0), (100, 100), 'hello world!')

    while run:
        mouse_pos = pygame.mouse.get_pos()
        # run = game(b, mouse_pos, screen)
        run = main_menu(mouse_pos, screen, button)
        pygame.display.update()

    # Quit Pygame
    pygame.quit()