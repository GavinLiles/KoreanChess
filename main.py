import pygame
import os
from board import Board
from button import TextButton

class State:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))#, pygame.RESIZABLE)
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
        size = pygame.display.get_surface().get_size() # size of screen
        self.settings_state, self.game = Settings(), Game() # init other states
        self.buttons = []
        button_size = (150, 100)
        x = (size[0]/2)-(button_size[0]/2) # x position of button
        button_traits = {'play':self._goto_game, 'settings':self._goto_settings, 'exit':self._exit_game}
        i = 1 # iter for y position of button
        
        # create buttons
        for label, function in button_traits.items():
            y = 100*i + 10*i
            self.buttons.append(TextButton((x, y), button_size, label, func=function))
            i += 1

    def _exit_game(self):
        self.set_inactive()

    def _goto_settings(self):
        self.activate_state(self.settings_state)

    def _goto_game(self):
        self.activate_state(self.game)

    def process(self):
        WIND_SIZE = pygame.display.get_window_size()
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
        
        # render buttons
        # render menu when MainMenu is only active
        if not (self.settings_state.is_active() or self.game.is_active()):
            pygame.draw.rect(self.screen, (255,255,0), (0, 0, WIND_SIZE[0], WIND_SIZE[1]))
            for button in self.buttons:
                button.render(self.screen)

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


class Settings(State):
    def __init__(self):
        super().__init__()
        size = pygame.display.get_surface().get_size() # size of screen
        button_size = (150, 100)
        x = (size[0]/2)-(button_size[0]/2)
        self.return_button = TextButton((x, 100), button_size, 'return', func=self._return_to_main)

    def _return_to_main(self):
        self.set_inactive()

    def process(self, event, mouse_pos):
        WIND_SIZE = pygame.display.get_window_size()
        pygame.draw.rect(self.screen, (255,0,0), (0, 0, WIND_SIZE[0], WIND_SIZE[1]))
        self.return_button.render(self.screen)

        if event.type == pygame.QUIT:
            print(self.b.background.get_size())
            self.b.print_grid()
            return False

        self.return_button.process(event, mouse_pos)

class Game(State):
    def __init__(self):
        super().__init__()
        self.b = Board(self.screen)
        self.b.render(self.screen)

    def process(self, event, mouse_pos):
        mouse_pos = pygame.mouse.get_pos()
        self.b.render(self.screen)

        if event.type == pygame.QUIT:
            print(self.b.background.get_size())
            self.b.print_grid()
            return False

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if width < WIDTH_LIMIT_MIN:
                width = WIDTH_LIMIT_MIN
            if height < HEIGHT_LIMIT_MAX:
                height = HEIGHT_LIMIT_MAX
            screen = pygame.display.set_mode((width, height),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            self.b.update(self.screen)

        
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