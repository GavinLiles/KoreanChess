# piece.py
from button import *

class Piece(TextureButton):
    def __init__(self, pos, size, func, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(pos, size, image_file, func)
        self.value = 0       # the value the piece is worth
        self.team = None     # team of the piece
        self.location = None # where the piece is located on the board
    
class Pawn(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Pawn.png', func=func)
        self.value = 2

    def get_possible_moves():
        pass

class Advisor(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Advisor.png', func=func)
        self.value = 3

    def get_possible_moves():
        pass

class Elephant(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Elephant.png', func=func)
        self.value = 3

    def get_possible_moves():
        pass

class Horse(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Horse.png', func=func)
        self.value = 5

    def get_possible_moves():
        pass

class Cannon(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Cannon.png', func=func)
        self.value = 7

    def get_possible_moves():
        pass

class Chariot(Piece):
    def __init__(self, pos, size, func, team=None): 
        super().__init__(pos, size, image_file='assets/Pieces/I_Cho_Chariot.png', func=func)
        self.value = 13

    def get_possible_moves():
        pass

if __name__ == '__main__':
    import pygame
    import os

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    background = pygame.image.load('assets/Janggi_Board.png').convert()
    run = True
    def fun():
        print("click")
        
    pieces = [ 
        Chariot([50, 100], [50, 50], func=fun, team='cho'),
        Pawn([100, 100], [50, 50], func=fun, team='cho'),
        Cannon([150, 100], [50, 50], func=fun, team='cho'),
        Horse([200, 100], [50, 50], func=fun, team='cho')
    ]

    while run:
        background = pygame.transform.smoothscale(background, screen.get_size())
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for piece in pieces:
            piece.render(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            for piece in pieces:
                piece.process(event, mouse_pos)

        pygame.display.update()

    # Quit Pygame
    pygame.quit()