import pygame

resource_piece_url = "resources/imgs/pieces/"
resource_mark_available_url = "resources/imgs/marks/mark-available.png"
resource_mark_weak_url = "resources/imgs/marks/mark-weak.png"
resource_mark_selected_url = "resources/imgs/marks/mark-selected.png"
resource_board_url = "resources/imgs/board.jpg"
resource_border = "resources/imgs/borders/selected.png"
resource_border_light = "resources/imgs/borders/light.png"
resource_forward = "resources/imgs/borders/forward.png"
resource_back = "resources/imgs/borders/back.png"
resource_new_button = "resources/imgs/buttons/new.png"
resource_remove_button = "resources/imgs/buttons/remove.png"
resource_left_button = "resources/imgs/buttons/left.png"
resource_right_button = "resources/imgs/buttons/right.png"
resource_up_button = "resources/imgs/buttons/up.png"
resource_down_button = "resources/imgs/buttons/down.png"
resource_left_selected_button = "resources/imgs/buttons/left-selected.png"
resource_right_selected_button = "resources/imgs/buttons/right-selected.png"
resource_up_selected_button = "resources/imgs/buttons/up-selected.png"
resource_down_selected_button = "resources/imgs/buttons/down-selected.png"

images = {}

def get_image(url):
    if (images.get(url) is None):
        images.setdefault(url, pygame.image.load(url))
    return images [url]

def get_piece_image(piece_symbol, mapper = {}):
    if isinstance (piece_symbol, int):
        return get_image(resource_piece_url + "custom/" + str(piece_symbol) + ".png")
    
    piece_symbol_img = piece_symbol
    if piece_symbol.upper() in mapper:
        piece_symbol_img = "custom/" + mapper [piece_symbol.upper()]
        
    piece_url = resource_piece_url + piece_symbol_img + ".png"
    if not piece_symbol.islower():
        piece_url = resource_piece_url + piece_symbol_img + "w" + ".png"
    return get_image(piece_url)

def get_board_image():
    return get_image (resource_board_url)

def get_mark_available():
    return get_image (resource_mark_available_url)

def get_mark_weak():
    return get_image(resource_mark_weak_url)

def get_mark_selected():
    return get_image (resource_mark_selected_url)

def get_border_light():
    return get_image (resource_border_light)
    
def get_border():
    return get_image (resource_border)

def get_forward():
    return get_image(resource_forward)

def get_back():
    return get_image(resource_back)

def get_new_button():
    return get_image(resource_new_button)

def get_remove_button():
    return get_image(resource_remove_button)

def get_arrow_button(str, selected):
    if str == "U":
        return get_image(resource_up_selected_button if selected else resource_up_button)
    if str == "D":
        return get_image(resource_down_selected_button if selected else resource_down_button)
    if str == "L":
        return get_image(resource_left_selected_button if selected else resource_left_button)
    if str == "R":
        return get_image(resource_right_selected_button if selected else resource_right_button)