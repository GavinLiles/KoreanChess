import pygame, button, container

class Window:
    """
    A window that holds elements and will resize according to what's in it
    """
    def __init__(self, pos:tuple=(0,0), margin:int=10):
        self.pos = pos
        self.container = container.VContainer(pos, margin=10)

        self.container.add_item(button.TextButton(pos=(0,0), text="testing", size=(75,20)))

        self.width = self.container.get_size()[0] + margin
        self.height = self.container.get_size()[1] + margin
        print(self.container.get_size())
        self._rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def process(self, event, mouse_pos):
        self.container.process(event, mouse_pos)

    def render(self, surface):
        pygame.draw.rect(surface, 'grey', self._rect)
        self.container.render(surface)