from collections import defaultdict

class ModifierBase:
    __str__ = lambda self: '..'
    def score_letter(self, let_score):
        return let_score
    def score_word(self, word_score):
        return word_score

class DoubleWord(ModifierBase):
    __str__ = lambda self: 'DW'
    def score_word(self, word_score):
        return 2 * word_score
class TripleWord(ModifierBase):
    __str__ = lambda self: 'TW'
    def score_word(self, word_score):
        return 3 * word_score
class DoubleLetter(ModifierBase):
    __str__ = lambda self: 'DL'
    def score_letter(self, let_score):
        return 2 * let_score
class TripleLetter(ModifierBase):
    __str__ = lambda self: 'TL'
    def score_letter(self, let_score):
        return 3 * let_score


# define the moodifiers on the upper left portion of the board and rotate
# the symmetrically across the rest
upper_left_modifiers = {
    (0, 3) : TripleWord,
    (0, 6) : TripleLetter,
    (1, 2) : DoubleLetter,
    (1, 5) : DoubleWord,
    (2, 1) : DoubleLetter,
    (2, 4) : DoubleLetter,
    (3, 0) : TripleWord,
    (3, 3) : TripleLetter,
    (3, 7) : DoubleWord,
    (4, 2) : DoubleLetter,
    (4, 6) : DoubleLetter,
    (5, 1) : DoubleWord,
    (5, 5) : TripleLetter,
    (6, 0) : TripleLetter,
    (6, 4) : DoubleLetter,
    (7, 3) : DoubleWord,
}

# rotate the upper left to the right side
upper_modifiers = dict(upper_left_modifiers)
for pos in upper_left_modifiers:
    modifier = upper_left_modifiers[pos]
    upper_modifiers[14 - pos[0], pos[1]] = modifier

del upper_left_modifiers

# rotate the upper portion onto the bottom
modifiers = defaultdict(lambda: ModifierBase)
modifiers.update(upper_modifiers)
for pos in upper_modifiers:
    modifier = upper_modifiers[pos]
    modifiers[pos[0], 14 - pos[1]] = modifier

del upper_modifiers

def __debug_print():
    for i in xrange(0, 15):
        for j in xrange(0, 15):
            print modifiers[(i, j)](),
        else:
            print
