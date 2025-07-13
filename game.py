import pygame
from state import State
from board import Board

class Game(State):
    def __init__(self):
        super().__init__()
        self.b = Board(self.screen)
        self.b.update(self.screen)

    def process(self, event, mouse_pos):
        mouse_pos = pygame.mouse.get_pos()
        self.b.render(self.screen)

        if event.type == pygame.QUIT:
            print(self.b.background.get_size())
            print(self.b)
            return False
        
        for piece in self.b.cho_player.pieces:
            piece.process(self.b, event, mouse_pos)
