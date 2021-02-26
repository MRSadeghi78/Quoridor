from collections import deque
from Logic.Logic4P import *
from Graphic.Player import *
from Graphic.Position import *
import random

class AI4P:
    # sourse is a string that can be r0 or r8 or c0 or c8
    def __init__(self, logic: Logic4P, source):
        self.logic = logic
        self.source = source
                                    
    def chooseAnAction(self, players):
        p1 = Player(Position(players[0].pos.row, players[0].pos.col), None, None, players[0].walls)
        p2 = Player(Position(players[1].pos.row, players[1].pos.col), None, None, players[1].walls)
        p3 = Player(Position(players[2].pos.row, players[2].pos.col), None, None, players[2].walls)
        p4 = Player(Position(players[3].pos.row, players[3].pos.col), None, None, players[3].walls)
        ps = []
        if self.source == 'c0':
            ps = players[1:4] + players[0:1]
        elif self.source == 'r8':
            ps = players[2:4] + players[0:2]
        elif self.source == 'c8':
            ps = players[3:4] + players[0:3]
        else:
            ps = players
        alphaBeta = -1
        r = 0
        c = 0
        action = ""

        sp = -1;
        sr = 0;
        sc = 0;
        pmList = self.logic.possibleMoves(p1, p2, p3, p4);
        for pm in pmList:
            p = Player(Position(pm.row, pm.col), None, None, p1.walls);
            l = self.shortestPath(p, p2, p3, p4);
            if sp == -1 or l < sp:
                sp = l;
                sr = pm.row;
                sc = pm.col;
        

        for pm in pmList:
            p = Player(Position(pm.row, pm.col), None, None, p1.walls)
            a = self.minimaxTree(p, p2, p3, p4, 1, 0, 80)

            if pm.row == sr and pm.col == sc:
                a += 0.3;

            if a > alphaBeta:
                alphaBeta = a
                r = pm.row
                c = pm.col
                action = "move"
        if players[0].walls > 0:
            for row in range(players[2].pos.row - 2, players[2].pos.row + 2):
                for col in range(players[2].pos.col - 2, players[2].pos.col + 2):
                    if self.logic.addHwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80)
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != 'move'):
                            alphaBeta = a
                            r = row
                            c = col
                            action = 'add Hwall'
                        self.logic.hwalls[row][col] = False
                    if self.logic.addVwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80)
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != "move"):
                            alphaBeta = a
                            r = row
                            c = col
                            action = "add Vwall"
                        self.logic.vwalls[row][col] = False
            for row in range(players[3].pos.row - 2, players[3].pos.row + 2):
                for col in range(players[3].pos.col - 2, players[3].pos.col + 2):
                    if self.logic.addHwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80)
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != 'move'):
                            alphaBeta = a
                            r = row
                            c = col
                            action = 'add Hwall'
                        self.logic.hwalls[row][col] = False
                    if self.logic.addVwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80)
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != "move"):
                            alphaBeta = a
                            r = row
                            c = col
                            action = "add Vwall";
                        self.logic.vwalls[row][col] = False;
            for row in range(players[1].pos.row - 2, players[1].pos.row + 2):
                for col in range(players[1].pos.col - 2, players[1].pos.col + 2):
                    if self.logic.addHwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80);
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != 'move'):
                            alphaBeta = a;
                            r = row;
                            c = col;
                            action = 'add Hwall';
                        self.logic.hwalls[row][col] = False;
                    if self.logic.addVwall(col, row, ps):
                        a = self.minimaxTree(p1, p2, p3, p4, 1, 0, 80);
                        if a > alphaBeta or (a == alphaBeta and random.randint(0, 10) < 5 and action != "move"):
                            alphaBeta = a;
                            r = row;
                            c = col;
                            action = "add Vwall";
                        self.logic.vwalls[row][col] = False;
        return action, r, c;

    def isGoal(self, p: Player, s):
        if s == 'r0':
            return p.pos.row == 8 or p.pos.col == 0 or p.pos.col == 8;
        if s == 'c8':
            return p.pos.row == 8 or p.pos.col == 0 or p.pos.row == 0;
        if s == 'r8':
            return p.pos.row == 0 or p.pos.col == 0 or p.pos.col == 8;
        if s == 'c0':
            return p.pos.row == 8 or p.pos.row == 0 or p.pos.col == 8;


    def minimaxTree(self, player1: Player, player2: Player, player3: Player, player4: Player, d, l, r):
        sources = [];
        if self.source == 'r0':
            sources = ['r0', 'c8', 'r8', 'c0']
        if self.source == 'c8':
            sources = ['c8', 'r8', 'c0', 'r0']
        if self.source == 'r8':
            sources = ['r8', 'c0', 'r0', 'c8']
        if self.source == 'c0':
            sources = ['c0', 'r0', 'c8', 'r8']
        
        if d == 3:
            return self.heuristic(player1, player2, player3, player4, sources);

        if self.isGoal(player1, sources[0]):
            return 80;
        elif self.isGoal(player2, sources[1]) or self.isGoal(player3, sources[2]) or self.isGoal(player4, sources[3]):
            return 0;

        ps = [];
        if self.source == 'c0':
            ps = [player2, player3, player4, player1];
        elif self.source == 'r8':
            ps = [player3, player4, player1, player2];
        elif self.source == 'c8':
            ps = [player4, player1, player2, player3];
        else:
            ps = [player1, player2, player3, player4];
        
        if d % 4 == 0:
            #max
            alphaBeta = 0;
            for pm in self.logic.possibleMoves(player1, player2, player3, player4):
                p = Player(Position(pm.row, pm.col), None, None, player1.walls);
                a = self.minimaxTree(p, player2, player3, player4, d+1, l, r);
                alphaBeta = max(alphaBeta, a);
                if a >= r:
                    return alphaBeta;
                l = max(l, a);
            if player1.walls > 0:
                for row in range(player2.pos.row - 2, player2.pos.row + 2):
                    for col in range(player2.pos.col - 2, player2.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.vwalls[row][col] = False;
                for row in range(player3.pos.row - 2, player3.pos.row + 2):
                    for col in range(player3.pos.col - 2, player3.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.vwalls[row][col] = False;
                for row in range(player4.pos.row - 2, player4.pos.row + 2):
                    for col in range(player4.pos.col - 2, player4.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = max(alphaBeta, a);
                            if a >= r:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            l = max(l, a);
                            self.logic.vwalls[row][col] = False;
            return alphaBeta;

        elif d % 4 == 1:
        #min
            alphaBeta = 80;
            for pm in self.logic.possibleMoves(player2, player1, player3, player4):
                p = Player(Position(pm.row, pm.col), None, None, player2.walls);
                a = self.minimaxTree(player1, p, player3, player4, d+1, l, r);
                alphaBeta = min(alphaBeta, a);
                if a <= l:
                    return alphaBeta;
                r = max(r, a);
            if player2.walls > 0:
                for row in range(player1.pos.row - 2, player1.pos.row + 2):
                    for col in range(player1.pos.col - 2, player1.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.vwalls[row][col] = False;
            return alphaBeta;

        elif d % 4 == 2:
            #min
            alphaBeta = 80;
            for pm in self.logic.possibleMoves(player3, player1, player2, player4):
                p = Player(Position(pm.row, pm.col), None, None, player3.walls);
                a = self.minimaxTree(player1, player2, p, player4, d+1, l, r);
                alphaBeta = min(alphaBeta, a);
                if a <= l:
                    return alphaBeta;
                r = max(r, a);
            if player3.walls > 0:
                for row in range(player1.pos.row - 2, player1.pos.row + 2):
                    for col in range(player1.pos.col - 2, player1.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.vwalls[row][col] = False;  
            return alphaBeta;

        elif d % 4 == 3:
            #min
            alphaBeta = 80;
            for pm in self.logic.possibleMoves(player4, player1, player3, player2):
                p = Player(Position(pm.row, pm.col), None, None, player4.walls);
                a = self.minimaxTree(player1, player2, player3, p, d+1, l, r);
                alphaBeta = min(alphaBeta, a);
                if a <= l:
                    return alphaBeta;
                r = max(r, a);
            if player4.walls > 0:
                for row in range(player1.pos.row - 2, player1.pos.row + 2):
                    for col in range(player1.pos.col - 2, player1.pos.col + 2):
                        if self.logic.addHwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.hwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.hwalls[row][col] = False;
                        if self.logic.addVwall(col, row, ps):
                            a = self.minimaxTree(player1, player2, player3, player4, d + 1, l, r);
                            a = min(alphaBeta, a);
                            if a <= l:
                                self.logic.vwalls[row][col] = False;
                                return alphaBeta;
                            r = min(r, a);
                            self.logic.vwalls[row][col] = False;      
            return alphaBeta;

    def heuristic(self, player1: Player, player2: Player, player3: Player, player4: Player, sources):
        if self.isGoal(player1, sources[0]):
            return 80;
        if self.isGoal(player2, sources[1]) or self.isGoal(player3, sources[2]) or self.isGoal(player4, sources[3]):
            return 0;
        return (0.75 * (min(self.shortestPath(player2, player1, player3, player4), self.shortestPath(player3, player1, player2, player4), self.shortestPath(player4, player1, player3, player2)) - self.shortestPath(player1, player2, player3, player4)) + 0.15 * (player1.walls - max(player2.walls, player3.walls, player4.walls)) + 0.05 * (((self.countNearWalls(player2, player1, player3, player4) + self.countNearWalls(player3, player2, player1, player4) + self.countNearWalls(player4, player2, player3, player1)) / 3) - self.countNearWalls(player1, player2, player3, player4)) + 0.05 * (len(self.logic.possibleMoves(player1, player2, player3, player4)) - ((len(self.logic.possibleMoves(player2, player1, player3, player4)) + len(self.logic.possibleMoves(player3, player2, player1, player4)) + len(self.logic.possibleMoves(player4, player2, player3, player1))) / 3))) + 35;

    def countNearWalls(self, player1: Player, player2: Player, player3: Player, player4: Player):
        w = 0;
        if self.logic.isHwall(player1.pos.row, player1.pos.col):
            w += 1
        if self.logic.isHwall(player1.pos.row - 1, player1.pos.col):
            w += 1
        if self.logic.isVwall(player1.pos.row, player1.pos.col):
            w += 1
        if self.logic.isVwall(player1.pos.row, player1.pos.col - 1):
            w += 1
        for pm in self.logic.possibleMoves(player1, player2, player3, player4):
            if self.logic.isHwall(pm.row, pm.col):
                w += 1
            if self.logic.isHwall(pm.row - 1, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col):
                w += 1
            if self.logic.isVwall(pm.row, pm.col - 1):
                w += 1
        return w
    
    def shortestPath(self, player1: Player, player2: Player, player3: Player, player4: Player):
        mark = [[False for i in range(9)] for j in range(9)];
        p1 = Player(Position(player1.pos.row, player1.pos.col), None, None, player1.walls);
        q = deque();
        q.append((p1, 0));
        mark[p1.pos.row][p1.pos.col] = True;

        while q:
            p, d = q.popleft();
            if self.isGoal(p, self.source):
                return d;
            for pm in self.logic.possibleMoves(p, player2, player3, player4):
                if not mark[pm.row][pm.col]:
                    mark[pm.row][pm.col] = True;
                    p5 = Player(Position(pm.row, pm.col), None, None, player1.walls);
                    q.append((p5, d + 1));

        return -1;
