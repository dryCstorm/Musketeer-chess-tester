import pygame
import library.chess.musketeer as Musketeer
import library.chess.pgn as pgn
import res
import library.chess as Chess
import utils
import math
from renderergame import BoardRendererGame
from renderersetting import BoardRendererSetting
import tkinter as tk
from tkinter import filedialog

pygame.init()
pygame.display.set_caption("Musketeer Chess")
game_clock = pygame.time.Clock()

    
SETTING_STATE_NONE = 1
SETTING_STATE_OK = 2
SETTING_STATE_CANCEL = 3

# F/B/L/R, S/H, LEN, C/M, G/P, J/N
BETZA = [("W", True, False, True, False, True, True), 
         ("D", True, False, True, True, True, True), 
         ("H", True, False, True, True, True, True), 
         ("F", True, False, True, True, True, True), 
         ("A", True, False, True, True, True, True), 
         ("G", True, False, True, True, True, True), 
         ("N", True, True, False, True, False, False), 
         ("L", True, True, False, True, False, False), 
         ("J", True, True, False, True, False, False)]

UN_AVAILABLE_LETTERS = ["P", "K", "Q", "R", "B", "N"]
ICON_COUNT = 26

selected_pieces = [[None, None, []], [None, None, []]]

def build_betja (settings):
    res = ""
    for setting in settings:
        sub = ""
        for i in range (1, 7):
            if i != 3 and BETZA [setting [0]][i]:
                sub += setting [i].lower()
        sub += BETZA [setting[0]][0]
        if BETZA[setting [0]][3] and setting [3] != 7:
            sub += str(setting [3])
        res += sub
    return res


def save_file_dialog():
   root = tk.Tk()
   root.withdraw()  # Hide the main Tkinter window
    
   file_path = filedialog.asksaveasfilename(defaultextension='.pgn', filetypes=[("Text files", "*.txt, *.pgn"), ("All files", "*.*")])
   return file_path

def load_file_dialog():
   root = tk.Tk()
   root.withdraw()  # Hide the main Tkinter window
    
   file_path = filedialog.askopenfilename(initialdir="./")
   return file_path

setting_state = SETTING_STATE_NONE

def select_piece():
    boardrenderer = BoardRendererSetting(pygame)
    global setting_state
    setting_state = SETTING_STATE_NONE
    wip_piece = 0
    
    boardrenderer.clear()
    
    while setting_state != SETTING_STATE_OK and setting_state != SETTING_STATE_CANCEL:
        boardrenderer.clear()
        boardrenderer.draw_board()
        for i in range (0, len(selected_pieces)):
            boardrenderer.draw_head (i, selected_pieces [i][0], build_betja(selected_pieces [i][2]), i == wip_piece)
        
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
            
        for index, movement_setting in enumerate(selected_pieces [wip_piece][2]):
            boardrenderer.draw_movement_setting(index, movement_setting, BETZA)
        boardrenderer.draw_new_movement_button(len(selected_pieces [wip_piece][2]))
        boardrenderer.draw_start_button()
        
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
                elif boardrenderer.is_new_button(pos, len(selected_pieces [wip_piece][2])):
                    selected_pieces [wip_piece][2].append([0, "", "", 7, "", "", ""])
                elif boardrenderer.is_start_button(pos):
                    setting_state = SETTING_STATE_OK
                else:
                    for index, movement_setting in enumerate(selected_pieces [wip_piece][2]):
                        button = boardrenderer.is_setting_button (pos, index, movement_setting, BETZA)
                        if button != None:
                            if button == "REMOVE":
                                selected_pieces [wip_piece][2].pop(index)
                            if button == "BL":
                                movement_setting[0] = (movement_setting[0] - 1 + len(BETZA)) % len(BETZA)
                            if button == "BR":
                                movement_setting[0] = (movement_setting[0] + 1) % len(BETZA)
                            if button == "L" or button == "R" or button == "F" or button == "B":
                                if button in movement_setting[1]:
                                    movement_setting[1] = movement_setting[1].replace(button, "")
                                else:
                                    movement_setting[1] += button
                            if button == "SH":
                                if movement_setting [2] == "S":
                                    movement_setting [2] = "H"
                                elif movement_setting [2] == "H":
                                    movement_setting [2] = ""
                                else:
                                    movement_setting [2] = "S"
                            if button == "NL":
                                movement_setting [3] = movement_setting [3] - 1 if movement_setting [3] > 1 else movement_setting [3]
                            if button == "NR":
                                movement_setting [3] = movement_setting [3] + 1 if movement_setting [3] < 7 else movement_setting [3]
                            break
                
        pygame.display.flip()
        game_clock.tick(60)
        
        
    
    
GAME_STATE_PLAYING = 1
GAME_STATE_FINISHED = 2
GAME_STATE_MUSKETEER_SETUP = 3

USER_STATE_NONE = 1
USER_STATE_SELECTED = 2

