import tiles
import letters

def score_word(word):
    ret = 0
    for let in word:
        if let.pos in tiles.modifiers:
            mod = tiles.modifiers[let.pos]
            ret += mod().score_letter(letters.values[let.letter])
        else:
            ret += letters.values[let.letter]
    for let in word:
        if let.pos in tiles.modifiers:
            mod = tiles.modifiers[let.pos]
            ret = mod().score_word(ret)
    return ret
