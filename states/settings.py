import pygame
from states.state import State
from button import TextButton
from text import Text
import container

class Settings(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.board_buttons = container.HContainer(margin=10)
        self.v_container = container.VContainer(margin=10)

        # making button functions. they change the file used on the board
        board_filenames = {
            'old':   'Janggi_Board.png',
            'brown': 'JanggiBrown.svg',
            'orange':'JanggiOrange.svg',
            'stone': 'JanggiStone.svg',
            'dark':  'JanggiWoodDark.svg',
            'wood':  'JanggiWood.svg',
        }
        board_select_button_traits = {
            name: (lambda path=path: self.manager.states['pregame_swap'].board.change_board(f'assets/boards/{path}'))
            for name, path in board_filenames.items()
        }

        # init board_buttons
        button_size = (100, 75)
        for label, function in board_select_button_traits.items():
            self.board_buttons.add_item(TextButton((0, 0), button_size, label, function))

        x = self.screen_size[0]/2 - self.board_buttons.get_size()[0]/2
        y = self.screen_size[1]/5 - self.board_buttons.get_size()[1]/2
        self.board_buttons.set_pos((x,y))

        button_size = (125, 50)
        x, y = (self.screen_size[0]/2)-(button_size[0]/2), 900
        self.return_button = TextButton(
            (x, y),
            button_size,
            'return',
            func=lambda: self.manager.change_state('main_menu'))
        
        self.text = Text('Board selection')

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        
        self.board_buttons.process(event, mouse_pos)
        self.return_button.process(event, mouse_pos)

        if event.type == pygame.VIDEORESIZE:
            x = self.screen_size[0]/2 - self.board_buttons.get_size()[0]/2
            y = self.screen_size[1]/5 - self.board_buttons.get_size()[1]/2
            self.board_buttons.set_pos((x,y))

    def render(self):
        pygame.draw.rect(self.screen, 'grey', (0, 0, self.screen_size[0], self.screen_size[1]))
        
        self.return_button.render(self.screen)
        self.board_buttons.render(self.screen)
        
        self.text.render(self.screen, (self.screen_size[0]/2-(self.text.size[0]/2), 100))
        
        # rendering board
        self.board_preview = pygame.transform.scale_by(self.manager.states['pregame_swap'].board.background, .25)
        board_size = self.board_preview.get_size()
        pos = (self.screen_size[0]//2-board_size[0]//2, 300) # x is centered w/ screen
        self.screen.blit(self.board_preview, pos)
