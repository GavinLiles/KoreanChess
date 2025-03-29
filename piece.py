# piece.py
from button import *
from board import Board

PATH = 'assets/Pieces/' # path to piece images

class Piece(TextureButton):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(pos, size, image_file)
        self.VALUE = 0           # the value the piece is worth
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

class Royalty(Piece):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(grid_pos, pos, size, team, image_file)

    def __str__(self):
        return super().__str__()

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
    
    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        valid_spots, curr_pos = [], self.get_position()
        possible_spots = super().filter_moves(board, possible_spots)
        # filter spots that are not in palace area
        for delta in possible_spots:
            pos = tuple(map(lambda i, j: i + j, curr_pos, delta))
            if self.is_in_palace(pos):
                valid_spots.append(delta)
        return valid_spots

class Animal(Piece):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(grid_pos, pos, size, team, image_file)
        self.DIAGONAL_STEPS = 1

    def _get_move_steps(self, pos:tuple[int], diagonal_steps:int=1) -> list[tuple[int]]:
        steps = []
        if abs(pos[0]) > abs(pos[1]):
            step_sign = 1 if pos[0] > 0 else -1
            first_step = (step_sign, 0)
            delta = [step_sign, 1] if pos[1] > 0 else [step_sign, -1]

        else:
            step_sign = 1 if pos[1] > 0 else -1
            first_step = (0, step_sign)
            delta = (1, step_sign) if pos[0] > 0 else (-1, step_sign)

        steps.append(first_step)
        for i in range(diagonal_steps):
            steps.append(tuple([x+(y*(i+1)) for x,y in zip(first_step, delta)]))
        return steps

    def _is_move_blocked(self, board:Board, move:tuple[int]) -> bool:
        steps = self._get_move_steps(move, self.DIAGONAL_STEPS)

        for step_delta in steps:
            pos = tuple(map(lambda i, j: i + j, self.grid_pos, step_delta))
            if not board.is_pos_avaliable(pos):
                return True
        return False

    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        possible_spots = super().filter_moves(board, possible_spots)
        valid_moves = []

        for delta in possible_spots:
            if not self._is_move_blocked(board, delta):
                valid_moves.append(delta)
        return valid_moves

class King(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_King.png')
        self.VALUE = 5
        self.func = self.get_possible_moves

    def __str__(self):
        return 'King'

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

class Advisor(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Advisor.png')
        self.VALUE = 3
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

class Pawn(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Pawn.png')
        self.VALUE = 2
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

class Elephant(Animal):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Elephant.png')
        self.VALUE = 3
        self.DIAGONAL_STEPS = 2
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Elephant'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = [
            (-3, -2), # top left
            (-3,  2), # top right
            (-2, -3), # left top
            ( 2, -3), # left bottom
            (-2,  3), # right top
            ( 2,  3), # right bottom
            ( 3, -2), # bottom left
            ( 3,  2), # bottom right
        ]
        possible_spots = self.filter_moves(board, possible_spots)
        print(f'Elephant clicked at {self.grid_pos}')
        print(f'Possible moevs for this piece: {possible_spots}')
        return possible_spots

class Horse(Animal):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Horse.png')
        self.VALUE = 5
        self.DIAGONAL_STEPS = 1
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Horse'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = [
            (-2,  1), # top right
            (-2, -1), # top left
            (-1, -2), # left top
            (-1,  2), # left bottom
            ( 1, -2), # right top
            ( 1,  2), # right bottom
            ( 2,  1), # bottom right
            ( 2, -1), # bottom left
        ]
        print(f'Horse clicked at position {self.grid_pos}.')
        possible_spots = self.filter_moves(board, possible_spots)
        
        print(f'possbile moves for this piece: {possible_spots}')
        return possible_spots

class Cannon(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Cannon.png')
        self.VALUE = 7
        self.func = self.get_possible_moves
    
    def __str__(self):
        return 'Cannon'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        print(f'Cannon clicked at pos {self.grid_pos}')

        # get horizontal slice of board that cannon is at
        # get position of all pieces in slice
        # get position of all pieces 
        for col in board.grid[self.grid_pos[0]]:
            if col:
                curr_col, other_col = self.grid_pos[1], col.grid_pos[1]
                print(curr_col, other_col, end=': ')
                if curr_col == other_col:
                    print("this is the current piece")
                elif curr_col < other_col:
                    print('other piece is to the right of current piece')
                    # get everything past the other piece
                    ls = board.grid[self.grid_pos[0]][other_col:]
                    print(*ls)

                else:
                    print('other piece is to the left of current piece')
                    # get everything past the other piece
                    ls = board.grid[self.grid_pos[0]][:other_col]
                    print(*ls)

                    
        # get vertical slice of board that cannon is at
        # get position of all pieces in slice
        # for row in board.grid:
        #     row = row[self.grid_pos[1]]
        #     if row:
        #         curr_row, other_row = self.grid_pos[0], row.grid_pos[0]
        #         print(curr_row, other_row, end=': ')
        #         if curr_row == other_row:
        #             print("this is the current piece")
        #         elif curr_row < other_row:
        #             print('other piece is below current piece')
        #         else:
        #             print('other piece is above current piece')
        print()

class Chariot(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        # image_file = team.capitalize()
        super().__init__(grid_pos, pos, size, image_file='assets/Pieces/I_Cho_Chariot.png')
        self.VALUE = 13
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
