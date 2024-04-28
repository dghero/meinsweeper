# Meinsweeper
# (C) Devin Hero 2024

from enum import Enum
import math
import os
import re
import random
#from ast import literal_eval


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

class TextStyle():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\33[90m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

staticBoard = []
interactBoard = []

def main():
    boardWidth = 0
    boardHeight = 0
    mines = 0
    exploded = False
    flagScore = 0 #increases with correct flags, decreases with incorrect flags
    endGame = False
    lastAction = LastAction.UNKNOWN
    lastCoordinates = (None,None)

    print("Welcome to Meinsweeper!")
    boardWidth, boardHeight, mines = PromptGameDifficulty()
    # print(boardWidth, boardHeight, bombCount, remainingBombs)
    InitializeStaticBoard(boardWidth, boardHeight, mines)
    InitializeInteractBoard(boardWidth, boardHeight)

    UpdateVisualBoard()
    RefreshUserScreen()

    while(endGame == False):
        lastAction, lastCoordinates = PromptUserAction()
        if(lastAction == LastAction.UNKNOWN):
            AppendMessage("Error: Invalid action, try again")
        elif(lastAction == LastAction.FLAGGED):
            AppendMessage(f'Last Action: Flagged cell at ({lastCoordinates[0]+1}, {lastCoordinates[1]+1})')
            flagScore += FlagCell(*lastCoordinates)
        elif(lastAction == LastAction.CLICKED):
            AppendMessage(f'Last Action: Revealed cell at ({lastCoordinates[0]+1}, {lastCoordinates[1]+1})')
            exploded = RevealCell(*lastCoordinates)

        endGame = IsGameEnd(exploded, mines, flagScore)
        AppendMessage(f'DEBUG -- {mines} mines, {flagScore} score')
        UpdateVisualBoard(endGame)
        RefreshUserScreen()
        ClearMessageBuffer()
    



##### BOARD MANIPULATION #####

## Board Initialization

def PromptGameDifficulty():
    print(
"""Please enter difficulty:
  1 - Beginner:       9 x  9, 10 mines
  2 - Intermediate:  16 x 16, 40 mines
  3 - Expert:        30 x 16, 99 mines
  4 - Custom:        Choose your own""")
    mode = ""
    while(not mode.isdigit() or int(mode) != 1 and int(mode) != 2 and int(mode) != 3 and int(mode) != 4):
        mode = input("> ")
    mode = int(mode)
    # Returns in order: width, height, bombs
    if(mode == 1):
        return 9, 9, 10
    elif(mode == 2):
        return 16, 16, 40
    elif(mode == 3):
        return 30, 16, 99
    elif(mode == 4):
        return PromptBoardParameters()

    
def PromptBoardParameters():
    boardWidth, boardHeight, mines = (0,0,0)

    boardWidth = GetUserBoardDimension('width')
    boardHeight = GetUserBoardDimension('height')
    mines = GetUserMineCount(boardHeight * boardWidth)
        
    return boardWidth, boardHeight, mines

def InitializeStaticBoard(boardWidth, boardHeight, mines):
    global staticBoard
    remainingBombs = mines

    staticBoard = [[StaticBoardCellContent.EMPTY for i in range(boardWidth)] for j in range(boardHeight)]
    random.seed()
    while(remainingBombs > 0):
        x = random.randint(0, boardWidth-1)
        y = random.randint(0, boardHeight-1)
        if(staticBoard[y][x] == StaticBoardCellContent.EMPTY):
            staticBoard[y][x] = StaticBoardCellContent.BOMB
            remainingBombs -= 1

    # Randomly pick cell; if empty, fill it and decrease
    # Dummy vals for testing purposes!
    # staticBoard[1][1] = StaticBoardCellContent.BOMB
    # staticBoard[1][4] = StaticBoardCellContent.BOMB
    # staticBoard[1][5] = StaticBoardCellContent.BOMB
    # staticBoard[1][6] = StaticBoardCellContent.BOMB
    # staticBoard[5][5] = StaticBoardCellContent.BOMB
    # staticBoard[3][7] = StaticBoardCellContent.BOMB

    # staticBoard[0][0] = StaticBoardCellContent.BOMB
    # staticBoard[7][0] = StaticBoardCellContent.BOMB
    # staticBoard[0][7] = StaticBoardCellContent.BOMB
    # staticBoard[7][7] = StaticBoardCellContent.BOMB

    # staticBoard[boardHeight-1][boardWidth-1] = StaticBoardCellContent.BOMB


def InitializeInteractBoard(boardWidth, boardHeight):
    global interactBoard
    interactBoard = [[InteractBoardCellState.HIDDEN for i in range(boardWidth)] for j in range(boardHeight)]

## Board Initialization Helpers

def GetUserBoardDimension(dimension):
    while(True):
        boardDimension = input(f'Enter board {dimension} between 1-50 (leave empty for default 10): ')
        if(boardDimension.isdigit() and int(boardDimension) > 0 and int(boardDimension) < 51):
            return int(boardDimension)
        if(boardDimension == ""):
            return 10
        
def GetUserMineCount(totalCells):
    defaultMineCnt = int(math.ceil(totalCells * .17))
    
    while(True):
        mines = input(f'Enter mine count between 1-{totalCells-1} (leave empty for default {defaultMineCnt}): ')
        if(mines.isdigit() and int(mines) > 0 and int(mines) < totalCells):
            return int(mines)
        if(mines == ""):
            return defaultMineCnt


## Board Actions

def PromptUserAction():
    print("Select action and coordinates in X,Y format (e.g. C2,5)")
    print("[C] - Clear")
    print("[F] - Flag/Unflag")
    commandReg = re.search("^[CcFf][0-5]{0,1}[0-9],[0-5]{0,1}[0-9]$", input("> "))
    if commandReg == None:
        return LastAction.UNKNOWN, (None,None)
    
    action = LastAction.CLICKED if commandReg.string[0].lower() == "c" else LastAction.FLAGGED
    coordinates = commandReg.string[1:].split(",")
    # Need to account for -1 offset between user coordinates vs. list indexing
    x, y = int(coordinates[0])-1, int(coordinates[1])-1
    
    if(IsValidCoordinates(x, y)):
        return action, (x,y)
    else:
        AppendMessage(f'Coordinates ({x+1}, {y+1}) are out of range!')
        return LastAction.UNKNOWN, (None,None)
    
def RevealCell(xColumn, yRow):
    global interactBoard
    global staticBoard
    
    if(interactBoard[yRow][xColumn] == InteractBoardCellState.CLICKED):
        AppendMessage('Attempted to reveal cleared cell; no action taken')

    elif(interactBoard[yRow][xColumn] == InteractBoardCellState.FLAGGED):
        AppendMessage('Attempted to reveal flagged cell; no action taken')

    elif(staticBoard[yRow][xColumn] == StaticBoardCellContent.BOMB):
        interactBoard[yRow][xColumn] = InteractBoardCellState.CLICKED
        AppendMessage('BOOM! Mine was triggered and exploded')
        return True
    
    elif(GetCellAdjacentBombCount(xColumn, yRow) > 0):
        AppendMessage('Cell cleared')
        interactBoard[yRow][xColumn] = InteractBoardCellState.CLICKED

    else:
        AppendMessage('Blank cell/s cleared')
        CascadeBlankCellReveal(xColumn, yRow)
    
    return False
    
def CascadeBlankCellReveal(xColumn, yRow):
    global interactBoard
    global staticBoard
    boardWidth, boardHeight = len(staticBoard[0]), len(staticBoard)
    
    if(not IsValidCoordinates(xColumn,yRow)):
        return
    
    if(GetCellAdjacentBombCount(xColumn, yRow) > 0):
        interactBoard[yRow][xColumn] = InteractBoardCellState.CLICKED
    elif(interactBoard[yRow][xColumn] == InteractBoardCellState.HIDDEN):
        interactBoard[yRow][xColumn] = InteractBoardCellState.CLICKED
        CascadeBlankCellReveal(xColumn+1, yRow+1)
        CascadeBlankCellReveal(xColumn+1, yRow-1)
        CascadeBlankCellReveal(xColumn+1, yRow)
        CascadeBlankCellReveal(xColumn-1, yRow+1)
        CascadeBlankCellReveal(xColumn-1, yRow-1)
        CascadeBlankCellReveal(xColumn-1, yRow)
        CascadeBlankCellReveal(xColumn, yRow+1)
        CascadeBlankCellReveal(xColumn, yRow-1)
    

def FlagCell(xColumn, yRow):
    global interactBoard
    global staticBoard
    cellState = interactBoard[yRow][xColumn]

    if(cellState == InteractBoardCellState.CLICKED):
        AppendMessage('Attempted to flag revealed cell; no action taken')
        return 0
    if(cellState == InteractBoardCellState.HIDDEN):
        AppendMessage('Cell flagged')
        interactBoard[yRow][xColumn] = InteractBoardCellState.FLAGGED
        if(staticBoard[yRow][xColumn] == StaticBoardCellContent.BOMB):
            return 1
        else:
            return -1
    if(cellState == InteractBoardCellState.FLAGGED):
        AppendMessage('Cell unflagged')
        interactBoard[yRow][xColumn] = InteractBoardCellState.HIDDEN
        if(staticBoard[yRow][xColumn] == StaticBoardCellContent.BOMB):
            return -1
        else:
            return 1


def GetCellAdjacentBombCount(xColumn, yRow):
    global staticBoard
    boardWidth, boardHeight = len(staticBoard[0]), len(staticBoard)
    adjBombCount = 0
    for y in range(yRow-1, yRow+2):
        for x in range(xColumn-1, xColumn+2):
            
            if (IsValidCoordinates(x,y) and staticBoard[y][x] == StaticBoardCellContent.BOMB):
                adjBombCount += 1
    return adjBombCount

def IsGameEnd(exploded, mines, flagScore):
    if(exploded):
        AppendMessage("You blew up a mine. Oops. GAME OVER")
        return True
    elif(mines == flagScore):
        AppendMessage("All mines were flagged! YOU WIN")
        return True
    return False

def IsValidCoordinates(xColumn, yRow):
    boardWidth, boardHeight = len(staticBoard[0]), len(staticBoard)
    validCoordinates = [
                xColumn >= 0,
                yRow >= 0,
                xColumn < boardWidth,
                yRow < boardHeight]
    return all(validCoordinates)
    

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

def UpdateVisualBoard(isGameEnd=False):
    global visualBoard
    global staticBoard
    boardWidth, boardHeight = len(staticBoard[0]), len(staticBoard)
    newBoard = []
    newBoard.append(GenerateBoardTopBorder(boardWidth))
    for row in reversed(range(boardHeight)):
        nextLine = '|'
        for column in range(boardWidth):
            icon = GetVisualBoardCellIcon(column, row, isGameEnd)
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

def GetVisualBoardCellIcon(xColumn, yRow, isGameEnd=False):
    global interactBoard
    global visualBoard

    if(interactBoard[yRow][xColumn] == InteractBoardCellState.HIDDEN):
        return TextStyle.GRAY + '?' + TextStyle.RESET

    if(interactBoard[yRow][xColumn] == InteractBoardCellState.FLAGGED):
        if(isGameEnd and staticBoard[yRow][xColumn] == StaticBoardCellContent.EMPTY):
            return TextStyle.YELLOW + '~' + TextStyle.RESET
        else:
            return TextStyle.RED + 'F' + TextStyle.RESET

    if(staticBoard[yRow][xColumn] == StaticBoardCellContent.BOMB):
        return TextStyle.RED+'*'+TextStyle.RESET if interactBoard[yRow][xColumn] != InteractBoardCellState.CLICKED else TextStyle.RED + 'X' + TextStyle.RESET

    # Anything else clicked by now is a number or clicked
    localBombCount = GetCellAdjacentBombCount(xColumn, yRow)
    return TextStyle.GREEN + str(localBombCount) + TextStyle.RESET if localBombCount > 0 else ' '



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

