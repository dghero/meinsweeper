# Meinsweeper
# (C) Devin Hero 2024

from enum import Enum
import os
import re
from ast import literal_eval as make_tuple

class InteractBoardCellState(Enum):
    HIDDEN = 0
    CLICKED = 1
    FLAGGED = 2

class StaticBoardCellContent(Enum):
    EMPTY = 0
    BOMB = 1

class LastAction(Enum):
    UNKNOWN = 0
    CLICKED = 1
    FLAGGED = 2

bombCount = 10
remainingBombs = 0

staticBoard = []
interactBoard = []

def main():
    boardWidth = 0
    boardHeight = 0
    endGame = False
    lastAction = LastAction.UNKNOWN
    lastCoordinates = (None,None)

    print("Welcome to Meinsweeper!")
    boardWidth, boardHeight = PromptBoardDimensions()
    # print(boardWidth, boardHeight, bombCount, remainingBombs)
    InitializeStaticBoard(boardWidth, boardHeight)
    InitializeInteractBoard(boardWidth, boardHeight)

    while(endGame == False):
        UpdateVisualBoard(boardWidth, boardHeight)
        RefreshUserScreen()
        ClearMessageBuffer()
        lastAction, lastCoordinates = PromptUserAction()

        # Resolve based on square
        ## For flag: if hidden, flag
        ##
        ## Update immediate cell
        ## Update surrounding cells 

        # Check if victory obtained




##### BOARD MANIPULATION #####

## Board Initialization

def PromptBoardDimensions():
    boardWidth, boardHeight = (0,0)
    while True:
        boardWidth = input('Enter board width between 1-50): ')
        print(boardWidth, type(boardWidth), boardWidth.isdigit())
        if(boardWidth.isdigit() and int(boardWidth) > 0 and int(boardWidth) < 51):
            break
    while True:
        boardHeight = input('Enter board height between 1-50: ')
        if(boardHeight.isdigit() and int(boardHeight) > 0 and int(boardHeight) < 51):
            break
    return int(boardWidth), int(boardHeight)

def InitializeStaticBoard(boardWidth, boardHeight):
    global staticBoard
    remainingBombs = bombCount

    # staticBoard  = [[StaticBoardCellContent.EMPTY]*boardWidth]*boardHeight 
    staticBoard = [[StaticBoardCellContent.EMPTY for i in range(boardWidth)] for j in range(boardHeight)]
    
    # Randomly pick cell; if empty, fill it and decrease
    # Dummy vals for testing purposes!
    staticBoard[1][1] = StaticBoardCellContent.BOMB
    staticBoard[1][4] = StaticBoardCellContent.BOMB
    staticBoard[1][5] = StaticBoardCellContent.BOMB
    staticBoard[1][6] = StaticBoardCellContent.BOMB
    staticBoard[5][5] = StaticBoardCellContent.BOMB
    staticBoard[3][7] = StaticBoardCellContent.BOMB

    staticBoard[0][0] = StaticBoardCellContent.BOMB
    staticBoard[7][0] = StaticBoardCellContent.BOMB
    staticBoard[0][7] = StaticBoardCellContent.BOMB
    staticBoard[7][7] = StaticBoardCellContent.BOMB


def InitializeInteractBoard(boardWidth, boardHeight):
    global interactBoard
    interactBoard = [[InteractBoardCellState.HIDDEN for i in range(boardWidth)] for j in range(boardHeight)]
    # interactBoard = [[InteractBoardCellState.CLICKED for i in range(boardWidth)] for j in range(boardHeight)]
    interactBoard[0][0] = InteractBoardCellState.FLAGGED
    interactBoard[1][0] = InteractBoardCellState.FLAGGED
    interactBoard[0][1] = InteractBoardCellState.CLICKED
    interactBoard[1][1] = InteractBoardCellState.CLICKED

    interactBoard[4][7] = InteractBoardCellState.CLICKED
    interactBoard[5][7] = InteractBoardCellState.CLICKED

## Board Actions

def PromptUserAction():
    print("Select action and coordinates in X,Y format (e.g. C2,5)")
    print("[C] - Clear")
    print("[F] - Flag")
    commandReg = re.search("^[CcFf][0-5]{0,1}[0-9],[0-5]{0,1}[0-9]$", input("> "))
    if commandReg == None:
        return LastAction.UNKNOWN, (None,None)
    
    action = LastAction.CLICKED if commandReg.string[0].lower() == "c" else LastAction.FLAGGED
    coordinates = make_tuple(commandReg.string[1:])
    
    return action, coordinates

def RevealCell():
    wowow = 2
    ## if bomb: update stateBoard cell, update endGame
    ## if number: update stateBoard cell
    ## if empty: update stateBoard, recurse upon all VALID surrounding cells
    ### most elegant way to do this? Blind recurion will have a good amount of redundant checks
    

def FlagCell():
    placeholder = 0
    # if hidden: change to flag
    ## if bomb space, decrease remaining bomb counter
    # if flagged: change to hidden
    ## if bomb space, increase remaining bomb counter
    # if revealed: print invalid message and do nothing


##### VISUAL MANAGEMENT #####

## General Visual Actions

def RefreshUserScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Should board come first or last? 
    PrintVisualBoard()
    PrintMessages()

