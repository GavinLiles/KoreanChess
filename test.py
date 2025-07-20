# test.py
from state import State
from timer import IncTimer

class Test(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.timer = IncTimer((500, 100))

    def process(self, event, mouse_pos):
        self.timer.process(event, mouse_pos)
        return super().process(event, mouse_pos)
    
    def render(self):
        self.timer.render(self.screen)
        return super().render()