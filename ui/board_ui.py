#Created by Nathaniel Clinger


import pygame, sys, time
from pygame import *

class ScrabbleBoardDelegate:
    def getNextBestWord(self, sender):
        pass
    def boardWasModified(self, sender):
        pass
    def tileWasCleared(self, sender, pos):
        pass
    def letterWasInput(self, sender, letter, pos):
        pass
    def acceptWord(self, sender, word):
        pass

class ScrabbleBoard(object):
    
    grid = [[ "NA", "NA", "NA", "3W", "NA", "NA", "3L", "NA", "3L", "NA", "NA", "3W", "NA", "NA", "NA" ],
            [ "NA", "NA", "2L", "NA", "NA", "2W", "NA", "NA", "NA", "2W", "NA", "NA", "2L", "NA", "NA" ],
            [ "NA", "2L", "NA", "NA", "2L", "NA", "NA", "NA", "NA", "NA", "2L", "NA", "NA", "2L", "NA" ],
            [ "3W", "NA", "NA", "3L", "NA", "NA", "NA", "2W", "NA", "NA", "NA", "3L", "NA", "NA", "3W" ],
            [ "NA", "NA", "2L", "NA", "NA", "NA", "2L", "NA", "2L", "NA", "NA", "NA", "2L", "NA", "NA" ],
            [ "NA", "2W", "NA", "NA", "NA", "3L", "NA", "NA", "NA", "3L", "NA", "NA", "NA", "2W", "NA" ],
            [ "3L", "NA", "NA", "NA", "2L", "NA", "NA", "NA", "NA", "NA", "2L", "NA", "NA", "NA", "3L" ],
            [ "NA", "NA", "NA", "2W", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "2W", "NA", "NA", "NA" ],
            [ "3L", "NA", "NA", "NA", "2L", "NA", "NA", "NA", "NA", "NA", "2L", "NA", "NA", "NA", "3L" ],
            [ "NA", "2W", "NA", "NA", "NA", "3L", "NA", "NA", "NA", "3L", "NA", "NA", "NA", "2W", "NA" ],
            [ "NA", "NA", "2L", "NA", "NA", "NA", "2L", "NA", "2L", "NA", "NA", "NA", "2L", "NA", "NA" ],
            [ "3W", "NA", "NA", "3L", "NA", "NA", "NA", "2W", "NA", "NA", "NA", "3L", "NA", "NA", "3W" ],
            [ "NA", "2L", "NA", "NA", "2L", "NA", "NA", "NA", "NA", "NA", "2L", "NA", "NA", "2L", "NA" ],
            [ "NA", "NA", "2L", "NA", "NA", "2W", "NA", "NA", "NA", "2W", "NA", "NA", "2L", "NA", "NA" ],
            [ "NA", "NA", "NA", "3W", "NA", "NA", "3L", "NA", "3L", "NA", "NA", "3W", "NA", "NA", "NA" ],
            [ "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH", "HH" ]]

    colors = {"3W":(155, 0, 0), "2L":(131, 154, 255), "3L":(0, 0, 255), 
              "2W":(255, 192, 203), "SS":(255, 255, 255), "NA":(0, 255, 0), 
              "HH":(255, 255, 255)}
    
    def __init__(self, delegate=ScrabbleBoardDelegate()):
        pygame.init()
    
        self.width, self.height = 500, 500
        
        self.screen = pygame.display.set_mode((self.width, self.height)) #@UndefinedVariable
        pygame.display.set_caption('Scrabble Solver') #@UndefinedVariable
        
        self.board = self.__init_board__()
        self.__show_board__()
        
        self.writeTo = [False, -1, -1]
        self.delegate = delegate
        self.last_word = None
    
    def __init_board__(self):
        
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((255, 255, 255))
        
        sizeX = float(len(self.grid[0]))
        sizeY = float(len(self.grid))
        
        changeX = float(self.width) / sizeX
        changeY = float(self.height) / sizeY
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                # convert grid to list of what it is + associated letter
                self.grid[y][x] = [self.grid[y][x], None]
                
                # add colored rect 
                pygame.draw.rect(background, self.getColor(y, x), #@UndefinedVariable
                                                (x * changeX,
                                                 y * changeY,
                                                 (x + 1) * changeX,
                                                 (y + 1) * changeY), 0)
        
        self.__draw_boarder__() # draw the boarders
        
        self.grid[len(self.grid) - 1][len(self.grid[1]) - 1][1] = "GO"  # set up button
        
        self.update_board()     # make sure to update the board so that we see the changes
        
        return background
    
    
    def __draw_boarder__(self):
        size = float(len(self.grid[0]))
        
        for i in range(len(self.grid[0])):
            # Vertical lines
            pygame.draw.line(self.screen, (0, 0, 0), #@UndefinedVariable
                            (i * float(self.height) / size, 0), 
                            (i * float(self.height) / size, self.height), 2)
            
        size = float(len(self.grid))
        for i in range(len(self.grid)):
            # Horizontal lines
            pygame.draw.line(self.screen, (0, 0, 0), #@UndefinedVariable
                            (0, i * float(self.width) / size), 
                            (self.width, i * float(self.width) / size), 2)
    
    def getColor(self, i, j):
        return self.colors[self.grid[i][j][0]]
    
    def getLetter(self, i, j):
        return self.grid[i][j][1]
    
    
    def start(self):
        "start the game"
        
        self.update_board()
        
        while (True):
            for event in pygame.event.get(): #@UndefinedVariable
                if event.type is pygame.QUIT:
                    return
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    self.__click_board__()
                elif event.type == KEYDOWN:
                    inkey = event.key
                    if inkey == K_BACKSPACE:    # if backspace, set to blank
                        self.setLetter('')
                    elif inkey == K_RETURN:     # if return, stop editing that position
                        self.writeTo[0] = False
                    elif inkey in range(256):   # make sure within range
                        self.setLetter(chr(inkey))
                    self.update_board()
            
