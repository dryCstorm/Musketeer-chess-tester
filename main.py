import pygame
import library.chess.musketeer as Musketeer
import res
import library.chess as Chess
import utils
import math
from renderergame import BoardRendererGame
from renderersetting import BoardRendererSetting

pygame.init()
pygame.display.set_caption("Musketeer Chess")
game_clock = pygame.time.Clock()

    
SETTING_STATE_NONE = 1
SETTING_STATE_OK = 2
SETTING_STATE_CANCEL = 3

BETZA = ["W", "D", "H", "F", "A", "G", "N", "L", "J"]
UN_AVAILABLE_LETTERS = ["P", "K", "Q", "R", "B", "N"]
ICON_COUNT = 26

selected_pieces = [[None] * (len(BETZA) + 2), [None] * (len(BETZA) + 2)]
def select_piece():
    boardrenderer = BoardRendererSetting(pygame)
    setting_state = SETTING_STATE_NONE
    wip_piece = 0
    
    boardrenderer.clear()
    
    while setting_state != SETTING_STATE_OK and setting_state != SETTING_STATE_CANCEL:
        boardrenderer.clear()
        boardrenderer.draw_board()
        for i in range (0, len(selected_pieces)):
            boardrenderer.draw_head (i, selected_pieces [i][0], i == wip_piece)
        
        boardrenderer.draw_icon_selector(selected_pieces [wip_piece][0])
        
        letter = selected_pieces [wip_piece][1]
        letter_available = True
        if letter != None and utils.number_to_upper_char(letter) in UN_AVAILABLE_LETTERS:
            letter_available = False
        
        elif letter != None and any(one [1] == letter and index != wip_piece for index, one in enumerate (selected_pieces)):
            letter_available = False
            
        boardrenderer.draw_letter_selector(utils.number_to_upper_char(letter), letter_available)
        if selected_pieces [wip_piece][0]:
            boardrenderer.draw_piece_center(selected_pieces [wip_piece][0])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting_state = SETTING_STATE_CANCEL
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boardrenderer.is_back(pos):
                    if selected_pieces [wip_piece][0] == None:
                        selected_pieces [wip_piece][0] = 26
                    else:
                        selected_pieces [wip_piece][0] = (selected_pieces [wip_piece][0] + 24) % 26 + 1
                elif boardrenderer.is_forward(pos):
                    if selected_pieces [wip_piece][0] == None:
                        selected_pieces [wip_piece][0] = 1
                    else:
                        selected_pieces [wip_piece][0] = selected_pieces [wip_piece][0] % 26 + 1
                elif boardrenderer.is_letter_back(pos):
                    if selected_pieces [wip_piece][1] == None:
                        selected_pieces [wip_piece][1] = 26
                    else:
                        selected_pieces [wip_piece][1] = (selected_pieces [wip_piece][1] + 24) % 26 + 1
                elif boardrenderer.is_letter_forward(pos):
                    if selected_pieces [wip_piece][1] == None:
                        selected_pieces [wip_piece][1] = 1
                    else:
                        selected_pieces [wip_piece][1] = selected_pieces [wip_piece][1] % 26 + 1                    
                elif boardrenderer.is_head(pos, len(selected_pieces)) != None:
                    wip_piece = boardrenderer.is_head(pos, len(selected_pieces))
                    
                
        pygame.display.flip()
        game_clock.tick(60)
        
        
    
    
GAME_STATE_PLAYING = 1
GAME_STATE_FINISHED = 2

USER_STATE_NONE = 1
USER_STATE_SELECTED = 2

icon_mapper = {
    "E": "5",
    "U": "7",
}
def play_game ():
    boardrenderer = BoardRendererGame(pygame)
    boardrenderer.clear()
    
    custom_pieces = [{"name":"Elephant", "letter":"E", "betza":"fhHfrlRK", "position":[3, 2]},
                     {"name":"Unicorn","letter":"U","betza":"NK","position": [6, 4]}]
    
    board = Musketeer.MusketeerBoard(custom_pieces)
    game_state = GAME_STATE_PLAYING
    user_state = USER_STATE_NONE
    custom_pieces = [(),()]
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
        for square in Chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                pieces.append((str(piece), square % 8 + 1, math.floor(square / 8) + 1))
        
        for musketeer in board.inplaced_musketeer_pieces():
            pieces.append(musketeer)
        
        
        return pieces
                
    running = True
    
    while running:
        movable_pieces = get_movable_pieces()
        movable_pieces_from = None if user_state != USER_STATE_SELECTED else get_movable_pieces_from(selected_piece)
        
        # Drawing
        boardrenderer.draw_board()
        boardrenderer.draw_pieces(get_pieces (), icon_mapper)
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
    select_piece()
    play_game()