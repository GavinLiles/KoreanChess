import pygame
from states.state import State
from board import Board
from piece import King
from player import Player, Position
import window

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
        self.player_in_check = None
        self.bikjang_initiator = None
        self.piece_count = self.board.piece_count()
        self.game_end = False

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        
        # process each piece
        for piece in self.players[self.current_player].pieces:
            
            # if player is in check, only allow for king to move,
            # otherwise, any piece can be moved
            if (not self.player_in_check) or (self.player_in_check and isinstance(piece, King)):
                valid_move, captured_piece = piece.process(self.board, event, mouse_pos)
            
            # check for a check or bikjang
            if isinstance(piece, King):
                if piece.is_in_check(self.board):
                    self.player_in_check = piece.team
                
                # if king is in bikjang and bikjang is not active
                elif piece.is_in_bikjang(self.board) and not self.bikjang_initiator:
                    self.bikjang_initiator = self.current_player
                    print(self.current_player, 'initiated bikjang')

                # if king is in bikjang and bikjang is already active
                elif piece.is_in_bikjang(self.board) and self.bikjang_initiator != self.current_player:
                    print('game ended')

            # if move made, capture pieces as necessary and swap turn
            if valid_move:
                for player in ('cho', 'han'):
                    if captured_piece in self.players[player].pieces:
                        self.players[player].pieces.remove(captured_piece)
                        self.players[player].captured_pieces.append(captured_piece)
                self._swap_turn()

        if event.type == pygame.VIDEORESIZE:
            self.board.update(self.screen)


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