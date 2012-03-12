'''
Classes and methods for performing pattern matching against a wordlist.
'''

###############################################################################
# Pattern matching methods and helpers

import lists
import string

def without_one(lst, which):
    return lst[0:which]+lst[which+1:len(lst)]

def find_in_list(lst, what):
    for i in xrange(0, len(lst)):
        if lst[i] == what:
            return i
    raise ValueError('failed to find object in list')

def remove_from_list(lst, what):
    return without_one(lst, find_in_list(lst, what))

def _find_matches_rec(wordlist, gutter, pattern, progress, ret):
    'Recursively fill out the given pattern'
    if pattern == '':
        if progress in wordlist:
            ret.add(progress)
        return
    if pattern[0] != '_':
        _find_matches_rec(
                wordlist,
                gutter,
                pattern[1:],
                progress + pattern[0],
                ret)
    else:
        for let in gutter:
            _find_matches_rec(
                    wordlist,
                    remove_from_list(gutter, let),
                    pattern[1:],
                    progress + let,
                    ret)

###############################################################################
# The pattern class itself

class Pattern(str):
    '''
    Represents a pattern consisting of alphanumeric letters and underscores.
    Provides capabilities for pattern matching against a wordlist.
    '''
    alphabet = string.lowercase + '_'

    def __init__(self, s):
        s = s.lower()
        str.__init__(self, s)
        if any([i not in self.alphabet for i in s]):
            raise ValueError('Invalid pattern string.')
    def find_matches(self, wordlist, gutter):
        ret = set()
        _find_matches_rec(wordlist, gutter, self, '', ret)
        return ret

###############################################################################
# driver for sanity checking and demonstration

if __name__=='__main__':
    import os
    import sys
    sys.path.append(os.getcwd())
    
    try:
        from libs.termcolor import termcolor
    except ImportError:
        print 'Failed to import libs. Are you calling the driver from the ',
        print 'project root? (cwd is %s)' % os.getcwd()
        exit(1)

    import lists
    wordlist = lists.get_wordlist()

    print 'Input a pattern and a gutter to see the words that match it.'
    print '  usage: [pattern],[gutter]'

    while True:
        try:
            try:
                pattern, gutter = [i.strip() for i in
                                   raw_input(' > ').split(',')]
            except ValueError:
                print '  usage: [pattern],[gutter]'
                continue
        except (EOFError, KeyboardInterrupt):
            print
            break

        p = Pattern(pattern)
        words = p.find_matches(wordlist, gutter)
        if len(words) == 0:
            print 'No matches found'
        for word in words:
            print word

