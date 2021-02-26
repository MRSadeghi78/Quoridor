import random
import time
from collections import deque
from Logic.Logic2P import *
from Graphic.Player import *
from Graphic.Position import *


class AI2P:
    def __init__(self, logic: Logic2P, goal: int, heuristicFactors=[0.75, 0.15, 0.05, 0.05]):
        self.logic = logic
        self.goal = goal
        self.heuristicFactors = heuristicFactors
        self.maxOfHeuristic = 45*heuristicFactors[0] + 10*heuristicFactors[1] + 20*heuristicFactors[2] + 5*heuristicFactors[3]
        self.prevRow = -1
        self.prevCol = -1
        self.targetForChangeDepth = 15
        self.depth = 3

    def chooseAnAction(self, player1: Player, player2: Player):
        start = time.process_time()
        if player1.walls + player2.walls == self.targetForChangeDepth:
            self.depth += 1
            self.targetForChangeDepth -= 5
        p1 = Player(Position(player1.pos.row, player1.pos.col), None, None, player1.walls)
        p2 = Player(Position(player2.pos.row, player2.pos.col), None, None, player2.walls)
        alphaBeta = -1
        r = 0
        c = 0
        action = ""
        sp = -1
        sr = 0
        sc = 0
        for pm in self.logic.possibleMoves(player1, player2):
            p = Player(Position(pm.row, pm.col), None, None, p1.walls)
            l = self.shortestPath(p, p2, self.goal)
            if sp == -1 or l < sp:
                sp = l
                sr = pm.row
                sc = pm.col
        check = False
        if len(self.logic.possibleMoves(player1, player2)) > 1 and self.prevRow != -1:
            check = True
        for pm in self.logic.possibleMoves(player1, player2):
            if check and pm.row == self.prevRow and pm.col == self.prevCol:
                continue
            p = Player(Position(pm.row, pm.col), None, None, p1.walls)
            a = self.minimaxTree(p, p2, 1, 0, 80, self.depth)
            # if pm.row == sr and pm.col == sc:
            #     a += 0.3
            # print(a, "move", pm.row, pm.col)
            if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5):
                alphaBeta = a
                r = pm.row
                c = pm.col
                action = "move"
        if player1.walls > 0:
            for row in range(player2.pos.row - 2, player2.pos.row + 2):
                for col in range(player2.pos.col - 2, player2.pos.col + 2):
                    if self.logic.addHwall(col, row, p1, p2, self.goal):
                        a = self.minimaxTree(p1, p2, 1, 0, 80, self.depth)
                        # print(a, "add Hwall", row, col)
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != "move"):
                            alphaBeta = a
                            r = row
                            c = col
                            action = "add Hwall"
                        self.logic.hwalls[row][col] = False
                    if (row != 0 and row != 8) or (self.logic.isVwall(2 if row == 0 else 6, col)) \
                            or (self.logic.isHwall(row, col)) or (self.logic.isHwall(row, col + 1)):
                        if self.logic.addVwall(col, row, p1, p2, self.goal):
                            a = self.minimaxTree(p1, p2, 1, 0, 80, self.depth)
                            # print(a, "add Vwall", row, col)
                            if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != "move"):
                                alphaBeta = a
                                r = row
                                c = col
                                action = "add Vwall"
                            self.logic.vwalls[row][col] = False
        if action == "move":
            self.prevRow = player1.pos.row
            self.prevCol = player1.pos.col
        else:
            self.prevRow = -1
            self.prevCol = -1
        t = time.process_time() - start
        return action, r, c, t

    def minimaxTree(self, player1: Player, player2: Player, d, l, r, maxDepth):
        # TODO find the best depth for algorithm
        if d == maxDepth:
            return self.heuristic(player1, player2)
        if player1.pos.row == self.goal:
            return 80
        g = 0 if self.goal == 8 else 8
        if player2.pos.row == g:
            return 0
        if d % 2 == 1:
            # min
            alphaBeta = 80
            for pm in self.logic.possibleMoves(player2, player1):
                p = Player(Position(pm.row, pm.col), None, None, player2.walls)
                a = self.minimaxTree(player1, p, d + 1, l, r, maxDepth)
                alphaBeta = min(alphaBeta, a)
                if a <= l:
                    return alphaBeta
                r = min(r, a)
            if player2.walls > 0:
                for row in range(player1.pos.row - 1, player1.pos.row + 2):
                    for col in range(player1.pos.col - 2, player1.pos.col + 2):
                        if self.logic.addHwall(col, row, player1, player2, self.goal):
                            a = self.minimaxTree(player1, player2, d + 1, l, r, maxDepth)
                            alphaBeta = min(alphaBeta, a)
                            if a <= l:
                                self.logic.hwalls[row][col] = False
                                return alphaBeta
                            r = min(r, a)
                            self.logic.hwalls[row][col] = False
                        if (row != 0 and row != 8) or (self.logic.isVwall(2 if row == 0 else 6, col)) \
                                or (self.logic.isHwall(row, col)) or (self.logic.isHwall(row, col + 1)):
                            if self.logic.addVwall(col, row, player1, player2, self.goal):
                                a = self.minimaxTree(player1, player2, d + 1, l, r, maxDepth)
                                alphaBeta = min(alphaBeta, a)
                                if a <= l:
                                    self.logic.vwalls[row][col] = False
                                    return alphaBeta
                                r = min(r, a)
                                self.logic.vwalls[row][col] = False
            return alphaBeta
        else:
            # max
            alphaBeta = 0
            for pm in self.logic.possibleMoves(player1, player2):
                p = Player(Position(pm.row, pm.col), None, None, player1.walls)
                a = self.minimaxTree(p, player2, d + 1, l, r, maxDepth)
                alphaBeta = max(alphaBeta, a)
                if a >= r:
                    return alphaBeta
                l = max(l, a)
            if player1.walls > 0:
                for row in range(player2.pos.row - 1, player2.pos.row + 2):
                    for col in range(player2.pos.col - 2, player2.pos.col + 2):
                        if self.logic.addHwall(col, row, player1, player2, self.goal):
                            a = self.minimaxTree(player1, player2, d + 1, l, r, maxDepth)
                            alphaBeta = max(alphaBeta, a)
                            if a >= r:
                                self.logic.hwalls[row][col] = False
                                return alphaBeta
                            l = max(l, a)
                            self.logic.hwalls[row][col] = False
                        if (row != 0 and row != 8) or (self.logic.isVwall(2 if row == 0 else 6, col)) \
                                or (self.logic.isHwall(row, col)) or (self.logic.isHwall(row, col + 1)):
                            if self.logic.addVwall(col, row, player1, player2, self.goal):
                                a = self.minimaxTree(player1, player2, d + 1, l, r, maxDepth)
                                alphaBeta = max(alphaBeta, a)
                                if a >= r:
                                    self.logic.vwalls[row][col] = False
                                    return alphaBeta
                                l = max(l, a)
                                self.logic.vwalls[row][col] = False
            return alphaBeta

    def heuristic(self, player1: Player, player2: Player):
        # TODO add more factors
        if player1.pos.row == self.goal:
            return 80
        g = 0 if self.goal == 8 else 8
        if player2.pos.row == g:
            return 0
        return (self.heuristicFactors[0] * (self.shortestPath(player2, player1, 0 if self.goal == 8 else 8)
                        - self.shortestPath(player1, player2, self.goal))
                + self.heuristicFactors[1] * (player1.walls - player2.walls)
                + self.heuristicFactors[2] * (self.countNearWalls(player2, player1) - self.countNearWalls(player1, player2))
                + self.heuristicFactors[3] * (len(self.logic.possibleMoves(player1, player2))
                        - len(self.logic.possibleMoves(player2, player1)))
                + self.maxOfHeuristic) / (2 * self.maxOfHeuristic)

    def countNearWalls(self, player1: Player, player2: Player):
        w = 0
        if self.logic.isHwall(player1.pos.row, player1.pos.col):
            w += 1
        if self.logic.isHwall(player1.pos.row - 1, player1.pos.col):
            w += 1
        if self.logic.isVwall(player1.pos.row, player1.pos.col):
            w += 1
        if self.logic.isVwall(player1.pos.row, player1.pos.col - 1):
            w += 1
        for pm in self.logic.possibleMoves(player1, player2):
            if self.logic.isHwall(pm.row, pm.col):
                w += 1
            if self.logic.isHwall(pm.row - 1, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col - 1):
                w += 1
        return w

    def shortestPath(self, player1: Player, player2: Player, goal):
        mark = [[False for i in range(9)] for j in range(9)]
        p1 = Player(Position(player1.pos.row, player1.pos.col))
        q = deque()
        q.append((p1, 0))
        mark[p1.pos.row][p1.pos.col] = True

        while q:
            p, d = q.popleft()
            if p.pos.row == goal:
                return d
            for pm in self.logic.possibleMoves(p, player2):
                if not mark[pm.row][pm.col]:
                    mark[pm.row][pm.col] = True
                    p3 = Player(Position(p.pos.row, p.pos.col))
                    p3.pos.row = pm.row
                    p3.pos.col = pm.col
                    q.append((p3, d + 1))
        return -1
