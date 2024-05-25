import pygame

resource_piece_url = "resources/imgs/pieces/"
resource_mark_available_url = "resources/imgs/marks/mark-available.png"
resource_mark_weak_url = "resources/imgs/marks/mark-weak.png"
resource_mark_selected_url = "resources/imgs/marks/mark-selected.png"
resource_board_url = "resources/imgs/board.jpg"

images = {}

def get_image(url):
    if (images.get(url) is None):
        images.setdefault(url, pygame.image.load(url))
    return images [url]

def get_piece_image(piece_symbol):
    piece_url = resource_piece_url + piece_symbol + ".png"
    if not piece_symbol.islower():
        piece_url = resource_piece_url + piece_symbol + "w" + ".png"
    return get_image(piece_url)

def get_board_image():
    return get_image (resource_board_url)

def get_mark_available():
    return get_image (resource_mark_available_url)

def get_mark_weak():
    return get_image(resource_mark_weak_url)

def get_mark_selected():
    return get_image (resource_mark_selected_url)