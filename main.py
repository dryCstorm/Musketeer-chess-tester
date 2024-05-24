import pygame
import res
from renderer import BoardRenderer



pygame.init()
pygame.display.set_caption("Musketeer Chess")
game_clock = pygame.time.Clock()
boardrenderer = BoardRenderer(pygame)

def select_piece ():
    1
    

def play_game ():
    boardrenderer.clear()
    boardrenderer.draw_board()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        game_clock.tick(60)

if __name__ == "__main__":
    pygame.display.flip()
    play_game()