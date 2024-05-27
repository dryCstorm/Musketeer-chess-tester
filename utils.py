def char_to_number(char):
    if char.isalpha() and len(char) == 1:
        return ord(char.lower()) - ord('a') + 1
    else:
        return None
    
def number_to_char(number):
    if number == None:
        return None
    return chr(number + ord('a') - 1)

def number_to_upper_char(number):
    if number == None:
        return None
    return chr(number + ord('A') - 1)

def analyze_betza_notation(notation):
    # Define movement characteristics
    directions = {
        'F': 'forward',
        'B': 'backward',
        'L': 'left',
        'R': 'right',
        'W': 'one square diagonally',
        'N': 'knight',
        'D': 'queen',
        'A': 'king'
    }
    
    # Define modifiers
    modifiers = {
        'm': 'move only',
        'c': 'capture only',
        'j': 'jump'
    }
    
    # Initialize the piece's movement capabilities
    piece_movements = {
        'directions': [],
        'modifiers': []
    }
    
    # Parse the notation
    for char in notation:
        if char in directions:
            piece_movements['directions'].append(directions[char])
        elif char in modifiers:
            piece_movements['modifiers'].append(modifiers[char])
    
    return piece_movements

# Example usage
notation = 'FRLB'
movement_capabilities = analyze_betza_notation(notation)
# print(movement_capabilities)