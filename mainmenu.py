import pygame
from button import TextButton
from game import Game
from state import State
from settings import Settings

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