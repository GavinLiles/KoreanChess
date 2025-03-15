# test.py
from piece import *

class Board():

    def __init__(self):
        self.background = pygame.image.load('assets/Janggi_Board.png').convert()
        self.grid = [ [None] * 10 for _ in range(9)]

    def __str__(self):
        return 'Board'

    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end=' ')
            print()

    def insert_piece(self, pos:list, item):
        self.grid[pos[0]][pos[1]] = item

    def render(self, surface):
        board_size = surface.get_size()

        # if window isnt square, keep board a square
        if board_size[0] != board_size[1]:
            small_side = min(board_size)
            board_size = (small_side, small_side)

        self.background = pygame.transform.smoothscale(self.background, board_size)
        surface.blit(self.background, (0, 0))

    def __render_pieces(self):
        for row in self.grid:
            for piece in row:
                if piece is None:
                    break
                piece.render()

if __name__ == '__main__':
    import pygame
    import os

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    run = True

    b = Board()
    b.render(screen)

    board_size = b.background.get_size()
    print(board_size)
    piece_size = (50, 50)
    move_scale = [pos/ind + 5 for pos, ind in zip(board_size, (9, 10))]
    grid_pos = (8, 9)
    piece_pos = [x*y-(z/2) for x, y, z in zip(move_scale, grid_pos, piece_size)]

    p = Pawn(piece_pos, piece_size, 'cho')
    b.insert_piece(grid_pos, p)

    while run:
        mouse_pos = pygame.mouse.get_pos()
        b.render(screen)
        p.render(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                print(b.background.get_size())
            
            p.process(event, mouse_pos)

        pygame.display.update()

    # Quit Pygame
    pygame.quit()