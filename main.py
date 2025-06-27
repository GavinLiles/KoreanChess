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
        self.play = TextButton((100, 100), (100, 100), 'play', func=self._goto_game)
        self.settings = TextButton((100, 210), (100, 100), 'settings', func=self._goto_settings)
        self.exit = TextButton((100, 320), (100, 100), 'exit', func=self._exit_game)
        self.settings_state = Settings()
        self.game = Game()

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
        
        if not (self.settings_state.is_active() or self.game.is_active()):
            pygame.draw.rect(self.screen, (255,255,0), (0, 0, WIND_SIZE[0], WIND_SIZE[1]))
            self.play.render(self.screen)
            self.settings.render(self.screen)
            self.exit.render(self.screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            if self.settings_state.is_active():
                self.settings_state.process(event, mouse_pos)
            elif self.game.is_active():
                self.game.process(event, mouse_pos)
            else:
                self.play.process(event, mouse_pos)
                self.settings.process(event, mouse_pos)
                self.exit.process(event, mouse_pos)

class Settings(State):
    def __init__(self):
        super().__init__()
        self.return_button = TextButton((100, 100), (100, 100), 'return', func=self._return_to_main)

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