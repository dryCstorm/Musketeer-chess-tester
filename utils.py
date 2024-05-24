def char_to_number(char):
    if char.isalpha() and len(char) == 1:
        return ord(char.lower()) - ord('a') + 1
    else:
        return None
    
def number_to_char(number):
    return chr(number + ord('a') - 1)