import random
import json
from datetime import datetime
import threading
import queue
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
    for i in range(5):
        print(50 * "-")
        print("Round", i + 1, " of evolution")
        winners = []
        with open('population.txt', 'r') as file:
            population = json.load(file)
        random.shuffle(population)
        winners = winners + childProduction(population)
        j = 0
        que = queue.Queue()
        threads_list = list()
        start_time = datetime.now()
        while j < 20:
            print("#Thread", int(j/4+1), "finding winners of group", int(j/4+1), "...")
            t = threading.Thread(target=lambda q, arg1, arg2: q.put(finedWinners(arg1, arg2)), args=(que, population[j:j + 4], int(j/4+1)))
            t.start()
            threads_list.append(t)
            j += 4
        for t in threads_list:
            t.join()

        while not que.empty():
            result = que.get()
            winners = winners + result
        end_time = datetime.now()
        print('[Duration: {}]'.format(end_time - start_time))
        with open('population.txt', 'w') as file:
            json.dump(winners, file)
        with open('evolution-history.txt', 'a') as file:
            json.dump(winners, file)
            file.write("\n")


def finedWinners(population, threadNumber):
    scores = [0, 0, 0, 0]
    numOfActions = [0, 0, 0, 0]
    # print(population)
    for i in range(3):
        que = queue.Queue()
        threads_list = list()
        logic = Logic2P()
        ai1 = AI2P(logic, 8, population[0])
        ai2 = AI2P(logic, 0, population[1+i])
        t = threading.Thread(target=lambda q, arg1, arg2, arg3, arg4, arg5: q.put(playGame(arg1, arg2, arg3, arg4, arg5)),
                args=(que, ai1, ai2, 0, 1+i, logic))
        t.start()
        threads_list.append(t)
        if i == 0:
            j = 2
            k = 3
        else:
            j = 1
            k = 1 + i
        logic = Logic2P()
        ai1 = AI2P(logic, 8, population[j])
        ai2 = AI2P(logic, 0, population[k])
        t = threading.Thread(
            target=lambda q, arg1, arg2, arg3, arg4, arg5: q.put(playGame(arg1, arg2, arg3, arg4, arg5)),
            args=(que, ai1, ai2, j, k, logic))
        t.start()
        threads_list.append(t)
        for t in threads_list:
            t.join()
        while not que.empty():
            result = que.get()
            i, j, winner, actions = result
            numOfActions[i] += actions
            numOfActions[j] += actions
            if winner == 0:
                scores[i] += 1
            elif winner == 1:
                scores[j] += 1

    # print score board
    print("\tThread", threadNumber, "players score")
    for i in range(4):
        print("\t\t", i+1, 4*" ", scores[i])
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
    else:
        return winners[0:2]


def playGame(ai1, ai2, i, j, logic):
    numOfActions = 0
    turn = random.choice([0, 1])
    player1 = Player(Position(0, 4))
    player2 = Player(Position(8, 4))
    players = [player1, player2]
    while True:
        if numOfActions > 500:
            winner = -1
            break
        if turn == 0:
            action, row, col, tim = ai1.chooseAnAction(players[0], players[1])
        else:
            action, row, col, tim = ai2.chooseAnAction(players[1], players[0])
        numOfActions += 1
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
    return [i, j, winner, numOfActions]


def childProduction(winners):
    print("generating childes ...")
    random.shuffle(winners)
    childes = []
    numOfMutations = 0
    for i in range(0, len(winners), 2):
        break_point = random.choice([1, 2, 3])
        ch1 = []
        for j in range(break_point):
            ch1.append(winners[i][j])
        for j in range(break_point, 4):
            ch1.append(winners[i + 1][j])
        if random.random() <= 0.1:
            numOfMutations += 1
            mutation = random.choice([0, 1, 2, 3])
            ch1[mutation] = random.random()
            if ch1[mutation] == 0:
                ch1[mutation] = 1
        childes.append(ch1)
    print("\t", numOfMutations, "mutations")
    return childes


def chooseBestFactor():
    with open('population.txt', 'r') as file:
        population = json.load(file)
    random.shuffle(population)
    winners = []
    j = 0
    que = queue.Queue()
    threads_list = list()
    start_time = datetime.now()
    while j < 20:
        print("#Thread", int(j / 4 + 1), "finding winners of group", int(j / 4 + 1), "...")
        t = threading.Thread(target=lambda q, arg1, arg2: q.put(finedWinners(arg1, arg2)),
                             args=(que, population[j:j + 4], int(j / 4 + 1)))
        t.start()
        threads_list.append(t)
        j += 4
    for t in threads_list:
        t.join()

    while not que.empty():
        result = que.get()
        winners.append(result[0])
    print("finding winner of last group ...")
    scores = [0 for i in range(len(winners))]
    for i in range(len(winners)):
        for j in range(i+1, len(winners)):
            logic = Logic2P()
            ai1 = AI2P(logic, 8, population[i])
            ai2 = AI2P(logic, 0, population[j])
            t = threading.Thread(
                target=lambda q, arg1, arg2, arg3, arg4, arg5: q.put(playGame(arg1, arg2, arg3, arg4, arg5)),
                args=(que, ai1, ai2, i, j, logic))
            t.start()
            threads_list.append(t)
    for t in threads_list:
        t.join()
    while not que.empty():
        result = que.get()
        i, j, winner, actions = result
        if winner == 0:
            scores[i] += 1
        elif winner == 1:
            scores[j] += 1
    m = max(scores)
    mindx = [i for i, j in enumerate(scores) if j == m]
    print("best factors:", winners[mindx[0]])
    end_time = datetime.now()
    print('[Duration: {}]'.format(end_time - start_time))
    with open('final-factors.txt', 'w') as file:
        json.dump(winners[mindx[0]], file)


if __name__ == '__main__':
    # createEarlyPopulation()
    # main()
    chooseBestFactor()
