# piece.py
from button import *
from board import Board

PATH = 'assets/Pieces/' # path to piece images
DEAF_IMG = 'assets/Pieces/Blank_Piece.png'
BOLD, BOLD_END = '\033[1m', '\033[0m'

class Piece(TextureButton):
    def __init__(self, grid_pos, pos, size, team=None,
                 image_file=DEAF_IMG,
                 international=True):
        super().__init__(pos, size, image_file)
        self.VALUE = 0           # the value the piece is worth
        self.team = team         # team of the piece
        self.location = grid_pos # where the piece is located on the board
        self.possible_moves = None
        self.international = international
        self.selected = False    # a 'latch' to render possible moves when piece is clicked
        self.set_piece_image()

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
            self.possible_moves = self.func(board)
            self.selected = not self.selected
            print(self.possible_moves)
        # if left click occured, but piece wasnt clicked
        elif self.is_left_click(event):
            self.selected = False

    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int,int]]:
        curr_pos = self.get_position()
        valid_spots = []
        # iterate through list and see if it is valid position
        for delta in possible_spots:
            pos = tuple(map(lambda i, j: i + j, curr_pos, delta))
            if board.is_pos_avaliable(pos):
                valid_spots.append(delta)
        return valid_spots

    def set_piece_image(self) -> None:
        if self.team:
            file_name = PATH
            file_name += 'I_' if self.international else ''
            file_name += 'Cho_' if self.team.capitalize() == 'Cho' else 'Han_'
            file_name += str(self).capitalize() + '.png'
            self.set_image(file_name)
        else:
            self.set_image(DEAF_IMG)

    def render_possible_spots(self, board:Board, surface):
        spots_as_pieces = []
        for pos in self.possible_moves:
            render_pos = board.calculate_render_pos(pos)
            spots_as_pieces.append(Piece(pos, render_pos, board.piece_size))
        for spot in spots_as_pieces:
            spot.render(surface)

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

        # opposing side's palace
        OTHER_PALACE = [add_tuples(x, (-7, 0)) for x in PALACE_SPOTS]
        PALACE_SPOTS.extend(OTHER_PALACE)

        if pos in PALACE_SPOTS:
            return True
        return False
    
    def filter_moves(self, board:Board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        valid_spots, curr_pos = [], self.get_position()
        possible_spots = super().filter_moves(board, possible_spots)
        # filter spots that are not in palace area
        for delta in possible_spots:
            pos = add_tuples(curr_pos, delta)
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

class Artillery(Piece):
    def get_adjacent_rows_and_cols(self, board:Board) -> dict[tuple, tuple[int,int]]:
        row_index = self.grid_pos[1]
        col_index = self.grid_pos[0]
        
        # get row and col of board that this piece is on
        row = board.grid[col_index]
        col = [col[row_index] for col in board.grid]

        # get spots left, right, above and below this piece
        left_side, right_side = split_array(row, row_index)
        top_side, botton_side = split_array(col, col_index)

        # left & top lists reversed so it can get piece closest to current piece
        # tuples are the movement deltas for corresp. side
        lists_to_process = {
            tuple(left_side[::-1]) : (0, -1),
            tuple(right_side)      : (0, 1),
            tuple(top_side[::-1])  : (-1, 0),
            tuple(botton_side)     : (1, 0)
        }
        return lists_to_process

class King(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 5
        self.func = self.get_possible_moves

    def __str__(self):
        return 'King'

    def __repr__(self):
        return 'king'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = []
        possible_deltas = [
            (-1, 0), # up
            ( 1, 0), # down
            ( 0,-1), # left
            ( 0, 1), # right
            (-1,-1), # top left
            ( 1,-1), # top right
            ( 1,-1), # bottom left
            ( 1, 1), # bottom right
            ]
        
        possible_deltas = self.filter_moves(board, possible_deltas)
        for delta in possible_deltas:
            possible_spots.append(add_tuples(self.grid_pos, delta))
        return possible_spots

class Advisor(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 3
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Advisor'

    def __repr__(self):
        return 'advisor'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = []
        possible_deltas = [
            (-1, 0), # up
            ( 1, 0), # down
            ( 0,-1), # left
            ( 0, 1), # right
            (-1,-1), # top left
            (-1, 1), # top right
            ( 1,-1), # bottom left
            ( 1, 1), # bottom right
            ]
        
        possible_deltas = self.filter_moves(board, possible_deltas)
        for delta in possible_deltas:
            possible_spots.append(add_tuples(self.grid_pos, delta))
        return possible_spots

class Pawn(Piece):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 2
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Pawn'

    def __repr__(self):
        return 'Pawn'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        possible_spots = []
        possible_deltas = [
            (-1, 0), # up
            ( 0,-1), # left
            ( 0, 1), # right
            ]

        possible_deltas = self.filter_moves(board, possible_deltas)
        for delta in possible_deltas:
            possible_spots.append(add_tuples(self.grid_pos, delta))
        return possible_spots

class Elephant(Animal):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 3
        self.DIAGONAL_STEPS = 2
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Elephant'

    def __repr__(self):
        return 'elephant'

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
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 5
        self.DIAGONAL_STEPS = 1
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Horse'

    def __repr__(self):
        return 'horse'

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

class Cannon(Artillery):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 7
        self.func = self.get_possible_moves
    
    def __str__(self):
        return 'Cannon'

    def __repr__(self):
        return 'Cannon'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        print(f'Cannon clicked at pos {self.grid_pos}')
        possible_spots = []
        lists_to_process = self.get_adjacent_rows_and_cols(board)

        for pieces, delta in lists_to_process.items():
            pieces = list(pieces)
            closest_piece = get_first_item_in(pieces)

            if closest_piece:
                piece_pos = closest_piece.grid_pos
                piece_index = pieces.index(closest_piece)
                _, spots_past_piece = split_array(pieces, piece_index)

                for spot in spots_past_piece:
                    if spot is None:
                        piece_pos = add_tuples(piece_pos, delta)
                        possible_spots.append(piece_pos)
        
        return possible_spots
    
class Chariot(Artillery):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        # image_file = team.capitalize()
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 13
        self.func = self.get_possible_moves
    
    def __str__(self):
        return 'Chariot'

    def __repr__(self):
        return 'chariot'

    def get_possible_moves(self, board:Board) -> list[tuple[int]]:
        print('Chariot clicked at pos', self.grid_pos)
        possible_spots = []
        lists_to_process = self.get_adjacent_rows_and_cols(board)

        for pieces, delta in lists_to_process.items():
            pieces = list(pieces)
            current_pos = self.grid_pos
            for piece in pieces:
                current_pos = add_tuples(current_pos, delta)
                possible_spots.append(current_pos)
                if piece:
                    break                      

        return possible_spots

def add_tuples(x:tuple, y:tuple) -> tuple:
    try:
        return tuple(map(lambda i, j: i + j, x, y))
    except TypeError:
        print('types are incompatible to add.')
        return None

# splits list into two lists at the index specified.
# leaves out the specified index from list.
def split_array(list:list, index) -> tuple[list,list]:
    list1 = list[:index]
    list2 = list[index+1:]
    return (list1, list2)

def get_first_item_in(list:list):
    for piece in list:
        if piece:
            return piece
    return None
