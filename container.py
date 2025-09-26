# container.py

class Container:
    """
    A parent class to be inherited by HContainer and Vcontainer.
    """
    def __init__(self):
        self.height, self.width = 0, 0
        self._items:list = []
        self.pos:tuple = (0,0)
        self.size:int = 0

    def process(self, event, mousepos):
        for item in self._items:
            try:
                item.process(event, mousepos)
            except Exception:
                pass

    def render(self, surface):
        for item in self._items:
            item.render(surface)

class VContainer(Container):
    """
    A container to put objects into for better organization and automatic placing.
    Objects will be placed on top of each other.
    """
    def __init__(self, pos:tuple=(0,0), margin:float=10):
        super().__init__()
        self.pos = pos
        self.margin = margin

    def add_item(self, item):
        self._items.append(item)
        x = item.pos[0] + self.pos[0]
        y = item.pos[1] + self.pos[1] + self.size * (item.height + self.margin)
        self._items[self.size].set_pos((x, y))
        self.size += 1

    def set_pos(self, pos:tuple[int,int]):
        self.pos = pos
        for i, item in enumerate(self._items):
            x = self.pos[0]
            y = self.pos[1] + i * (item.height + self.margin)
            item.set_pos((x, y))

    def get_size(self) -> tuple[float,float]:
        x = max([item.width for item in self._items])
        y = self._items[self.size-1].pos[1]-self.pos[1] + self._items[self.size-1].height
        return (x, y)
        

class HContainer(Container):
    """
    A container to put objects into for better organization and automatic placing.
    Objects will be placed beside each other.
    """
    def __init__(self, pos:tuple=(0,0), margin:float=10):
        super().__init__()
        self.margin = margin

    def add_item(self, item):
        self._items.append(item)
        x = item.pos[0] + self.pos[0] + self.size * (item.width + self.margin)
        y = item.pos[1] + self.pos[1]
        self._items[self.size].set_pos((x, y))
        self.size += 1

    def set_pos(self, pos:tuple[int,int]):
        self.pos = pos
        for i, item in enumerate(self._items):
            x = self.pos[0] + i * (item.width + self.margin)
            y = self.pos[1]
            item.set_pos((x, y))

    def get_size(self) -> tuple[float,float]:
        x = self._items[-1].pos[0]-self.pos[0] + self._items[-1].width
        print(x)
        y = max([item.height for item in self._items])
        return (x, y)