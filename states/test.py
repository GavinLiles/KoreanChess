# test.py
from states.state import State
from timer import IncTimer
import container, window, button

class Test(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.window = window.Window((0,0))
        self.window.add_item(IncTimer((0,0)))

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        self.window.process(event, mouse_pos)
        return super().process(event, mouse_pos)
    
    def render(self):
        self.window.render(self.screen)
        return super().render()