from rendererbase import *

PIECE_SIZE = 60
BOARD_WIDTH = 500
BOARD_HEIGHT = 500
BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 90
BOARD_MAIN_WIDTH = PIECE_SIZE * 7
BOARD_MAIN_HEIGHT = PIECE_SIZE * 7
BOARD_MAIN_OFFSET_X = BOARD_OFFSET_X + (BOARD_WIDTH - BOARD_MAIN_WIDTH) / 2
BOARD_MAIN_OFFSET_Y = BOARD_OFFSET_Y + (BOARD_HEIGHT - BOARD_MAIN_HEIGHT) / 2


BACK_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE
BACK_BUTTON_Y = PIECE_SIZE * 3

FORWARD_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE * 4
FORWARD_BUTTON_Y = PIECE_SIZE * 3

LETTER_BACK_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE
LETTER_BACK_BUTTON_Y = PIECE_SIZE * 4

LETTER_FORWARD_BUTTON_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE * 4
LETTER_FORWARD_BUTTON_Y = PIECE_SIZE * 4

HEAD_X = BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE
HEAD_Y = PIECE_SIZE
HEAD_GAP = PIECE_SIZE * 2

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
        
# ====================================================================================
        
    def draw_board (self):
        self.draw_board_background()
        self.draw_board_rects()
        self.draw_board_line()
            
    def draw_head (self, number, icon_number, selected):
        if icon_number:
            self.draw_img(res.get_piece_image(icon_number), 
                                (HEAD_X + number * HEAD_GAP, HEAD_Y), (PIECE_SIZE, PIECE_SIZE))
            
        if (selected):
            self.draw_img(res.get_border(), 
                                    (HEAD_X + number * HEAD_GAP, HEAD_Y), (PIECE_SIZE, PIECE_SIZE))
        else:
            self.draw_img(res.get_border_light(), 
                                    (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + PIECE_SIZE + number * PIECE_SIZE * 2, PIECE_SIZE), (PIECE_SIZE, PIECE_SIZE))
            
    def draw_icon_selector(self, icon_number):
        if icon_number and icon_number != "None":
            self.draw_img(res.get_piece_image(icon_number), 
                                    ((BACK_BUTTON_X + FORWARD_BUTTON_X) / 2, BACK_BUTTON_Y), (PIECE_SIZE, PIECE_SIZE))
        self.draw_img(res.get_back(), 
                                    (BACK_BUTTON_X, BACK_BUTTON_Y), (PIECE_SIZE, PIECE_SIZE))
        self.draw_img(res.get_forward(), 
                                    (FORWARD_BUTTON_X, FORWARD_BUTTON_Y), (PIECE_SIZE, PIECE_SIZE))
        
    def draw_letter_selector(self, letter, available):
        if letter and letter != "None":           
            if available:
                self.draw_letter(letter, PIECE_SIZE, (0,0,255),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + PIECE_SIZE / 2, LETTER_BACK_BUTTON_Y + PIECE_SIZE / 2))
            else:
                self.draw_letter(letter, PIECE_SIZE, (255,0,0),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + PIECE_SIZE / 2, LETTER_BACK_BUTTON_Y + PIECE_SIZE / 2))
                self.draw_letter("Choose another letter", 12, (255,0,0),
                                        ((LETTER_BACK_BUTTON_X + LETTER_FORWARD_BUTTON_X) / 2 + PIECE_SIZE / 2, LETTER_BACK_BUTTON_Y + PIECE_SIZE - 6))
        self.draw_img(res.get_back(), 
                                    (LETTER_BACK_BUTTON_X, LETTER_BACK_BUTTON_Y), (PIECE_SIZE, PIECE_SIZE))
        self.draw_img(res.get_forward(), 
                                    (LETTER_FORWARD_BUTTON_X, LETTER_FORWARD_BUTTON_Y), (PIECE_SIZE, PIECE_SIZE))
        
    def draw_piece_center (self, icon_number):
        if icon_number and icon_number != "None":
            self.draw_piece(icon_number, 
                                4, 4)

# ====================================================================================

    def is_back(self, pos):
        return pos [0] >= BACK_BUTTON_X and pos [1] >= BACK_BUTTON_Y and pos [0] - BACK_BUTTON_X <= PIECE_SIZE and pos [1] - BACK_BUTTON_Y <= PIECE_SIZE
    
    def is_forward(self, pos):
        return pos [0] >= FORWARD_BUTTON_X and pos [1] >= FORWARD_BUTTON_Y and pos [0] - FORWARD_BUTTON_X <= PIECE_SIZE and pos [1] - FORWARD_BUTTON_Y <= PIECE_SIZE
    
    def is_head(self, pos, max_count):
        if pos [1] < HEAD_Y or pos [1] > HEAD_Y + PIECE_SIZE:
            return None

        for i in range(0, max_count):
            if pos [0] >= HEAD_X + HEAD_GAP * i and pos [0] <= HEAD_X + HEAD_GAP * i + PIECE_SIZE:
                return i
            
        return None
    
    def is_letter_back(self, pos):
        return pos [0] >= LETTER_BACK_BUTTON_X and pos [1] >= LETTER_BACK_BUTTON_Y and pos [0] - LETTER_BACK_BUTTON_X <= PIECE_SIZE and pos [1] - LETTER_BACK_BUTTON_Y <= PIECE_SIZE
    
    def is_letter_forward(self, pos):
        return pos [0] >= LETTER_FORWARD_BUTTON_X and pos [1] >= LETTER_FORWARD_BUTTON_Y and pos [0] - LETTER_FORWARD_BUTTON_X <= PIECE_SIZE and pos [1] - LETTER_FORWARD_BUTTON_Y <= PIECE_SIZE