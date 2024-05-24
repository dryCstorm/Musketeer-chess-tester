import pygame
import res
import math

COLOR_WHITE = (255,255,255)
COLOR_BORDER = (57,41,27)
COLOR_ODD = (203, 139, 98)
COLOR_EVEN = (242, 219, 183)

PIECE_SIZE = 60
BOARD_WIDTH = 560
BOARD_HEIGHT = 680
BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 0
BOARD_MAIN_WIDTH = PIECE_SIZE * 8
BOARD_MAIN_HEIGHT = PIECE_SIZE * 10
BOARD_MAIN_OFFSET_X = BOARD_OFFSET_X + (BOARD_WIDTH - BOARD_MAIN_WIDTH) / 2
BOARD_MAIN_OFFSET_Y = BOARD_OFFSET_Y + (BOARD_HEIGHT - BOARD_MAIN_HEIGHT) / 2
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 680

class BoardRenderer():
    screen: pygame.Surface
    
    def __init__ (self, _pygame):
        self.screen = _pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
# ====================================================================================

    def draw_img (self, img, offset, size):
        self.screen.blit(pygame.transform.scale(img, size), offset)
        
    def draw_line(self, start, end, color = COLOR_BORDER):
        pygame.draw.line(self.screen, color, start, end, 4)

    def draw_alpha_rect(self, start, size, color, alpha):
        temp = pygame.Surface(size)
        temp.set_alpha(alpha)
        temp.fill(color)
        self.screen.blit(temp, start)
        
    def draw_rect(self, start, size, color = COLOR_WHITE):
        pygame.draw.rect(self.screen, color, (start, size))
        
        
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
        
        self.draw_line((BOARD_MAIN_OFFSET_X - 1, BOARD_MAIN_OFFSET_Y + PIECE_SIZE),
                       (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + 2, BOARD_MAIN_OFFSET_Y + PIECE_SIZE))
        
        self.draw_line((BOARD_MAIN_OFFSET_X - 1, BOARD_MAIN_OFFSET_Y + PIECE_SIZE * 9),
                       (BOARD_MAIN_OFFSET_X + BOARD_MAIN_WIDTH + 2, BOARD_MAIN_OFFSET_Y + PIECE_SIZE *  9))
    
    def draw_board_rects (self):
        self.draw_alpha_rect((BOARD_MAIN_OFFSET_X, BOARD_MAIN_OFFSET_Y), 
                             (BOARD_MAIN_WIDTH, PIECE_SIZE), COLOR_WHITE, 64)
        self.draw_alpha_rect((BOARD_MAIN_OFFSET_X, BOARD_MAIN_OFFSET_Y + PIECE_SIZE * 9), 
                             (BOARD_MAIN_WIDTH, PIECE_SIZE), COLOR_WHITE, 64)
        for y in range(1, 9):
            for x in range(1, 9):
                self.draw_rect((BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1), BOARD_MAIN_OFFSET_Y + PIECE_SIZE * y), 
                               (PIECE_SIZE, PIECE_SIZE), COLOR_EVEN if (x + y) % 2 else COLOR_ODD)
        
    def draw_piece (self, piece_symbol, x, y):
        self.draw_img(res.get_piece_image(piece_symbol), 
                            (BOARD_MAIN_OFFSET_X + PIECE_SIZE * (x - 1), BOARD_MAIN_OFFSET_Y + PIECE_SIZE * y),
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
        
    def clear (self):
        self.screen.fill (COLOR_WHITE)
        
    def draw_board (self):
        self.draw_board_background()
        self.draw_board_rects()
        self.draw_board_line()
        
    def draw_pieces(self, pieces):
        for piece in pieces:
            self.draw_piece(piece[0], piece[1], piece[2])
            
    def highlight_piece_normal(self, pieces):
        for piece in pieces:
            self.draw_highlight_normal(piece[0], piece[1])
            
    def highlight_piece_weak(self, pieces):
        for piece in pieces:
            self.draw_highlight_weak(piece[0], piece[1])
            
    def highlight_piece_selected(self, pieces):
        for piece in pieces:
            self.draw_highlight_selected(piece[0], piece[1])
    
# ====================================================================================

    def get_board_position(self, pos):
        x = math.floor ((pos [0] - BOARD_MAIN_OFFSET_X) / PIECE_SIZE) + 1
        y = math.floor ((pos [1] - BOARD_MAIN_OFFSET_Y) / PIECE_SIZE)
        if x < 1 or y < 0 or x >= 9 or y >= 10:
            return None
        
        return (x, y)