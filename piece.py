# piece.py
from button import *
from board import Board

PATH = 'assets/Pieces/' # path to piece images

class Piece(TextureButton):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(pos, size, image_file)
        self.value = 0           # the value the piece is worth
        self.team = None         # team of the piece
        self.location = grid_pos # where the piece is located on the board
        self.possible_moves = None
    def __str__(self):
        return 'Piece'

    def set_position(self, grid_pos:tuple[int], pos:tuple[float]):
        self.grid_pos = grid_pos
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def get_position(self) -> tuple[int]:
        return self.grid_pos

    def process(self, board, event, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.normal_color
        if self.is_clicked(event, mouse_pos):
            self.func(board)

    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        curr_pos = self.get_position()
        valid_spots = []
        # iterate through list and see if it is valid position
        for delta in possible_spots:
            pos = tuple(map(lambda i, j: i + j, curr_pos, delta))
            if board.is_pos_avaliable(pos):
                valid_spots.append(delta)
        return valid_spots

    def is_in_palace(self, pos:tuple[int]) -> bool:
        PALACE_SPOTS = [
            (8, 4), # middle
            (9, 4), # bottom middle
            (7, 4), # top middle
            (8, 3), # middle left
            (9, 3), # bottom left
            (7, 3), # top left
            (8, 5), # middle right
            (9, 5), # bottom right
            (7, 5), # top right
        ]
        if pos in PALACE_SPOTS:
            return True
        return False

class Royalty(Piece):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(grid_pos, pos, size, team, image_file)

    def __str__(self):
        return super().__str__()
    
    def filter_moves(self, board, possible_spots):
        return super().filter_moves(board, possible_spots)

class King(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_King.png')
        self.value = 5
        self.func = self.get_possible_moves

    def __str__(self):
        return 'King'

    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        valid_spots = []
        curr_pos = self.get_position()
        possible_spots = super().filter_moves(board, possible_spots)
        # removes spots not in palace
        for delta in possible_spots:
            pos = tuple(map(lambda i, j: i + j, curr_pos, delta))
            if self.is_in_palace(pos):
                valid_spots.append(delta)
        return valid_spots


    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = [
            (-1, 0), # up
            ( 1, 0), # down
            ( 0,-1), # left
            ( 0, 1), # right
            (-1,-1), # top left
            ( 1,-1), # top right
            ( 1,-1), # bottom left
            ( 1, 1), # bottom right
            ]
        
        possible_spots = self.filter_moves(board, possible_spots)
        print(possible_spots)
        return possible_spots
    
class Pawn(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Pawn.png')
        self.value = 2
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Pawn'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = [
            (-1, 0), # up
            ( 0,-1), # left
            ( 0, 1), # right
            ]

        self.filter_moves(board, possible_spots)
        print(possible_spots)
        return possible_spots

class Advisor(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Advisor.png')
        self.value = 3
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Advisor'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = [
            (-1, 0), # up
            ( 1, 0), # down
            ( 0,-1), # left
            ( 0, 1), # right
            (-1,-1), # top left
            (-1, 1), # top right
            ( 1,-1), # bottom left
            ( 1, 1), # bottom right
            ]
        
        possible_spots = self.filter_moves(board, possible_spots)
        print(possible_spots)
        return possible_spots

class Elephant(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Elephant.png')
        self.value = 3
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Elephant'

    def get_possible_moves(self):
        print('Pawn clicked')

class Horse(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Horse.png')
        self.value = 5
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Horse'

    def get_possible_moves(self):
        print('Horse clicked')

class Cannon(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Cannon.png')
        self.value = 7
        self.func = self.get_possible_moves
    
    def __str__(self):
        return 'Cannon'

    def get_possible_moves(self):
        print('Cannon clicked')

class Chariot(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        # image_file = team.capitalize()
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Chariot.png')
        self.value = 13
        self.func = self.get_possible_moves
    
    def __str__(self):
        return 'Chariot'

    def get_possible_moves(self):
        print('Chariot clicked')

if __name__ == '__main__':
    import pygame

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    background = pygame.image.load('assets/Janggi_Board.png').convert()
    run = True
    def fun():
        print("click")
        
    pieces = [ 
        Chariot([50, 100], [50, 50], team='cho'),
        Pawn([100, 100], [50, 50], team='cho'),
        Cannon([150, 100], [50, 50], team='cho'),
        Horse([200, 100], [50, 50], team='cho')
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
