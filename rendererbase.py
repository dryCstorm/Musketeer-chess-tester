import pygame
import res
import math

COLOR_WHITE = (255,255,255)
COLOR_BORDER = (57,41,27)
COLOR_ODD = (203, 139, 98)
COLOR_EVEN = (242, 219, 183)

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
        
    def clear (self):
        self.screen.fill (COLOR_WHITE)