def play_game ():
    boardrenderer = BoardRendererGame(pygame)
    boardrenderer.clear()
    
    custom_pieces = [{"name":"", "letter":utils.number_to_upper_char(selected_pieces [0][1]), "betza":build_betja(selected_pieces [0][2]), "position":[None, None], "icon":str(selected_pieces [0][0])},
                     {"name":"","letter":utils.number_to_upper_char(selected_pieces [1][1]),"betza":build_betja(selected_pieces [1][2]),"position": [None, None], "icon":str(selected_pieces [1][0])}]
    #custom_pieces = [{"name":"", "letter":"D", "betza":"ND", "icon":"6", "position":[2, 3]},
    #                 {"name":"","letter":"C","betza":"JA2W3", "icon":"10", "position": [4, 5]}]
    board = Musketeer.MusketeerBoard(custom_pieces)#, "cd******/nrbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/C**D**** w KQkq - 0 1")
    game = pgn.Game()
    node = game
    game.setup(board)
    
    game_state = GAME_STATE_MUSKETEER_SETUP
    user_state = USER_STATE_NONE
    selected_piece = (0,0)
    musketeer_positions = [None, None, None, None]
    
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
        boardrenderer.draw_pieces(get_pieces (), board.get_icon_mapper())
        boardrenderer.draw_buttons()
        if game_state == GAME_STATE_PLAYING:
            if user_state == USER_STATE_NONE:
                boardrenderer.highlight_piece_normal(movable_pieces)
            if user_state == USER_STATE_SELECTED:
                boardrenderer.highlight_piece_weak(movable_pieces)
                boardrenderer.highlight_piece_selected([selected_piece])
                boardrenderer.highlight_piece_normal(movable_pieces_from)
                
        if game_state == GAME_STATE_MUSKETEER_SETUP:
            if musketeer_positions [0] == None:
                boardrenderer.draw_piece(custom_pieces [0]["letter"], 8, 3, board.get_icon_mapper())
            else:
                boardrenderer.draw_piece(custom_pieces [0]["letter"], musketeer_positions [0], 0, board.get_icon_mapper())
                
            if musketeer_positions [1] == None:
                boardrenderer.draw_piece(custom_pieces [1]["letter"], 8, 4, board.get_icon_mapper())
            else:
                boardrenderer.draw_piece(custom_pieces [1]["letter"], musketeer_positions [1], 0, board.get_icon_mapper())
            
            if musketeer_positions [2] == None:
                boardrenderer.draw_piece(custom_pieces [0]["letter"].lower(), 1, 5, board.get_icon_mapper())
            else:
                boardrenderer.draw_piece(custom_pieces [0]["letter"].lower(), musketeer_positions [2], 9, board.get_icon_mapper())
            
            if musketeer_positions [3] == None:
                boardrenderer.draw_piece(custom_pieces [1]["letter"].lower(), 1, 6, board.get_icon_mapper())
            else:
                boardrenderer.draw_piece(custom_pieces [1]["letter"].lower(), musketeer_positions [3], 9, board.get_icon_mapper())
            
            if musketeer_positions [0] == None:
                boardrenderer.highlight_piece_normal([(x, 0) for x in range(1, 9)])
                boardrenderer.highlight_piece_selected([(8, 3)])
            elif musketeer_positions [2] == None:
                boardrenderer.highlight_piece_normal([(x, 9) for x in range(1, 9)])
                boardrenderer.highlight_piece_selected([(1, 5)])
            elif musketeer_positions [1] == None:
                boardrenderer.highlight_piece_normal([(x, 0) for x in range(1, 9) if x != musketeer_positions [0]])
                boardrenderer.highlight_piece_selected([(8, 4)])
            elif musketeer_positions [3] == None:
                boardrenderer.highlight_piece_normal([(x, 9) for x in range(1, 9) if x != musketeer_positions [2]])
                boardrenderer.highlight_piece_selected([(1, 6)])
            else:
                board.set_muskeeter_chess_init_position([[musketeer_positions [2], musketeer_positions [0]],[musketeer_positions [3], musketeer_positions [1]]])
                game_state = GAME_STATE_PLAYING
        # Event Handling
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GAME_STATE_PLAYING:
                    if boardrenderer.is_on_save(pygame.mouse.get_pos()):
                        pgn_path = save_file_dialog()
                        if pgn_path != None and pgn_path != "":                        
                            with open(pgn_path, 'w') as file:
                                pgn.save_game(file, game, game.accept(pgn.StringExporter(headers=False)))
                            print ("============================================= ", board)
                    if boardrenderer.is_on_load(pygame.mouse.get_pos()):
                        pgn_path = load_file_dialog()
                        if pgn_path != None and pgn_path != "":
                            with open(pgn_path) as file:
                                ogame = pgn.read_game(file)
                                board = ogame.board()
                                game = ogame
                                moveArray = ogame.mainline_moves()
                                for move in moveArray:
                                    board.push(move)
                                    game = game.add_variation(Chess.Move.from_uci(board, move.uci()))
                        print("Load")
                    if boardrenderer.is_on_undo(pygame.mouse.get_pos()):
                        print("Undo")
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
                            move = f'{utils.number_to_char(selected_piece [0])}{selected_piece [1]}{utils.number_to_char(pos [0])}{pos [1]}'
                            node = node.add_variation(Chess.Move.from_uci(board, move))
                            board.push_uci(move)
                            user_state = USER_STATE_NONE

                if game_state == GAME_STATE_MUSKETEER_SETUP:
                    pos = boardrenderer.get_board_position(pygame.mouse.get_pos())
                    if pos == None:
                        continue
                    if musketeer_positions [0] == None and pos [1] == 0:
                        musketeer_positions [0] = pos [0]
                    
                    elif musketeer_positions [2] == None and pos [1] == 9:
                        musketeer_positions [2] = pos [0]
                        
                    elif musketeer_positions [1] == None and pos [1] == 0 and pos [0] != musketeer_positions [0]:
                        musketeer_positions [1] = pos [0]
                    
                    elif musketeer_positions [3] == None and pos [1] == 9 and pos [0] != musketeer_positions [2]:
                        musketeer_positions [3] = pos [0]
        
        pygame.display.flip()
        game_clock.tick(60)
    

if __name__ == "__main__":
    select_piece()
    if (setting_state == SETTING_STATE_OK):
        play_game()