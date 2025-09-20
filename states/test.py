# test.py
from states.state import State
from timer import IncTimer
import container

class Test(State):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.hcontainer = container.HContainer()
        self.vcontainer = container.VContainer()

        self.hcontainer.add_item(IncTimer((0,0)))
        self.hcontainer.add_item(IncTimer((0,0)))

        self.vcontainer.add_item(self.hcontainer)
        self.vcontainer.add_item(IncTimer((0,0)))

    def process(self, event, mouse_pos):
        super().process(event, mouse_pos)
        self.vcontainer.process(event, mouse_pos)
        return super().process(event, mouse_pos)
    
    def render(self):
        self.vcontainer.render(self.screen)
        return super().render()