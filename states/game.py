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
        self.current_player = 'cho'
        self.piece_count = self.board.piece_count()

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        
        for piece in self.players[self.current_player].pieces:
            # if move made, swap turn
            if piece.process(self.board, event, mouse_pos): # NOTE: process returns true if valid move made
                print('piece has been captured') if self.piece_count != self.board.piece_count() else None
                self._swap_turn()


    def render(self):
        self.board.render(self.screen)

    def _swap_turn(self):
        self.current_player = 'han' if self.current_player == 'cho' else 'cho'

    def recieve_data(self, data=None):
        if data: self.board, self.players['cho'], self.players['han'] = data
        else: print('nothing was recieved')