import pygame
from state import State
from button import TextButton

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