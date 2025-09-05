# piece.py
from button import *
from misc_functions import *

PATH = 'assets/Pieces/' # path to piece images
# PATH = 'assets/pieces_white/' # path to piece images
DEAF_IMG = 'assets/Pieces/Blank_Piece.png'
BOLD, BOLD_END = '\033[1m', '\033[0m'

class Piece(TextureButton):
    PALACE_SPOTS = [
            (7, 3), (7, 4), (7, 5),
            (8, 3), (8, 4), (8, 5),
            (9, 3), (9, 4), (9, 5),
        ]
    # PALACE_DIAGONALS = [
    #         (7,3), (7,5),
    #             (8,4),
    #         (9,3), (9,5),
    # ]
    PALACE_DIAGONAL = {
        (9,3):[(-1,1)],
        (9,5):[(-1,-1)],
        (8,4):[(-1,-1),(-1,1)],
        (2,3):[(-1,1)],
        (2,5):[(-1,-1)],
        (1,4):[(-1,-1),(-1,1)],
    }
    PALACE_SPOTS.extend([add_tuples(x, (-7, 0)) for x in PALACE_SPOTS]) # other palace


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
        self.location = grid_pos
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def set_render_pos(self, render_pos:tuple[float,float]):
        self.pos = render_pos

    def get_position(self) -> tuple[int]:
        return self.location

    def process(self, board, event, mouse_pos) -> bool:
        ''' Pieces will return true if a valid move was made '''
        if self.is_hovered(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.normal_color
            
        if self.is_clicked(event, mouse_pos):
            self.selected = True
            self.possible_moves = self.func(board)
            self.possible_moves = self.create_candidates(board)

        if self.possible_moves:
            for candidate in self.possible_moves:
                if candidate.is_clicked(event,mouse_pos):
                    # get new render_pos, move piece on board, update piece's position
                    pos = candidate.location
                    render_pos = board.calculate_render_pos(pos)
                    captured_piece = board.move_piece(self.location, candidate.location)
                    self.set_position(pos, render_pos)
                    self.possible_moves.clear()
                    return True, captured_piece

        # if there was a left click, but the piece itself is not clicked, unselect it
        # must clear possible_moves so when you unselect it, you cant click on those spots
        if self.is_left_click(event) and not self.is_clicked(event, mouse_pos) and self.selected:
            self.selected = False
            self.possible_moves.clear()
        return False, None

    def filter_moves(self, board, possible_spots:list[tuple[int,int]]) -> list[tuple[int,int]]:
        ''' takes in move deltas and returns a list of deltas that are valid moves '''
        curr_pos = self.get_position()
        valid_spots = []

        for delta in possible_spots:
            pos = tuple(map(lambda i, j: i + j, curr_pos, delta))
            if board.is_pos_avaliable(pos):
                valid_spots.append(delta)
            elif board.at(pos) and board.at(pos).team != self.team:
                valid_spots.append(delta)

        return valid_spots

    def set_piece_image(self) -> None:
        if self.team:
            file_name = PATH
            file_name += 'I_' if self.international else ''
            file_name += 'Cho_' if self.team.capitalize() == 'Cho' else 'Han_'
            file_name += str(self).capitalize() + '.png'
            # file_name += 'blue_' if self.team.capitalize() == 'Cho' else 'red_'
            # file_name += str(self).lower() + '.svg'

            self.set_image(file_name)
        else:
            self.set_image(DEAF_IMG)

    def create_candidates(self, board):
        candidates = []
        for pos in self.possible_moves:
            render_pos = board.calculate_render_pos(pos)
            candidates.append(Candidate(pos, render_pos, board.piece_size))
        return candidates

    def render(self, surface):
        super().render(surface)
        if self.possible_moves and self.selected:
            for candidate in self.possible_moves:
                candidate.render(surface)

    def is_in_palace(self, pos:tuple[int]) -> bool:
        if pos in self.PALACE_SPOTS:
            return True
        return False

class Royalty(Piece):
    def __init__(self, grid_pos, pos, size, team=None, image_file='assets/Pieces/Blank_Piece.png'):
        super().__init__(grid_pos, pos, size, team, image_file)

    def __str__(self):
        return super().__str__()
    
    def filter_moves(self, board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
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

    def _is_move_blocked(self, board, move:tuple[int]) -> bool:
        steps = self._get_move_steps(move, self.DIAGONAL_STEPS)

        for step_delta in steps:
            pos = tuple(map(lambda i, j: i + j, self.location, step_delta))
            if not board.is_pos_avaliable(pos):
                return True
        return False

    def filter_moves(self, board, possible_spots:list[tuple[int]]) -> list[tuple[int]]:
        possible_spots = super().filter_moves(board, possible_spots)
        valid_moves = []

        for delta in possible_spots:
            if not self._is_move_blocked(board, delta):
                valid_moves.append(delta)
        return valid_moves

class Artillery(Piece):
    def get_adjacent_rows_and_cols(self, board) -> dict[tuple, tuple[int,int]]:
        row_index = self.location[1]
        col_index = self.location[0]
        
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

class Candidate(Piece):
    def __init__(self, grid_pos, pos, size):
        super().__init__(grid_pos, pos, size)
        self.func = self.clicked

    def __repr__(self):
        return 'candidate'

    def clicked(self):
        return self.location

class King(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True):
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 5
        self.func = self.get_possible_moves

    def __str__(self):
        return 'King'

    def __repr__(self):
        return 'king'

    def get_possible_moves(self, board) -> list[tuple[int]]:
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
            possible_spots.append(add_tuples(self.location, delta))
        return possible_spots

    def process(self, board, event, mouse_pos):
        valid_move, captured_piece = super().process(board, event, mouse_pos)
        if self.is_right_click(event, mouse_pos):
            valid_move = True
        return valid_move, captured_piece

class Advisor(Royalty):
    def __init__(self, grid_pos, pos, size, team=None, international=True): 
        super().__init__(grid_pos, pos, size, team)
        self.VALUE = 3
        self.func = self.get_possible_moves

    def __str__(self):
        return 'Advisor'

    def __repr__(self):
        return 'advisor'

    def get_possible_moves(self, board) -> list[tuple[int]]:
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
            possible_spots.append(add_tuples(self.location, delta))
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

    def get_possible_moves(self, board) -> list[tuple[int]]:
        possible_spots = []
        possible_deltas = [
            (-1, 0) if self.team == 'cho' else (1, 0), # up or down depending on team
            ( 0,-1), # left
            ( 0, 1), # right
            ]

        possible_deltas = self.filter_moves(board, possible_deltas)
        for delta in possible_deltas:
            possible_spots.append(add_tuples(self.location, delta))


        if self.location in self.PALACE_DIAGONAL:
            t = map(lambda d: add_tuples(self.location, d), self.PALACE_DIAGONAL[self.location])
            possible_spots.extend(list(t))

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

    def get_possible_moves(self, board) -> list[tuple[int]]:
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
        print(f'Elephant clicked at {self.location}')
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

    def get_possible_moves(self, board) -> list[tuple[int]]:
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
        print(f'Horse clicked at position {self.location}.')
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

    def get_possible_moves(self, board) -> list[tuple[int]]:
        print(f'Cannon clicked at pos {self.location}')
        possible_spots = []
        lists_to_process = self.get_adjacent_rows_and_cols(board)

        for pieces, delta in lists_to_process.items():
            pieces = list(pieces)
            closest_piece = get_first_item_in(pieces)

            if closest_piece:
                piece_pos = closest_piece.location
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

    def get_possible_moves(self, board) -> list[tuple[int]]:
        print('Chariot clicked at pos', self.location)
        possible_spots = []
        adj_rows_and_cols = self.get_adjacent_rows_and_cols(board)

        # iters through each list in adj_row_and_col
        for pieces, delta in adj_rows_and_cols.items():
            pieces = list(pieces)
            current_pos = self.location

            # add each empty pos into possible_spots, end loop
            # when piece is found.
            for piece in pieces:
                current_pos = add_tuples(current_pos, delta)
                possible_spots.append(current_pos)

                if piece and piece.team == self.team:
                    possible_spots.pop()
                    break
                elif piece:
                    break

        return possible_spots