## Message Actions
messageBuffer = ["Welcome to Meinsweeper!"]

def PrintMessages():
    for msg in messageBuffer:
        print(msg)

def AppendMessage(messageText):
    messageBuffer.append(messageText)

def ClearMessageBuffer():
    messageBuffer.clear()

## Visual Board Actions

visualBoard = []

def UpdateVisualBoard(boardHeight, boardWidth, isGameEnd=False):
    global visualBoard
    newBoard = []
    newBoard.append(GenerateBoardTopBorder(boardWidth))
    for row in reversed(range(boardHeight)):
        nextLine = '|'
        for column in range(boardWidth):
            icon = GetVisualBoardCellIcon(row, column, isGameEnd)
            nextLine += f' {icon} |'
        nextLine += f'  {row+1}'
        newBoard.append(nextLine)
    newBoard.append(GenerateBoardBottomBorder(boardWidth))
    newBoard.append(GenerateXAxisLabels(boardWidth))
    visualBoard = newBoard

def PrintVisualBoard():
    global visualBoard
    for line in visualBoard:
        print(line)

    # PrintBoardTopBorder()
    # for row in range(boardHeight):
    #     print('|', end='')
    #     for column in range(boardWidth):
    #         icon = GetVisualBoardCellIcon(row, column, isGameEnd)
    #         # icon = '_' if icon == ' ' else icon
    #         print(f' {icon} |', end='')
    #     print()
    # PrintBoardBottomBorder()
    # PrintXAxisLabels()

    
    #   1   2   3
    #  ___________
    # |   | 1 | * |   1
    # | 1 | 2 | 1 |   2
    # | * | 1 |   |   3

## UI Part Helpers

def GenerateBoardTopBorder(boardWidth):
    topBorder = ' '
    for x in range(boardWidth):
        topBorder += '___ '
    return topBorder

def GenerateBoardBottomBorder(boardWidth):
    bottomBorder = ' '
    for x in range(boardWidth):
        bottomBorder += '--- '
    bottomBorder += '  Y'
    return bottomBorder

def GenerateXAxisLabels(boardWidth):
    xLabels = ' '
    for x in range(boardWidth):
        label = f' {x+1}  '
        if(x+1 > 9):
            label = label[:-1]
        if(x+1 > 99):
            #What are you doing at this point? How big is your screen??
            label = label[1:]
        xLabels += label

    xLabels += "X"
    return xLabels

def GetVisualBoardCellIcon(yRow, xColumn, isGameEnd=False):
    global interactBoard
    global visualBoard
    localBombCount = 0
    boardWidth = len(interactBoard[0])
    boardHeight = len(interactBoard)

    if(interactBoard[yRow][xColumn] == InteractBoardCellState.HIDDEN):
        return ' '

    if(interactBoard[yRow][xColumn] == InteractBoardCellState.FLAGGED):
        if(isGameEnd and staticBoard[yRow][xColumn] == StaticBoardCellContent.EMPTY):
            return '#'
        else:
            return 'F'

    if(staticBoard[yRow][xColumn] == StaticBoardCellContent.BOMB):
        return '*' if interactBoard[yRow][xColumn] != InteractBoardCellState.CLICKED else 'X'

    # Anything else clicked by now is a number
    for y in range(yRow-1, yRow+2):
        for x in range(xColumn-1, xColumn+2):
            validCoordinates = [
                x >= 0,
                y >= 0,
                x < boardWidth,
                y < boardHeight]
            
            if (all(validCoordinates) and staticBoard[y][x] == StaticBoardCellContent.BOMB):
                localBombCount += 1
    return str(localBombCount)


#### OLD STATICBOARD DEBUG
# Doesn't show numbers or any interaction states, just bombs; primarily useful for debugging
# def PrintStaticBoard():
#     global staticBoard
#     PrintBoardTopBorder()
#     for row in range(boardHeight):
#         print('|', end='')
#         for column in range(boardWidth):
#             icon = GetStaticBoardCellIcon(staticBoard[row][column])
#             icon = '_' if icon == ' ' else icon
#             print(f'_{icon}_|', end='')
#         print()
#     PrintBoardBottomBorder()
#     PrintXAxisLabels()

# def GetStaticBoardCellIcon(cell):
#     return '*' if cell == StaticBoardCellContent.BOMB else ' '

# def PrintBoardTopBorder():
#     print(GenerateBoardTopBorder())
#     # print(' ', end='')
#     # for x in range(boardWidth):
#     #     print('___ ', end='')
#     # print()

# def PrintBoardBottomBorder():
#     print(GenerateBoardBottomBorder())
#     # print(' ', end='')
#     # for x in range(boardWidth):
#     #     print('--- ', end='')
#     # print()

# def PrintXAxisLabels():
#     print(GenerateXAxisLabels())
#     # print(' ', end='')
#     # for x in range(boardWidth):
#     #     label = f' {x+1}  '
#     #     if(x+1 > 9):
#     #         label = label[:-1]
#     #     if(x+1 > 99):
#     #         #What are you doing at this point? How big is your screen??
#     #         label = label[1:]
#     #     print(label, end='')
#     # print()
    


#####  PROGRAM START #####

main()