#            self.board.blit(self.background, (0, 0))
#            pygame.display.flip()
    
    
    def __show_board__(self):
        ''' Redraw the board on the screen '''
        self.update_board()
        self.screen.blit(self.board, (0, 0))
        pygame.display.flip() #@UndefinedVariable
    
    
    def __board_pos__(self, mouseX, mouseY):
        row = mouseY / (self.height / len(self.grid))
        col = mouseX / (self.width / len(self.grid[0]))
        
        return row, col
    
    def setLetter(self, letter, x=None, y=None):
        if x or y is None:  # check if x or y are none
            if self.writeTo[0]:     # if writeTo is true, set x/y
                x = self.writeTo[1]
                y = self.writeTo[2]
#                self.writeTo[0] = False
            else:
                return      # otherwise just return
        
        self.grid[x][y][1] = letter
        if letter == '':
            self.delegate.tileWasCleared(self, (y, x))
        else:
            self.delegate.letterWasInput(self, letter, (y, x))
        self.delegate.boardWasModified(self)
        self.delegate.acceptWord(self, self.last_word)

    def __click_board__(self):
        ''' Determine where clicked and draw '''
        mouseX, mouseY = pygame.mouse.get_pos() #@UndefinedVariable
        row, col = self.__board_pos__(mouseX, mouseY)
        
        if row != len(self.grid) - 1 or col != len(self.grid[1]) - 1:
            self.writeTo = [True, row, col]
        else:
            self.update_board() # update to current board state
            best_word = self.delegate.getNextBestWord(self)
            if best_word:
                for tile in best_word:
                    self.setRedLetter(tile.letter, tile.pos[0], tile.pos[1])
            self.last_word = best_word
            print best_word
    
    
    def setRedLetter(self, letter, x, y):
        '''set up a red letter for a new word being added to the grid'''
        self.grid[y][x][1] = letter
        
        sizeX = float(len(self.grid[0]))
        sizeY = float(len(self.grid))
        
        changeX = float(self.width) / sizeX
        changeY = float(self.height) / sizeY
        
        self.screen.fill(self.getColor(y, x),
                         (x * changeX,
                          y * changeY,
                          changeX,
                          changeY), 0)
        
#        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
#                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        
        font = pygame.font.Font(None, 30) #@UndefinedVariable
#        text = font.render(self.getLetter(y, x), 1, (1, 0, 0))
        self.screen.blit(font.render(self.getLetter(y, x), 1, (255, 0, 0)), 
                         (5 + x * float(self.height) / sizeX,
                          5 + y * float(self.width) / sizeY))
        
        self.__draw_boarder__() # create boarder now
        
        pygame.display.flip() #@UndefinedVariable
    
    def update_board(self):
        sizeX = float(len(self.grid[0]))
        sizeY = float(len(self.grid))
            
        changeX = float(self.width) / sizeX
        changeY = float(self.height) / sizeY
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.getLetter(y, x) is None:
                    continue
                else:
                    self.screen.fill(self.getColor(y, x),
                                                (x * changeX,
                                                 y * changeY,
                                                 changeX,
                                                 changeY), 0)
                    
                    font = pygame.font.Font(None, 30) #@UndefinedVariable
                    text = font.render(self.getLetter(y, x), 1, (0, 0, 0))
                    self.screen.blit(text, (5 + x * float(self.height) / sizeX,
                                           5 + y * float(self.width) / sizeY))
        
        self.__draw_boarder__()
        
        pygame.display.flip() #@UndefinedVariable


#def main():
#    game = ScrabbleBoard()
#    game.start()
#
#if __name__ == '__main__':
#    main()

