import pygame, button, container

class Window:
    """
    A window that holds elements and will resize according to what's in it
    """
    def __init__(self, pos:tuple=(0,0), margin:int=10):
        self.pos = pos
        self.width = 0
        self.height = 0
        self.margin = margin
        self._container = container.VContainer(pos, margin=10)
        self._rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self._size = 0

    def add_item(self, item):
        # adjust width and height of window and reinit rect
        self._container.add_item(item)
        self.width = self._container.get_size()[0] + self.margin
        self.height = self._container.get_size()[1] + self.margin
        self._rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self._size += 1

    def process(self, event, mouse_pos):
        self._container.process(event, mouse_pos)

    def render(self, surface):
        pygame.draw.rect(surface, 'brown', self._rect)
        self._container.render(surface)