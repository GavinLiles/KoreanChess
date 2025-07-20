import pygame
from state import State
from board import Board

class Game(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.board = Board(self.screen)
        self.board.update(self.screen)

    def process(self, event, mouse_pos):
        mouse_pos = pygame.mouse.get_pos()
        self.board.render(self.screen)

        if event.type == pygame.QUIT:
            print(self.board.background.get_size())
            print(self.board)
            return False
        
        for piece in self.board.cho_player.pieces:
            piece.process(self.board, event, mouse_pos)

    def render(self):
        self.board.render(self.screen)

    def recieve_data(self, data=None):
        if data: self.board = data
        else: print('nothing was recieved')