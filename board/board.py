'''
Contains classes for representing and maintaining the state of the board.
'''

###############################################################################

class BoardTile:
    'Represents a letter and a position.'
    def __init__(self, pos, letter):
        self.pos = pos
        assert len(letter) == 1, 'Length of letter string should be one'
        self.letter = letter

###############################################################################

def diff_pos(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1]) 

def is_direction(d):
    return d in set( [(0, 1), (1, 0), (-1, 0), (0, -1)] )

def sliding_window(lst, width):
    'Produce an iterator for a sliding window through an array'
    for i in xrange(0, len(lst) - width + 1):
        yield tuple([lst[j] for j in range(i, i + width)])

class Word(list):
    '''
    A list-like object that supports initialization by passing an array-like
    object.
    '''
    def __init__(self, lst=[]):
        super(list, self).__init__(self, lst)
        if not self.__validate():
            raise ValueError('invalid word')
    def __validate_direction(self, lst):
        '''
        Returns true if the tiles all go in the same direction and in
        increments of one.
        '''
        direction = None
        for c, n in sliding_window(lst, 2):
            print c, n
            diff = diff_pos(c.pos, n.pos)
            if direction is None:
                if not is_direction(diff):
                    return False
                direction = diff
            else:
                if diff != direction:
                    return False
        return True
    def __validate(self):
        if not self.__validate_direction(lst):
            return False
        return True

###############################################################################

def none():
    'Returns None as a default value for defaultdict'
    pass

from collections import defaultdict

class ScrabbleBoard:
    'Represents a board populated with words.'
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.board = defaultdict(none)
        self.words = defaultdict(list)
    def get_words(self, word):
        '''
        Returns a list of word objects corresponding to the given word.
        note that the list may be empty.
        '''
        return self.words[word]
    def get_tile(self, tile):
        '''
        Returns the tile object for this position, or None is no word was
        played there.
        '''
        return self.board[tile]
    def play_word(self, tile_list):
        pass

