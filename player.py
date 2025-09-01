# player.py
from piece import *
from enum import Enum

class Position(Enum):
    TOP = 1
    BOTTOM = 2

BOTTOM_PIECES = {
    King: [(8, 4)],
    Advisor: [(9, 3), (9, 5)],
    Horse: [(9, 2), (9, 6)],
    Chariot: [(9, 0), (9, 8)],
    Elephant: [(9, 1), (9, 7)],
    Cannon: [(7, 1), (7, 7)],
    Pawn: [(6, 0), (6, 2), (6, 4), (6, 6), (6, 8)],
}

TOP_PIECES = {
    King: [(1, 4)],
    Advisor: [(0, 3), (0, 5)],
    Horse: [(0, 2), (0, 6)],
    Chariot: [(0, 0), (0, 8)],
    Elephant: [(0, 1), (0, 7)],
    Cannon: [(2, 1), (2, 7)],
    Pawn: [(3, 0), (3, 2), (3, 4), (3, 6), (3, 8)],

}

class Player():
    def __init__(self, board, team, position):
        self.piece_size = (75, 75)
        self.color = team
        self.pieces = []
        self.international = True
        self.turn = False
        self._init_pieces(board, position, team)
        self.add_pieces_to_board(board)

    def __str__(self):
        return self.color + '\n' + str(self.pieces)

    def piece_count(self) -> int:
        return len(self.pieces)

    def add_pieces_to_board(self, board):
        for piece in self.pieces:
            board.insert_piece(piece.location, piece)

    def _init_pieces(self, board, player_position, team):
        set = TOP_PIECES if player_position == Position.TOP else BOTTOM_PIECES

        for piece_class, positions in set.items():
            for pos in positions:
                render_pos = board.calculate_render_pos(pos)
                p = piece_class(pos,
                                render_pos,
                                self.piece_size,
                                team=team,
                                international=self.international)
                self.pieces.append(p)
        
    def render_peices(self, surface):
        for piece in self.pieces:
            piece.render(surface)

    def process(self, event, mouse_pos):
        for piece in self.pieces:
            piece.process(event, mouse_pos)

    def update_piece_size(self, size:tuple[int]):
        self.piece_size = size
        self.piece_offset = tuple([i/2 for i in self.piece_size]) # offset for piece rendering

if __name__ == '__main__':
    import pygame
    from board import Board
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    run = True

    board = Board(screen)
    board.update(screen)
    player = Player(board, 'cho', Position.BOTTOM)
    for piece in player.pieces:
        print(piece, piece.pos)
    print(player)
