# piece.py
# contains the definition of the piece class
from button import *

class Piece(TextureButton):
    def __init__(self, surface, x, y, width, height, image_file):
        super().__init__(surface, x, y, width, height, image_file)
        self.value = 0       # the value the piece is worth
        self.team = None     # team of the piece
        self.location = None # where the piece is located on the board

    def get_team(self):
        return self.team
    
    def get_location(self):
        return self.location
    
    def get_value(self):
        return self.value
    
class Pawn(Piece):
    def __init__(self, surface, x, y, width, height, image_file):
        super().__init__(surface, x, y, width, height, image_file)