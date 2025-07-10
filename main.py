import pygame
import os
from board import Board
from button import TextButton

class State:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.DEFAULT_FONT = pygame.font.SysFont('Arial', 50)
        self.screen = pygame.display.set_mode((1000, 1000))
        self.screen_size = pygame.display.get_surface().get_size() # size of screen
        self.run = False

    def set_active(self):
        self.run = True

    def set_inactive(self):
        self.run = False

    def is_active(self):
        return self.run

    def activate_state(self, state):
        state.set_active()

class MainMenu(State):
    def __init__(self):
        super().__init__() # call parent init
        self.settings_state = Settings() # init other states
        self.game = Game()
        self.buttons = []
        self.title = self.DEFAULT_FONT.render('Korean Chess', False, (0,0,0))
        
        button_size = (150, 100)
        x = (self.screen_size[0]/2)-(button_size[0]/2) # x position of button
        button_traits = {
            'play':self._goto_game,
            'settings':self._goto_settings,
            'exit':self._exit_game,
            'goo':self._exit_game
            }
        
        # create buttons from dict, add to list
        button_spacing = 110
        y_pos_factor = 1
        y_offset = 100
        for label, function in button_traits.items():
            y = y_offset + button_spacing * y_pos_factor
            self.buttons.append(TextButton((x, y), button_size, label, func=function))
            y_pos_factor += 1

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
        
        # render menu when MainMenu is only active
        if not (self.settings_state.is_active() or self.game.is_active()):
            self.render()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            # process buttons
            if self.settings_state.is_active():
                self.settings_state.process(event, mouse_pos)
            elif self.game.is_active():
                self.game.process(event, mouse_pos)
            else:
                for button in self.buttons:
                    button.process(event, mouse_pos)

    def render(self):
        pygame.draw.rect(self.screen, (255,255,0), (0, 0, self.screen_size[0], self.screen_size[1]))
        for button in self.buttons:
            button.render(self.screen)

        # render title
        title_size = self.DEFAULT_FONT.size('Korean Chess')
        self.screen.blit(self.title, (self.screen_size[0]/2-(title_size[0]/2), 100))

    def _exit_game(self):
        self.set_inactive()

    def _goto_settings(self):
        self.activate_state(self.settings_state)

    def _goto_game(self):
        self.activate_state(self.game)

class Settings(State):
    def __init__(self):
        super().__init__()
        button_size = (150, 100)
        x = (self.screen_size[0]/2)-(button_size[0]/2)
        self.return_button = TextButton((x, 100), button_size, 'return', func=self._return_to_main)

    def _return_to_main(self):
        self.set_inactive()

    def process(self, event, mouse_pos):
        pygame.draw.rect(self.screen, (255,0,0), (0, 0, self.screen_size[0], self.screen_size[1]))
        self.return_button.render(self.screen)

        if event.type == pygame.QUIT:
            print(self.b.background.get_size())
            self.b.print_grid()
            return False

        self.return_button.process(event, mouse_pos)

    def render(self):
        pass

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
            self.b.print_grid()
            return False
        
        for piece in self.b.pieces:
            piece.process(self.b, event, mouse_pos)


if __name__ == '__main__':
    run = True
    main_menu = MainMenu()
    main_menu.set_active()

    while run:
        if main_menu.is_active():
            main_menu.process()
        else:
            run = False

    pygame.quit()