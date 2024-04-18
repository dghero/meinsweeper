# Meinsweeper
from enum import Enum
import os

class InteractBoardCellState(Enum):
    HIDDEN = 0
    CLICKED = 1
    FLAGGED = 2

class StaticBoardCellContent(Enum):
    EMPTY = 0
    BOMB = 1

boardWidth, boardHeight = (18,12)
bombCount = 10
endGame = False

staticBoard = []
interactBoard = []


#### HEY ME! Actual debate here! Should staticBoard JUST contain bombs, or contain numbers, or just a string visualization?
#### staticBoard should probably be in numerical/enum format, not string format
#### would it just store bombs, and have a dedicated visualBoard for storing numbers? Or store bombs+numbers
##### 1: staticBoard holds bombs and numbers, visualBoard is cached and updated by local cells as determined by staticBoard and interactBoard
##### 2: staticBoard holds bombs and numbers, visualBoard is generated from scratch every time
##### 3: staticBoard holds bombs only, visualBoard is cached with stored numbers
##### 4: staticBoard holds bombs only, visualBoard is generated from scratch every time
#### For starting: 4: staticBoard holds bombs only. VisualBoard re-created each time


def main():
    #initialize both boards
    InitializeStaticBoard()
    InitializeInteractBoard()

    while(endGame == False):
        RefreshUserScreen()
        
        # Ask for user input: reveal or flag, with coordinates

        # Resolve based on square
        ## For flag: if hidden, flag
        ##
        ## Update immediate cell
        ## Update surrounding cells 

        # Check if victory obtained


##### BOARD MANIPULATION

remainingBombs = 0

def InitializeStaticBoard():
    remainingBombs = bombCount
    # staticBoard  = [[StaticBoardCellContent.EMPTY]*boardWidth]*boardHeight 
    staticBoard = [[StaticBoardCellContent.EMPTY for i in range(boardWidth)] for j in range(boardHeight)]
    
    # Randomly pick cell; if empty, fill it and decrease
    # Dummy vals for testing purposes!
    staticBoard[1][4] = StaticBoardCellContent.BOMB
    staticBoard[1][5] = StaticBoardCellContent.BOMB
    staticBoard[1][6] = StaticBoardCellContent.BOMB
    staticBoard[5][5] = StaticBoardCellContent.BOMB
    return staticBoard


def InitializeInteractBoard():
    interactBoard = [[InteractBoardCellState.HIDDEN for i in range(boardWidth)] for j in range(boardHeight)]
    return interactBoard

def PromptUserAction():
    stacyFakename = 0
    #Need input from user: action type, cell location.
    #call appropriate of Reveal or Flag functions as.... appropriate
    #

def RevealInteractBoardCell():
    wowow = 2
    ## if bomb: update stateBoard cell, update endGame
    ## if number: update stateBoard cell
    ## if empty: update stateBoard, recurse upon all VALID surrounding cells
    ### most elegant way to do this? Blind recurion 
    

def FlagInteractBoardCell():
    placeholder = 0
    # if hidden: change to flag
    ## if bomb space, decrease remaining bomb counter
    # if flagged: change to hidden
    ## if bomb space, increase remaining bomb counter
    # if revealed: print invalid message and do nothing


##### VISUAL MANAGEMENT

messageBuffer = ["Welcome to Meinsweeper!"]
visualBoard = []

def RefreshUserScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Should board come first or last? 
    PrintVisualBoard()
    #print messages

## Message Update Actions

def OverwriteAndDisplayMessage(messageText):
    messageBuffer.clear()
    messageBuffer.append(messageText)
    RefreshUserScreen()

def AppendAndDisplayMessage(messageText):
    messageBuffer.append(messageText)
    RefreshUserScreen()

def AppendMessage(messageText):
    messageBuffer.append(messageText)

def ClearMessageBuffer():
    messageBuffer.clear()

## Board Update Actions

def UpdateVisualBoard():
    interactBoard = [[' ' for i in range(boardWidth)] for j in range(boardHeight)]

    for row in range(boardHeight):
        for column in range(boardWidth):
            eeee = 1
    # build visualBoard
    # Iterate through stateBoard
    # enum:
    #    0 - Uncleared
    #    1 - Revealed 
    #    2 - Flagged
    ##  
    return []

## Board Print Actions

def PrintRevealedVisualBoard():
    #For Game Win/Lose to show entire board
    for row in range(boardHeight):
        for column in range(boardWidth):
            placingholder = 1
            #Treat Hidden as Revealed
            #What to display for incorrectly flagged tile?
            #

def PrintVisualBoard():
    global visualBoard
    #print out board visually
    # print(' ', end='')
    # for x in range(boardWidth):
    #     print('___ ', end='')
    # print()
    # for row in staticBoard:
    #     print('|', end='')
    #     for cell in row:
    #         wow = 0
    
    #   A   B   C
    #  ___________
    # |   | 1 | * |   1
    # | 1 | 2 | 1 |   2
    # | * | 1 |   |   3


def PrintStaticBoard():
    global staticBoard
    PrintBoardTopBorder()
    for row in range(boardHeight):
        print('|', end='')
        for column in range(boardWidth):
            print(f' {GetStaticBoardCellIcon(staticBoard[row][column])} |', end='')
        print()
    PrintBoardBottomBorder()
    PrintXAxisLabels()

## UI Part Helpers

def PrintBoardTopBorder():
    print(' ', end='')
    for x in range(boardWidth):
        print('___ ', end='')
    print()

def PrintBoardBottomBorder():
    print(' ', end='')
    for x in range(boardWidth):
        print('‾‾‾ ', end='')
    print()

def PrintXAxisLabels():
    print(' ', end='')
    for x in range(boardWidth):
        label = f' {x+1}  '
        if(x+1 > 9):
            label = label[:-1]
        if(x+1 > 99):
            #What are you doing at this point? How big is your screen??
            label = label[1:]
        print(label, end='')
    
def GetStaticBoardCellIcon(cell):
    return '*' if cell == StaticBoardCellContent.BOMB else ' '






#####  PROGRAM START #####

staticBoard = InitializeStaticBoard()
interactBoard = InitializeInteractBoard()
PrintStaticBoard()
