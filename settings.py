import pygame
from state import State
from button import TextButton
from text import Text

class Settings(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        board_filenames = {
            'old':   'Janggi_Board.png',
            'brown': 'JanggiBrown.svg',
            'orange':'JanggiOrange.svg',
            'stone': 'JanggiStone.svg',
            'dark':  'JanggiWoodDark.svg',
            'wood':  'JanggiWood.svg',
        }
        board_select_button_traits = {
            name: (lambda path=path: self.manager.states['game'].board.change_board(f'assets/boards/{path}'))
            for name, path in board_filenames.items()
        }

        button_size = (100, 75)
        x_pos, y_pos = 0, 200
        button_spacing = button_size[0]+10
        width_of_row = (button_size[0] + button_spacing) * len(board_select_button_traits)
        offset = (self.screen_size[0]-(width_of_row//2)) // 2

        self.board_select_buttons = []
        for i, (label, function) in enumerate(board_select_button_traits.items()):
            x_pos = (button_spacing * i) + offset
            self.board_select_buttons.append(
                TextButton((x_pos, y_pos), button_size, label, func=function))

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
        
        for button in self.board_select_buttons:
            button.process(event, mouse_pos)

        self.return_button.process(event, mouse_pos)

    def render(self):
        pygame.draw.rect(self.screen, 'grey', (0, 0, self.screen_size[0], self.screen_size[1]))
        
        self.return_button.render(self.screen)
        for button in self.board_select_buttons:
            button.render(self.screen)
        
        self.text.render(self.screen, (self.screen_size[0]/2-(self.text.size[0]/2), 100))
        
        # rendering board
        self.board_preview = pygame.transform.scale_by(self.manager.states['game'].board.background, .25)
        board_size = self.board_preview.get_size()
        pos = (self.screen_size[0]//2-board_size[0]//2, 300) # x is centered w/ screen
        self.screen.blit(self.board_preview, pos)
