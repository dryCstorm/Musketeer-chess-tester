from rendererbase import *
import utils

PIECE_SIZE = 60
BUTTON_SIZE = 40
BOARD_WIDTH = 500
BOARD_HEIGHT = 500
BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 90
BOARD_MAIN_WIDTH = PIECE_SIZE * 7
BOARD_MAIN_HEIGHT = PIECE_SIZE * 7
BOARD_MAIN_OFFSET_X = BOARD_OFFSET_X + (BOARD_WIDTH - BOARD_MAIN_WIDTH) / 2
BOARD_MAIN_OFFSET_Y = BOARD_OFFSET_Y + (BOARD_HEIGHT - BOARD_MAIN_HEIGHT) / 2


BACK_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE
BACK_BUTTON_Y = BUTTON_SIZE * 2

FORWARD_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE * 4
FORWARD_BUTTON_Y = BUTTON_SIZE * 2

LETTER_BACK_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE
LETTER_BACK_BUTTON_Y = BUTTON_SIZE * 3

LETTER_FORWARD_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE * 4
LETTER_FORWARD_BUTTON_Y = BUTTON_SIZE * 3

HEAD_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE
HEAD_Y = BUTTON_SIZE
HEAD_GAP = BUTTON_SIZE * 2

SETTING_OFFSET_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE * 1.5
SETTING_OFFSET_Y = BUTTON_SIZE * 4.5
SETTING_GAP_Y = BUTTON_SIZE * 1.8
SETTING_GAP_X = BUTTON_SIZE * 2

class BoardRendererSetting(BoardRenderer):
# ====================================================================================

    def draw_board_background (self):
        self.draw_img(res.get_board_image(), (BOARD_OFFSET_X, BOARD_OFFSET_Y), (BOARD_WIDTH, BOARD_HEIGHT))
    
    def draw_board_line (self):
        self.draw_line((BOARD_MAIN_OFFSET_X, BOARD_MAIN_OFFSET_Y - 1), 
                       (BOARD_MAIN_OFFSET_X, BOARD_MAIN_OFFSET_Y + BOARD_MAIN_HEIGHT + 2))
        
        self.draw_line((BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH, BOARD_MAIN_OFFSET_Y - 1), 
                       (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH, BOARD_MAIN_OFFSET_Y + BOARD_MAIN_HEIGHT + 2))
        
        self.draw_line((BOARD_MAIN_OFFSET_X - 1, BOARD_MAIN_OFFSET_Y), 
                       (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + 2, BOARD_MAIN_OFFSET_Y))
        
        self.draw_line((BOARD_MAIN_OFFSET_X - 1, BOARD_MAIN_OFFSET_Y + BOARD_MAIN_HEIGHT),
                       (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + 2, BOARD_MAIN_OFFSET_Y + BOARD_MAIN_HEIGHT))
    
    def draw_board_rects (self):
        for y in range(1, 8):
            for x in range(1, 8):
                self.draw_rect((BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1), BOARD_MAIN_OFFSET_Y + PIECE_SIZE * (y - 1)), 
                               (PIECE_SIZE, PIECE_SIZE), COLOR_EVEN if (x + y) % 2 else COLOR_ODD)
        
    def draw_piece (self, piece_symbol, x, y):
        self.draw_img(res.get_piece_image(piece_symbol), 
                            (BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1), BOARD_MAIN_OFFSET_Y + PIECE_SIZE * (y - 1)),
                            (PIECE_SIZE, PIECE_SIZE))
        
    def draw_highlight_normal(self, x, y):
        self.draw_img(res.get_mark_available(),
                            (BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1) + 2, BOARD_MAIN_OFFSET_Y + PIECE_SIZE * y + 2),
                            (PIECE_SIZE - 4, PIECE_SIZE - 4))
        
    def draw_highlight_weak(self, x, y):
        self.draw_img(res.get_mark_weak(),
                            (BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1) + 2, BOARD_MAIN_OFFSET_Y + PIECE_SIZE * y + 2),
                            (PIECE_SIZE - 4, PIECE_SIZE - 4))
        
    def draw_highlight_selected(self, x, y):
        self.draw_img(res.get_mark_selected(),
                            (BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1) + 2, BOARD_MAIN_OFFSET_Y + PIECE_SIZE * y + 2),
                            (PIECE_SIZE - 4, PIECE_SIZE - 4))
        
    def draw_betza_selector (self, selected, x, y):
        self.draw_letter(selected, BUTTON_SIZE, (0,0,255),
            (x + BUTTON_SIZE / 2, y + BUTTON_SIZE / 2))
        self.draw_img(res.get_arrow_button("L", False),
                      (x - BUTTON_SIZE / 4, y),
                      (BUTTON_SIZE / 4, BUTTON_SIZE))
        
        self.draw_img(res.get_arrow_button("R", False),
                      (x + BUTTON_SIZE, y),
                      (BUTTON_SIZE / 4, BUTTON_SIZE))
        
    def draw_fblr (self, selected, x, y):
        self.draw_img(res.get_arrow_button("L", "L" in selected),
                      (x - BUTTON_SIZE / 4, y),
                      (BUTTON_SIZE / 4, BUTTON_SIZE))
        
        self.draw_img(res.get_arrow_button("R", "R" in selected),
                      (x + BUTTON_SIZE, y),
                      (BUTTON_SIZE / 4, BUTTON_SIZE))
        
        self.draw_img(res.get_arrow_button("U", "F" in selected),
                      (x, y - BUTTON_SIZE / 4),
                      (BUTTON_SIZE, BUTTON_SIZE / 4))
        
        self.draw_img(res.get_arrow_button("D", "B" in selected),
                      (x, y + BUTTON_SIZE),
                      (BUTTON_SIZE, BUTTON_SIZE / 4))
    
    def draw_sh (self, sh, content, x, y):
        self.draw_letter("N/A" if sh == "" else sh, int(BUTTON_SIZE * 0.8) if sh == "" else BUTTON_SIZE, (0,0,255),
            (x + BUTTON_SIZE / 2, y + BUTTON_SIZE / 2))
        self.draw_letter(content, 12, (255,0,0),
            (x + BUTTON_SIZE / 2, y + BUTTON_SIZE - 6))
        
