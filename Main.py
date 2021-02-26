from Graphic.Board import *

numOfPlayers = int(input("Please enter number of players (2 or 4): "))
if numOfPlayers == 2:
    numOfAi = int(input("Please enter number of bots (0 or 1): "))
else:
    numOfAi = int(input("Please enter number of bots (0 - 3): "))
board = Board(numOfPlayers, numOfAi)
board.play()
