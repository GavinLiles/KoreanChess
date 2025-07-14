# test.py
from piece import *
from math import isclose
from player import Player, Position

MARGIN = 100
RATIO = 880 / 982

class Board():

    def __init__(self, surface):
        self.background = pygame.image.load('assets/boards/Janggi_Board.png').convert()
        self.boarder = pygame.image.load('assets/boards/Janggi_Board_Border.png').convert()
        self.grid = [ [None] * 9 for _ in range(10)] # array representation of board
        self._update_board_size()
        self.update_piece_size((75, 75))
        self.international = True
        self.SCREEN_CENTER = [i-(j/2) for i, j in zip(surface.get_rect().center, self._board_size)]
        self.cho_player = Player(self, 'cho', Position.BOTTOM)
        self.han_player = Player(self, 'han', Position.TOP)
        self.cho_player.add_pieces_to_board(self)
        self.han_player.add_pieces_to_board(self)
        self.update(surface)

    def __str__(self):
        string = ''
        for row in self.grid:
            for piece in row:
                if piece is not None:
                    string += '\033[0;34m' if piece.team == 'cho' else '\033[0;31m'
                    string += f'{str(piece):>9}'
                    string += '\033[0m'
                else:
                    string += f'{str(piece):>9}'
            string += '\n'
        return string

    def process(self, event, mouse_pos):
        for piece in self.cho_player.pieces:
            piece.process(self, event, mouse_pos)

    def at(self, pos:tuple[int]):
        try:
            # pos = self.grid[pos[0]][pos[1]]
            pos = self.grid[pos[1]][pos[0]]
            if pos:
                return pos
            return None
        except IndexError:
            return None

    def calculate_render_pos(self, grid_position:tuple[int]) -> tuple[float]:
        x = grid_position[1]*self.row_spacing-(self.piece_offset[0]) + self.SCREEN_CENTER[0]
        y = grid_position[0]*self.col_spacing-(self.piece_offset[0]) + self.SCREEN_CENTER[1]
        return (x, y)
    
    def is_pos_avaliable(self, pos:tuple[int]) -> bool:
        try:
            if self.grid[pos[0]][pos[1]] is None:
                return True
            return False
        except IndexError:
            return False

    def insert_piece(self, pos:tuple[int], item):
        try:
            self.grid[pos[0]][pos[1]] = item
        except IndexError:
            print(f'given index {pos} is not within bounds.')

    def move_piece(self, old_pos:tuple[int,int], new_pos:tuple[int,int]):
        if self.at(old_pos) is None:
            print('nothing is in old position')
        if self.at(new_pos):
            print('piece is aleady at new position')

        piece = self.grid[old_pos[0]][old_pos[1]]
        print(piece)
        self.insert_piece(new_pos, piece)
        self.insert_piece(old_pos, None)

    def update(self, surface):
        self._update_board_size()
        self.SCREEN_CENTER = [i-(j/2) for i, j in zip(surface.get_rect().center, self._board_size)]
        surface_size = surface.get_size()
        # if the window is not in ratio of the board,
        # set board's height off window,
        # and use the ratio of the board to keep it scaled properly
        if not isclose(min(surface_size)*(1+RATIO), max(surface_size)):
            scale = (surface_size[1]*RATIO, surface_size[1]-MARGIN)

        self.boarder = pygame.transform.scale(self.boarder, surface_size)
        self.background = pygame.transform.scale(self.background, scale)
        self.update_piece_positions()

    def update_piece_positions(self):
        for i in range(10):
            for j in range(9):
                if self.grid[i][j]:
                    pos = self.calculate_render_pos((i, j))
                    self.grid[i][j].set_position((i, j), pos)

    def update_piece_size(self, size:tuple[int]):
        self.piece_size = size
        self.piece_offset = tuple([i/2 for i in self.piece_size]) # offset for piece rendering

    def _update_board_size(self):
        self._board_size = self.background.get_size()
        self.row_spacing = self._board_size[0] / 8
        self.col_spacing = self._board_size[1] / 9

    def render(self, surface):
        self._render_board(surface)
        self.render_pieces(surface)

    def render_pieces(self, surface):
        for row in self.grid:
            for piece in row:
                if piece is not None:
                    piece.render(surface)
                    if piece.possible_moves and piece.selected:
                        for candidate in piece.possible_moves:
                            candidate.render(surface)

    def _render_board(self, surface):
        board_pos = [i-(j/2) for i, j in zip(surface.get_rect().center, self._board_size)]
        surface.blit(self.boarder, (0, 0))
        surface.blit(self.background, board_pos)

if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    run = True

    b = Board(screen)
    b.update(screen)

    while run:
        mouse_pos = pygame.mouse.get_pos()
        b.render(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                print(b.background.get_size())
                print(b)

            b.process(event, mouse_pos)

        pygame.display.update()

    # Quit Pygame
    pygame.quit()
