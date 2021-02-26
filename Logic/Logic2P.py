from Graphic.Position import *
from Graphic.Player import *


class Logic2P:

    def __init__(self):
        # horizontal walls
        self.hwalls = [[False for i in range(9)] for j in range(8)]
        # vertical walls
        self.vwalls = [[False for i in range(8)] for j in range(9)]

    def isHwall(self, r, c):
        if r >= 8 or c < 0 or c > 8 or r < 0:
            return False
        if c == 0:
            return self.hwalls[r][c]
        return self.hwalls[r][c] or self.hwalls[r][c - 1]

    def isVwall(self, r, c):
        # print(r, c)
        if c >= 8 or r < 0 or r > 8 or c < 0:
            return False
        if r == 0:
            return self.vwalls[r][c]
        return self.vwalls[r][c] or self.vwalls[r - 1][c]

    def possibleMoves(self, player1, player2):
        pm = []

        def goUp():
            if player1.pos.row == 0 or self.isHwall(player1.pos.row - 1, player1.pos.col):
                return
            if player2.pos.row == player1.pos.row - 1 and player2.pos.col == player1.pos.col:
                if player1.pos.row == 1 or self.isHwall(player1.pos.row - 2, player1.pos.col):
                    if not(player1.pos.col == 0 or self.isVwall(player1.pos.row - 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col - 1))
                    if not(player1.pos.col == 8 or self.isVwall(player1.pos.row - 1, player1.pos.col)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col + 1))
                else:
                    pm.append(Position(player1.pos.row - 2, player1.pos.col))
            else:
                pm.append(Position(player1.pos.row - 1, player1.pos.col))

        def goDown():
            if player1.pos.row == 8 or self.isHwall(player1.pos.row, player1.pos.col):
                return
            if player2.pos.row == player1.pos.row + 1 and player2.pos.col == player1.pos.col:
                if player1.pos.row == 7 or self.isHwall(player1.pos.row + 1, player1.pos.col):
                    if not(player1.pos.col == 0 or self.isVwall(player1.pos.row + 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col - 1))
                    if not(player1.pos.col == 8 or self.isVwall(player1.pos.row + 1, player1.pos.col)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col + 1))
                else:
                    pm.append(Position(player1.pos.row + 2, player1.pos.col))
            else:
                pm.append(Position(player1.pos.row + 1, player1.pos.col))

        def goLeft():
            if player1.pos.col == 0 or self.isVwall(player1.pos.row, player1.pos.col - 1):
                return
            if player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col - 1:
                if player1.pos.col == 1 or self.isVwall(player1.pos.row, player1.pos.col - 2):
                    if not(player1.pos.row == 0 or self.isHwall(player1.pos.row - 1, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col - 1))
                    if not(player1.pos.row == 8 or self.isHwall(player1.pos.row, player1.pos.col - 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col - 1))
                else:
                    pm.append(Position(player1.pos.row, player1.pos.col - 2))
            else:
                pm.append(Position(player1.pos.row, player1.pos.col - 1))

        def goRight():
            if player1.pos.col == 8 or self.isVwall(player1.pos.row, player1.pos.col):
                return
            if player2.pos.row == player1.pos.row and player2.pos.col == player1.pos.col + 1:
                if player1.pos.col == 7 or self.isVwall(player1.pos.row, player1.pos.col + 1):
                    if not(player1.pos.row == 0 or self.isHwall(player1.pos.row - 1, player1.pos.col + 1)):
                        pm.append(Position(player1.pos.row - 1, player1.pos.col + 1))
                    if not(player1.pos.row == 8 or self.isHwall(player1.pos.row, player1.pos.col + 1)):
                        pm.append(Position(player1.pos.row + 1, player1.pos.col + 1))
                else:
                    pm.append(Position(player1.pos.row, player1.pos.col + 2))
            else:
                pm.append(Position(player1.pos.row, player1.pos.col + 1))

        goUp()
        goLeft()
        goRight()
        goDown()
        return pm

    def isSurrounded(self, player2, player1, des):
        blocks = []
        visited = [[False for x in range(9)] for y in range(9)]
        p = Player(Position(player1.pos.row, player1.pos.col))
        blocks.append(p.pos)
        while blocks:
            p.pos = blocks.pop()
            temp = self.possibleMoves(p, player2)
            for t in temp:
                if not visited[t.row][t.col]:
                    if t.row == des:
                        return False
                    visited[t.row][t.col] = True
                    blocks.append(t)
        return True

    def addHwall(self, c1, r1, player2, player1, des):
        if r1 < 0 or r1 > 7 or c1 < 0 or c1 > 7:
            return False
        if self.hwalls[r1][c1 - 1] or self.hwalls[r1][c1] or self.hwalls[r1][c1+1] or self.vwalls[r1][c1]:
            return False
        self.hwalls[r1][c1] = True
        if self.isSurrounded(player1, player2, des) or self.isSurrounded(player2, player1, 0 if des == 8 else 8):
            self.hwalls[r1][c1] = False
            return False
        return True

    def addVwall(self, c1, r1, player2, player1, des):
        if r1 < 0 or r1 > 7 or c1 < 0 or c1 > 7:
            return False
        if self.vwalls[r1 - 1][c1] or self.vwalls[r1][c1] or self.vwalls[r1+1][c1] or self.hwalls[r1][c1]:
            return False
        self.vwalls[r1][c1] = True
        if self.isSurrounded(player1, player2, des) or self.isSurrounded(player2, player1, 0 if des == 8 else 8):
            self.vwalls[r1][c1] = False
            return False
        return True
