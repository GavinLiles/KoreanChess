import pygame
from states.state import State
from board import Board, Side
from button import TextButton
from player import Player, Position

class PregameSwap(State):
    def __init__(self, screen, manager):
        super().__init__( screen,manager)
        self.board = Board(self.screen)
        self.board.update(self.screen)

        self.cho_player = Player(self.board, 'cho', Position.BOTTOM)
        self.han_player = Player(self.board, 'han', Position.TOP)

        button_size = (150, 50)
        button_traits = {
            'swap left': lambda: self.board.swap(Side.LEFT),
            'confirm': lambda: self.move_to_game(),
            'swap right': lambda: self.board.swap(Side.RIGHT),
        }
        self.swap_buttons = [
            TextButton((i*(self.screen_size[0]//3) + 100, 500), button_size, text, function) 
            for i, (text, function) in enumerate(button_traits.items())
        ]

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        mouse_pos = pygame.mouse.get_pos()

        for button in self.swap_buttons: button.process(event, mouse_pos)

    def render(self):
        self.board.update(self.screen)
        self.board.render(self.screen)
        for button in self.swap_buttons: button.render(self.screen)

    def move_to_game(self):
        self.manager.change_state('game')
        self.manager.current_state.recieve_data([self.board, self.cho_player, self.han_player])