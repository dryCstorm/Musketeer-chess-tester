import pygame
import chess.musketeer
import res
import chess
import utils
import math
from renderer import BoardRenderer

pygame.init()
pygame.display.set_caption("Musketeer Chess")
game_clock = pygame.time.Clock()
boardrenderer = BoardRenderer(pygame)

def selected_piece ():
    1
    
GAME_STATE_PLAYING = 1
GAME_STATE_FINISHED = 2

USER_STATE_NONE = 1
USER_STATE_SELECTED = 2

def play_game ():
    boardrenderer.clear()
    board = chess.musketeer.MusketeerBoard()
    game_state = GAME_STATE_PLAYING
    user_state = USER_STATE_NONE
    selected_piece = (0,0)
    
    def get_movable_pieces ():
        moves = []
        for move in board.legal_moves:
            uci = move.uci()
            x = utils.char_to_number(uci [0:1])
            y = int(uci [1:2])
            moves.append((x, y))
        
        return moves
    
    def get_movable_pieces_from (piece):
        moves = []
        for move in board.legal_moves:
            uci = move.uci()
            sx = utils.char_to_number(uci [0:1])
            sy = int(uci [1:2])
            ex = utils.char_to_number(uci [2:3])
            ey = int(uci [3:4])
            if sx == piece [0] and sy == piece [1]:
                moves.append((ex, ey))
        
        return moves
    
    def get_pieces ():
        pieces = []
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                pieces.append((str(piece), square % 8 + 1, math.floor(square / 8) + 1))
                
        return pieces
                
    running = True
    
    while running:
        movable_pieces = get_movable_pieces()
        movable_pieces_from = None if user_state != USER_STATE_SELECTED else get_movable_pieces_from(selected_piece)
        
        # Drawing
        boardrenderer.draw_board()
        boardrenderer.draw_pieces(get_pieces ())
        if game_state == GAME_STATE_PLAYING:
            if user_state == USER_STATE_NONE:
                boardrenderer.highlight_piece_normal(movable_pieces)
            if user_state == USER_STATE_SELECTED:
                boardrenderer.highlight_piece_weak(movable_pieces)
                boardrenderer.highlight_piece_selected([selected_piece])
                boardrenderer.highlight_piece_normal(movable_pieces_from)
                
        # Event Handling
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_state == USER_STATE_NONE:
                    pos = boardrenderer.get_board_position(pygame.mouse.get_pos())
                    if pos != None and pos in movable_pieces:
                        user_state = USER_STATE_SELECTED
                        selected_piece = pos
                elif user_state == USER_STATE_SELECTED:
                    pos = boardrenderer.get_board_position(pygame.mouse.get_pos())
                    if pos != None and pos in movable_pieces:
                        user_state = USER_STATE_SELECTED
                        selected_piece = pos
                    elif pos != None and pos in movable_pieces_from:
                        board.push_uci(f'{utils.number_to_char(selected_piece [0])}{selected_piece [1]}{utils.number_to_char(pos [0])}{pos [1]}')
                        user_state = USER_STATE_NONE
                        
                

        
        pygame.display.flip()
        game_clock.tick(60)
    

if __name__ == "__main__":
    pygame.display.flip()
    play_game()