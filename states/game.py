import pygame
from states.state import State
from board import Board
from player import Player, Position

class Game(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.board = Board(self.screen)
        self.board.update(self.screen)
        self.players = {
            'cho': Player(self.board, 'cho', Position.BOTTOM),
            'han': Player(self.board, 'han', Position.TOP)
        }
        self.current_player = 'han'
        self.piece_count = self.board.piece_count()

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        
        for piece in self.players[self.current_player].pieces:
            valid_move, captured_piece = piece.process(self.board, event, mouse_pos)
            
            # if move made, swap turn
            if valid_move:
                for player in ('cho', 'han'):
                    if captured_piece in self.players[player].pieces:
                        self.players[player].pieces.remove(captured_piece)
                        self.players[player].captured_pieces.append(captured_piece)

                # self._swap_turn()

    def render(self):
        self.board.render(self.screen)

    def _swap_turn(self):
        self.current_player = 'han' if self.current_player == 'cho' else 'cho'
        print('cho count:', len(self.players['cho'].pieces), 'han count:', len(self.players['han'].pieces))
        print('total piece count:', self.board.piece_count())
        print()

    def recieve_data(self, data=None):
        if data: self.board, self.players['cho'], self.players['han'] = data
        else: print('nothing was recieved')