# ====================================================================================
        
    def draw_board (self):
        self.draw_board_background()
        self.draw_board_rects()
        self.draw_board_line()
            
    def draw_head (self, number, icon_number, selected):
        if icon_number:
            self.draw_img(res.get_piece_image(icon_number), 
                                (HEAD_X + number * HEAD_GAP, HEAD_Y), (BUTTON_SIZE, BUTTON_SIZE))
            
        if (selected):
            self.draw_img(res.get_border(), 
                                    (HEAD_X + number * HEAD_GAP, HEAD_Y), (BUTTON_SIZE, BUTTON_SIZE))
        else:
            self.draw_img(res.get_border_light(), 
                                    (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + BUTTON_SIZE + number * BUTTON_SIZE * 2, HEAD_Y), (BUTTON_SIZE, BUTTON_SIZE))
            
    def draw_icon_selector(self, icon_number):
        if icon_number and icon_number != "None":
            self.draw_img(res.get_piece_image(icon_number), 
                                    ((BACK_BUTTON_X + FORWARD_BUTTON_X) / 2, BACK_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
        self.draw_img(res.get_back(), 
                                    (BACK_BUTTON_X, BACK_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
        self.draw_img(res.get_forward(), 
                                    (FORWARD_BUTTON_X, FORWARD_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
        
    def draw_letter_selector(self, letter, available):
        if letter and letter != "None":           
            if available:
                self.draw_letter(letter, BUTTON_SIZE, (0,0,255),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + BUTTON_SIZE / 2, LETTER_BACK_BUTTON_Y + BUTTON_SIZE / 2))
            else:
                self.draw_letter(letter, BUTTON_SIZE, (255,0,0),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + BUTTON_SIZE / 2, LETTER_BACK_BUTTON_Y + BUTTON_SIZE / 2))
                self.draw_letter("Choose another letter", 12, (255,0,0),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + BUTTON_SIZE / 2, LETTER_BACK_BUTTON_Y + BUTTON_SIZE - 6))
        self.draw_img(res.get_back(), 
                                    (LETTER_BACK_BUTTON_X, LETTER_BACK_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
        self.draw_img(res.get_forward(), 
                                    (LETTER_FORWARD_BUTTON_X, LETTER_FORWARD_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
        
    def draw_piece_center (self, icon_number):
        if icon_number and icon_number != "None":
            self.draw_piece(icon_number, 4, 4)
            
    def draw_movement_setting(self, offset, settings, BETZA):
        offset_y = SETTING_OFFSET_Y + SETTING_GAP_Y * offset
        offset_x = SETTING_OFFSET_X + SETTING_GAP_X
        self.draw_img(res.get_remove_button(),
                      (SETTING_OFFSET_X, offset_y), (BUTTON_SIZE, BUTTON_SIZE))
        
        self.draw_betza_selector(BETZA [settings [0]][0], offset_x, offset_y)
        offset_x += SETTING_GAP_X
        
        if (BETZA [settings [0]][1]):
            self.draw_fblr(settings [1], offset_x, offset_y)
            offset_x += SETTING_GAP_X
            
        
        if (BETZA [settings [0]][2]):
            offset_x -= SETTING_GAP_X
            self.draw_sh(settings [2], "Select S H", offset_x, offset_y)
            offset_x += SETTING_GAP_X
        
    def draw_new_movement_button(self, offset):
        offset_y = SETTING_OFFSET_Y + SETTING_GAP_Y * offset
        self.draw_img(res.get_new_button(),
                      (SETTING_OFFSET_X, offset_y), (BUTTON_SIZE, BUTTON_SIZE))
        

# ====================================================================================

    def is_back(self, pos):
        return utils.is_in_rect(pos, (BACK_BUTTON_X, BACK_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
    
    def is_forward(self, pos):
        return utils.is_in_rect(pos, (FORWARD_BUTTON_X, FORWARD_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
    
    def is_head(self, pos, max_count):
        if pos [1] < HEAD_Y or pos [1] > HEAD_Y + BUTTON_SIZE:
            return None

        for i in range(0, max_count):
            if utils.is_in_rect(pos, (HEAD_X + HEAD_GAP * i, HEAD_Y), (BUTTON_SIZE, BUTTON_SIZE)):
                return i
            
        return None
    
    def is_letter_back(self, pos):
        return utils.is_in_rect(pos, (LETTER_BACK_BUTTON_X, LETTER_BACK_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
    
    def is_letter_forward(self, pos):
        return utils.is_in_rect(pos, (LETTER_FORWARD_BUTTON_X, LETTER_FORWARD_BUTTON_Y), (BUTTON_SIZE, BUTTON_SIZE))
    
    def is_new_button(self, pos, offset):
        offset_y = SETTING_OFFSET_Y + SETTING_GAP_Y * offset
        return utils.is_in_rect(pos, (SETTING_OFFSET_X, offset_y), (BUTTON_SIZE, BUTTON_SIZE))
    
    def is_betza_selector(self, pos, x, y):
        if utils.is_in_rect(pos, (x - BUTTON_SIZE / 4, y), (BUTTON_SIZE / 4, BUTTON_SIZE)):
            return "BL"
        if utils.is_in_rect(pos, (x + BUTTON_SIZE, y), (BUTTON_SIZE / 4, BUTTON_SIZE)):
            return "BR"
        return None
    
    def is_fblr (self, pos, x, y):
        if utils.is_in_rect(pos, (x - BUTTON_SIZE / 4, y), (BUTTON_SIZE / 4, BUTTON_SIZE)):
            return "L"
        if utils.is_in_rect(pos, (x + BUTTON_SIZE, y), (BUTTON_SIZE / 4, BUTTON_SIZE)):
            return "R"
        if (utils.is_in_rect(pos, (x, y - BUTTON_SIZE / 4), (BUTTON_SIZE, BUTTON_SIZE / 4))):
            return "F"
        if (utils.is_in_rect(pos, (x, y + BUTTON_SIZE), (BUTTON_SIZE, BUTTON_SIZE / 4))):
            return "B"
        return None
    
    def is_sh(self, pos, x, y):
        if utils.is_in_rect(pos, (x, y), (BUTTON_SIZE, BUTTON_SIZE)):
            return "SH"
        return None
    def is_setting_button(self, pos, offset, settings, BETZA):
        res = None
        offset_y = SETTING_OFFSET_Y + SETTING_GAP_Y * offset
        offset_x = SETTING_OFFSET_X + SETTING_GAP_X
        
        if pos [0] >= SETTING_OFFSET_X and pos [1] >= offset_y and pos [0] <= SETTING_OFFSET_X + BUTTON_SIZE and pos [1] <= offset_y + BUTTON_SIZE:
            return "REMOVE"
        
        res = self.is_betza_selector(pos, offset_x, offset_y)
        offset_x += SETTING_GAP_X
        if res:
            return res
        
        if (BETZA [settings [0]][1]):
            res = self.is_fblr(pos, offset_x, offset_y)
            offset_x += SETTING_GAP_X
            
        if res:
            return res
        
        if (BETZA [settings [0]][2]):
            offset_x -= SETTING_GAP_X
            res = self.is_sh(pos, offset_x, offset_y)
            offset_x += SETTING_GAP_X
            
        if res:
            return res
        
        return res