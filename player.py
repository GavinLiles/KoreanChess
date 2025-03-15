# player.py
from piece import *

def f():
    print("click")

class Player():
    def __init__(self, color):
        self.PIECE_SIZE = (50, 50)
        self.color = color
        self.__init_pieces()

    def __init_pieces(self):
        self.pieces = []
        for i in range(4):
            self.pieces.append(Pawn([(100 + i*50), 100], self.PIECE_SIZE, f, self.color))
        for i in range(2):
            self.pieces.append(Chariot ([(100 + i*100), 150], self.PIECE_SIZE, f, self.color))
            self.pieces.append(Horse   ([(100 + i*100), 200], self.PIECE_SIZE, f, self.color))
            self.pieces.append(Elephant([(100 + i*100), 250], self.PIECE_SIZE, f, self.color))
            self.pieces.append(Cannon  ([(100 + i*100), 300], self.PIECE_SIZE, f, self.color))
            self.pieces.append(Advisor ([(100 + i*100), 350], self.PIECE_SIZE, f, self.color))

    def render_peices(self, surface):
        for piece in self.pieces:
            piece.render(surface)

    def process_pieces(self, event, mouse_pos):
        for piece in self.pieces:
            piece.process(event, mouse_pos)

if __name__ == '__main__':
    import pygame
    import os

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    background = pygame.image.load('assets/Janggi_Board.png').convert()
    run = True
        
    player = Player('cho')

    while run:
        background = pygame.transform.smoothscale(background, screen.get_size())
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        player.render_peices(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            player.process_pieces(event, mouse_pos)
            

        pygame.display.update()

    # Quit Pygame
    pygame.quit()