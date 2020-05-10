from chess import *
import time
from printfunctions import printBoard
from printfunctions import printAttacks
from printfunctions import printPossibleMoves
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

Board=[
        ['r', ' ', ' ', ' ', ' ', ' ', ' ', 'r'],
        [' ', ' ', ' ', 'k', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['R', ' ', ' ', ' ', 'K', ' ', ' ', 'R']];

#Board=KING_AND_ROOKS_POSITION
IsWhiteTurn=False



game = Game(Board, IsWhiteTurn)

move=None



while  move != "exit":
    printBoard(game.board)
    #printAttacks(game.whiteMovements.attacks, 'P')
    print(" is white? " + str(game.isWhitesTurn()))

    print(" is white king under attack? " + str(game.whiteMovements.isKingUnderAttack))
    print(" is black king under attack? " + str(game.blackMovements.isKingUnderAttack))
    print(" score: " + str(game.bestMoveScoreAndDepth()))
    print("last Move: " + game.lastMoveStr())
    print("state: " + game.state())
    print("previous States: " + str(game.previousPositions))
    print("white king moves: " + str(game.whiteMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.whiteMovements.kingValidMoves)))
    print("black king moves: " + str(game.blackMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.blackMovements.kingValidMoves)))

    printPossibleMoves(game)

    if game.isCheckMate():
        print("==== CHECKMATE ======")
        break

    moveStr=input("enter move or command:")

    if moveStr == "move":
        print(" thinking.....")
        start = time.time()
        game.doBestMove(20,4)
        end = time.time()
        print(" found move after " + str(end-start) + " secs !")
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
        game.move(r1, c1, r2, c2)


