import pygame
from states.state import State
from board import Board, Side
from button import TextButton
from player import Player, Position
import container

class PregameSwap(State):
    def __init__(self, screen, manager):
        super().__init__( screen,manager)
        self.board = Board(self.screen)
        self.board.update(self.screen)

        self.cho_player = Player(self.board, 'cho', Position.BOTTOM)
        self.han_player = Player(self.board, 'han', Position.TOP)
        
        self.swap_buttons = container.HContainer(margin=100)

        # define buttons
        button_size = (150, 50)
        button_traits = {
            'swap left': lambda: self.board.swap(Side.LEFT),
            'confirm': lambda: self.move_to_game(),
            'swap right': lambda: self.board.swap(Side.RIGHT),
        }

        # init buttons in container
        for label, function in button_traits.items():
            self.swap_buttons.add_item(
                TextButton((0, 0), button_size, label, function)
            )
        x = self.screen_size[0]/2-self.swap_buttons.get_size()[0]/2
        y = self.screen_size[1]/2-self.swap_buttons.get_size()[1]/2
        self.swap_buttons.set_pos((x, y))

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        mouse_pos = pygame.mouse.get_pos()
        self.swap_buttons.process(event, mouse_pos)

        if event.type == pygame.VIDEORESIZE:
            self.screen_size = self.screen.get_size()
            self.background = pygame.transform.scale(pygame.image.load('assets/bg.jpg').convert(), self.screen_size)
            
            # update position of container since window resized 
            x = self.screen_size[0]/2-self.swap_buttons.get_size()[0]/2
            y = self.screen_size[1]/2-self.swap_buttons.get_size()[1]/2
            self.swap_buttons.set_pos((x, y))

    def render(self):
        self.board.update(self.screen)
        self.board.render(self.screen)
        self.swap_buttons.render(self.screen)

    def move_to_game(self):
        self.manager.change_state('game')
        self.manager.current_state.recieve_data([self.board, self.cho_player, self.han_player])