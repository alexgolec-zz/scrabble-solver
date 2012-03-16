'''
Contains classes for representing and maintaining the state of the board.
'''

###############################################################################
# Singletons for the directions
#
# Note that all objects that hold these as variables 

class Position(tuple):
    def __init__(self, iterable):
        tuple.__init__(self, iterable)
    def extend(self, scalar):
        return Position( (self[0] * scalar, self[1] * scalar) )
    def __getx(self):
        return self[0]
    def __gety(self):
        return self[1]
    x = property(__getx)
    y = property(__gety)

DOWN = Position( (0, 1) )
__DOWN_OPPOSITE = Position( (0, -1) )
ACROSS = Position( (1, 0) )
__ACROSS_OPPOSITE = Position( (-1, 0) )

DOWN.orthogonal = lambda: ACROSS
ACROSS.orthogonal = lambda: DOWN
DOWN.opposite = lambda: __DOWN_OPPOSITE
ACROSS.opposite = lambda: __ACROSS_OPPOSITE

directions = (DOWN, ACROSS)

def is_direction(d):
    return d in directions

def make_direction(d):
    if d == (0, 1):
        return DOWN
    elif d == (1, 0):
        return ACROSS
    else:
        raise ValueError('passed tuple is not a direction')

###############################################################################
# Essentially a named tuple representing a location and a character

class BoardTile:
    'Represents a letter and a position.'
    def __init__(self, pos, letter):
        self.pos = Position(pos)
        assert len(letter) == 1, 'length of letter string should be one'
        self.letter = letter

###############################################################################
# Representing a word on the board

def diff_pos(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1]) 

def sliding_window(lst, width):
    'Produce an iterator for a sliding window through an array'
    for i in xrange(0, len(lst) - width + 1):
        yield tuple([lst[j] for j in range(i, i + width)])

def sort_by_field(lst, field):
    return sorted(lst, key=(lambda d: d[field]))

class Word(list):
    '''
    A list-like object that supports initialization by passing an array-like
    object.
    '''
    def __init__(self, lst=[]):
        list.__init__(self, lst)
        if len(lst) < 2:
            raise ValueError('invalid word: no single-letter words')
        self.direction = None
        if not self.__validate_direction(lst):
            raise ValueError('invalid word')
    def __validate_direction(self, lst):
        '''
        Returns true if the tiles all go in the same direction and in
        increments of one.
        '''
        for c, n in sliding_window(lst, 2):
            diff = diff_pos(n.pos, c.pos)
            if self.direction is None:
                if not is_direction(diff):
                    return False
                self.direction = make_direction(diff)
            else:
                if diff != self.direction:
                    return False
        return True

###############################################################################
# The state of the board

def none():
    'Returns None as a default ralue for defaultdict'
    pass

from collections import defaultdict

class BoardState:
    'Represents a board populated with words.'
    def __init__(self, h, w):
        self.height = h
        self.width = w
        # a map from (x, y) tuple to tile object
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
    def __put_word(self, word):
        '''
        Put a word onto the board. Note that this does no error checking or
        overwrite checking.
        '''
        for tile in word:
            self.board[tile.pos] = tile
    def __get_intersecting_word_for_pos(self, tile, direction):
        '''
        Returns the word that intersects this tile, if any.
        A note on exceptions: the exception is raised, and the offending
        object is attached at the end to facilitate distinguishing the two
        ValueError exceptions.
        '''
        if not is_direction(direction):
            raise ValueError('invalid direction'), direction
        if not tile.pos in self:
            raise ValueError('invalid position'), tile.pos
        tiles = []
        tiles.append(tile)
        # fan outwards from the starting tile
        for d in (direction, direction.opposite()):
            cur = tile.pos
            while True:
                # increment upwards. ugly, i know...
                cur = Position( (cur[0] + d.x, cur[1] + d.y) )
                if cur not in self or cur not in self.board:
                    break
                else:
                    tiles.append(self.board[cur])
        # sort the currently unsorted list of tiles
        if len(tiles) == 1:
            return None
        else:
           return sorted(tiles, key=lambda t: t.pos[0 if direction == ACROSS else 1])
    def get_intersecting_words(self, word_obj):
        words = []
        for tile in word_obj:
            tiles = self.__get_intersecting_word_for_pos(
                     tile, word_obj.direction.orthogonal())
            if tiles is not None:
                words.append(''.join([t.letter for t in tiles]))
        return words
    def __contains__(self, pos):
        return (pos[0] >= 0 and pos[0] <= self.width and
                pos[1] >= 0 and pos[1] <= self.height)

b = BoardState(15, 15)

# ac
# bd
# e

b.board[(0, 0)] = BoardTile((0, 0), 'a')
b.board[(0, 1)] = BoardTile((0, 1), 'b')
b.board[(0, 2)] = BoardTile((0, 2), 'e')
b.board[(1, 0)] = BoardTile((1, 0), 'c')
b.board[(1, 1)] = BoardTile((1, 1), 'd')

print b.get_intersecting_words(Word([BoardTile( (12, 12), 'a'), BoardTile( (12, 13), 'a')]))
