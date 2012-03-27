import board.board as board
import lists.lists as lists
import lists.pattern as pattern

def words_for_pos(brd, pos, direction, wordlist, gutter):
    '''
    Given a board, a position, and a direction, get the words that would fit.
    '''
    ret = []
    for pat in brd.make_patterns(pos, direction, len(gutter)):
        p = pattern.Pattern(pat.get_pattern())
        matches = p.find_matches(wordlist, gutter)
        for m in matches:
            # no need to use a full blown Word object, since we can trust the
            # returned list or correctly ordered
            ret.append(board.TileList(board.BoardTile(pat[i].pos, m[i])
                                      for i in xrange(0, len(pat))))
    return ret

b = board.get_example_board()

import random
import string

gutter = [random.choice(string.lowercase) for i in xrange(0, 7)]

print '\n'.join(
        str(i) for i in words_for_pos(b, (2, 2), board.ACROSS, lists.get_wordlist(), gutter))

