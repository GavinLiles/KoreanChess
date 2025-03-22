# test.py
from piece import *

class Board():

    def __init__(self, surface):
        self.background = pygame.image.load('assets/Janggi_Board.png').convert()
        self.grid = [ [None] * 9 for _ in range(10)] # array representation of board
        self.pieces = [] # NOTE: probably temp variable. will be replaced by player object
        self.__board_size = self.background.get_size()
        self.__row_spacing = self.__board_size[0] / 8
        self.__col_spacing = self.__board_size[1] / 9
        self.__piece_size = (50, 50)
        self.__piece_offset = tuple([i/2 for i in self.__piece_size]) # offset for piece rendering
        self.SCREEN_CENTER = [i-(j/2) for i, j in zip(surface.get_rect().center, self.__board_size)]
        self.init_pieces()

    def __calculate_render_pos(self, grid_position:tuple[int]):
        x = grid_position[1]*self.__row_spacing-(self.__piece_offset[0]) + self.SCREEN_CENTER[0]
        y = grid_position[0]*self.__col_spacing-(self.__piece_offset[0]) + self.SCREEN_CENTER[1]
        return (x, y)

    def init_pieces(self):
        # KING
        pos = (8,4)
        render_pos = self.__calculate_render_pos(pos)
        p = King(render_pos, self.__piece_size, team='cho')
        self.pieces.append(p)
        self.insert_piece(pos, p)

        # ADVISOR
        for pos in [(9,3), (9,5)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Advisor(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

        # HORSE
        for pos in [(9,2), (9,6)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Horse(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

        # CHARIOT
        for pos in [(9,0), (9,8)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Chariot(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

        # ELEPHANT
        for pos in [(9,1), (9,7)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Elephant(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

        # CANNON
        for pos in [(7,1), (7,7)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Cannon(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

        # PAWN
        for pos in [(6,0), (6,2), (6,4), (6,6), (6,8)]:
            render_pos = self.__calculate_render_pos(pos)
            p = Pawn(render_pos, self.__piece_size, team='cho')
            self.pieces.append(p)
            self.insert_piece(pos, p)

    def __str__(self):
        return 'Board'

    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end=' ')
            print()

    def insert_piece(self, pos:tuple[int], item):
        try:
            self.grid[pos[0]][pos[1]] = item
        except IndexError:
            print(f'given index {pos} is not within bounds.')

    def upadte_board_size(self):
        self.__board_size = self.background.get_size()
    
    def upadte_piece_spacing(self):
        self.__row_spacing = self.__board_size[0] / 8
        self.__col_spacing = self.__board_size[1] / 9

    def update_piece_positions(self):
        # STOPPING POINT
        # trying to figure out how to update the position of all the pieces
        # in the peices list so they stay on the board if the board is moved.
        pass

    def update_screen_center(self, surface):
        self.SCREEN_CENTER = [i-(j/2) for i, j in zip(surface.get_rect().center, self.__board_size)]

    def render(self, surface):
        self.__render_board(surface)
        self.__render_pieces(surface)

    def __render_pieces(self, surface):
        for piece in self.pieces:
            piece.render(surface)

    def __render_board(self, surface):
        board_pos = [i-(j/2) for i, j in zip(surface.get_rect().center, self.__board_size)]
        surface.blit(self.background, board_pos)


if __name__ == '__main__':
    import pygame
    import os

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    run = True

    b = Board(screen)

    while run:
        mouse_pos = pygame.mouse.get_pos()
        b.render(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                print(b.background.get_size())
            
            for piece in b.pieces:
                piece.process(event, mouse_pos)

        pygame.display.update()
        b.update_screen_center(screen)


    # Quit Pygame
    pygame.quit()
