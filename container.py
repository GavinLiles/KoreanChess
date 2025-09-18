# container.py

class Container:
    """A class to store objects into"""
    def __init__(self, pos:tuple=(0,0), item_spacing:float=10, y_margin:float=10):
        self._items:list = []
        self._pos:tuple = pos
        self.size:int = 0
        self.y_margin = y_margin

    def process(self, event, mouse_pos):
        for item in self._items:
            item.process(event, mouse_pos)

    def render(self, surface):
        for item in self._items:
            item.render(surface)

    def get_size(self) -> tuple[float,float]:
        x = max([item.width for item in self._items])
        y = self._items[self.size-1].pos[1]-self._pos[1]
        return (x, y)

    def add_item(self, item):
        self._items.append(item)
        x = item.pos[0] + self._pos[0]
        y = item.pos[1] + self._pos[1] + self.size * (item.height + self.y_margin)
        self._items[self.size].update_pos((x, y))
        self.size += 1

    def set_pos(self, pos:tuple[int,int]):
        self._pos = pos
        for i, item in enumerate(self._items):
            x = self._pos[0]
            y = self._pos[1] + i * (item.height + self.y_margin)
            item.update_pos((x, y))