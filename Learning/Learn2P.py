import random
import json
from datetime import datetime
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AI.AI2P import AI2P
from Logic.Logic2P import Logic2P
from Graphic.Player import Player
from Graphic.Position import Position


def createEarlyPopulation():
    print("generating early population ...")
    earlyPopulation = []
    for i in range(20):
        p = []
        for j in range(4):
            a = random.random()
            if a == 0:
                a = 1
            p.append(a)
        earlyPopulation.append(p)
    with open('population.txt', 'w') as file:
        json.dump(earlyPopulation, file)
    with open('evolution-history.txt', 'a') as file:
        json.dump(earlyPopulation, file)
        file.write("\n")


def main():
    for i in range(20):
        print(50 * "-")
        print("Round", i + 1, " of evolution")
        winners = []
        with open('population.txt', 'r') as file:
            population = json.load(file)
        random.shuffle(population)
        j = 0
        start_t = datetime.now()
        while j < 20:
            print("finding winners of group", int(j/4+1), "...")
            start_time = datetime.now()
            for winner in finedWinners(population[j:j + 4]):
                winners.append(winner)
            j += 4
            end_time = datetime.now()
            print('[Duration: {}]'.format(end_time - start_time))
        end_time = datetime.now()
        print('[Duration: {}]'.format(end_time - start_time))
        winners = winners + childProduction(winners)
        print(winners)
        with open('population.txt', 'w') as file:
            json.dump(winners, file)
        with open('evolution-history.txt', 'a') as file:
            json.dump(winners, file)
            file.write("\n")


def finedWinners(population):
    scores = [0, 0, 0, 0]
    numOfActions = [0, 0, 0, 0]
    for i in range(4):
        for j in range(i+1, 4):
            logic = Logic2P()
            turn = random.choice([0, 1])
            player1 = Player(Position(0, 4))
            player2 = Player(Position(8, 4))
            players = [player1, player2]
            ai1 = AI2P(logic, 8, population[i])
            ai2 = AI2P(logic, 0, population[j])
            while True:
                if turn == 0:
                    action, row, col, tim = ai1.chooseAnAction(players[0], players[1])
                else:
                    action, row, col, tim = ai2.chooseAnAction(players[1], players[0])
                numOfActions[i] += 1
                numOfActions[j] += 1
                if action == "move":
                    players[turn].pos.row = row
                    players[turn].pos.col = col
                    if turn == 1 and row == 0:
                        winner = 1
                        break
                    elif turn == 0 and row == 8:
                        winner = 0
                        break
                elif action == "add Vwall":
                    if logic.addVwall(col, row, players[turn], players[0 if turn == 1 else 1], 8 if turn == 0 else 0):
                        players[turn].walls -= 1
                elif action == "add Hwall":
                    if logic.addHwall(col, row, players[turn], players[0 if turn == 1 else 1],
                                           8 if turn == 0 else 0):
                        players[turn].walls -= 1
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            if winner == 0:
                scores[i] += 1
            else:
                scores[j] += 1

    # print score board
    print("\tplayer score")
    for i in range(4):
        print("\t", i+1, 4*" ", scores[i])
    m = max(scores)
    winners = [i for i, j in enumerate(scores) if j == m]
    if len(winners) == 1:
        rs = [population[winners[0]]]
        m2 = 0
        mindx = 0
        for i in range(4):
            if scores[i] > m2 and scores[i] != m:
                m2 = scores[i]
                mindx = i
            elif scores[i] == m2:
                if numOfActions[i] <= numOfActions[mindx]:
                    m2 = scores[i]
                    mindx = i
        rs.append(population[mindx])
        return rs
    elif len(winners) == 2:
        return [population[winners[0]], population[winners[1]]]
    elif len(winners) == 3:
        if numOfActions[winners[0]] >= numOfActions[winners[1]] and numOfActions[winners[0]] >= numOfActions[winners[2]]:
            return [population[winners[1]], population[winners[2]]]
        elif numOfActions[winners[1]] >= numOfActions[winners[0]] and numOfActions[winners[1]] >= numOfActions[winners[2]]:
            return [population[winners[0]], population[winners[2]]]
        else:
            return [population[winners[0]], population[winners[1]]]


def childProduction(winners):
    print("generating childes ...")
    random.shuffle(winners)
    childes = []
    numOfMutations = 0
    for i in range(0, len(winners), 2):
        break_point = random.choice([1, 2, 3])
        ch1 = []
        ch2 = []
        for j in range(break_point):
            ch1.append(winners[i][j])
            ch2.append(winners[i + 1][j])
        for j in range(break_point, 4):
            ch1.append(winners[i + 1][j])
            ch2.append(winners[i][j])
        if random.random() <= 0.1:
            numOfMutations += 1
            mutation = random.choice([0, 1, 2, 3])
            ch1[mutation] = random.random()
            if ch1[mutation] == 0:
                ch1[mutation] = 1
        if random.random() <= 0.1:
            numOfMutations += 1
            mutation = random.choice([0, 1, 2, 3])
            ch2[mutation] = random.random()
            if ch2[mutation] == 0:
                ch2[mutation] = 1
        childes.append(ch1)
        childes.append(ch2)
    print("\t", numOfMutations, "mutations")
    return childes


if __name__ == '__main__':
    createEarlyPopulation()
    main()
