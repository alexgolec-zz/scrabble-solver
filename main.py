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

import scoring

def get_best_words(b, gutter):
    ret = []
    for i in xrange(0, 15):
        for j in xrange(0, 15):
            pos = (i, j)
            if pos not in b.board:
                continue
            words = words_for_pos(b, pos, board.ACROSS, lists.get_wordlist(),
                                  gutter)
            ret.extend(words)
    return sorted(ret, key=lambda w: scoring.score_word(w))

if __name__ == '__main__':
    b = board.get_example_board()

    import random
    import string

    gutter = [random.choice(string.lowercase) for i in xrange(0, 7)]

    for w in get_best_words(b, gutter):
        print scoring.score_word(w), w
