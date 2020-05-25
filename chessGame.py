from chess import *
import time
from printfunctions import printBoard
from printfunctions import printAttacks
from printfunctions import printGame
from positions import *

Board = [
    ['r', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['p', ' ', ' ', ' ', 'n', ' ', 'P', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'R', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', ' ', 'K', ' ', 'P', ' ', ' ', 'P'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'k', 'k', ' ', ' ', ' ', ' ']];

Board= [
    ['r', ' ', ' ', ' ', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'],
    [' ', ' ', 'n', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'b', ' ', 'q', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'N', 'P', ' ', 'N', 'P', ' '],
    ['P', 'P', 'P', 'B', 'Q', 'P', 'B', 'P'],
    ['R', ' ', ' ', ' ', ' ', 'R', 'K', ' ']];

Board= [
    ['r', 'n', 'b', ' ', 'k', ' ', 'n', 'r'],
    ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'],
    [' ', ' ', ' ', 'b', 'p', 'q', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'P', 'P', 'P', ' ', ' '],
    [' ', ' ', 'P', ' ', ' ', ' ', 'P', ' '],
    ['P', 'P', ' ', ' ', ' ', ' ', ' ', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']];

Board= [
    ['r', ' ', 'b', 'q', 'k', ' ', 'n', 'r'],
    ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'],
    [' ', ' ', 'n', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '],
    [' ', 'b', 'B', ' ', 'P', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'Q', ' ', ' '],
    ['P', ' ', 'P', 'P', ' ', 'P', 'P', 'P'],
    ['R', 'N', 'B', ' ', 'K', ' ', 'N', 'R']];




#Board=KING_AND_ROOKS_POSITION
#Board=INITIAL_POSITION
IsWhiteTurn=True



game = Game(Board, IsWhiteTurn)

move=None



while  move != "exit":
    printGame(game)

    moveStr=input("enter move or command:")

    if moveStr == "move":
        print(" thinking.....")
        start = time.time()
        game.doBestMove([30,1,1,1])
        end = time.time()
        print(" found move after " + str(end-start) + " secs !")
    elif moveStr.startswith("eval"):

        tokens = moveStr.split(":")[1].split(",")

        if len(tokens) >= 2:
            print(" evaluating, maxMoves "+moveStr.split(":")[1] +".....")

            maxMoveArray = []
            for t in tokens:
                param = (int(t.split("/")[0]), float(t.split("/")[1]))
                maxMoveArray.append(param)

            start = time.time()
            game.do_timed_evaluated_move_score(maxMoveArray)
            game.sortPossibleMoves()
            end = time.time()
            print(" evaluating time " + str(end-start) + " secs !")
        else:
            print(" evaluating, max time" + tokens[0] +".....")

            maxtime = int(tokens[0])
            start = time.time()
            game.evaluate_until_time(maxtime)
            end = time.time()
            print(" evaluating time " + str(end - start) + " secs !")

    elif moveStr == "undo":
        game.undo()
    elif moveStr == "exit":
        break;
    else:
        tokens = moveStr.split(",")
        r1 = int(tokens[0])
        c1 = int(tokens[1])
        r2 = int(tokens[2])
        c2 = int(tokens[3])
        if not game.move(r1, c1, r2, c2):
            print("move is INVALID!! ")


