
def printBoard(board):
    print("     0     1    2    3   4     5   6     7  ")
    print("   +----+----+----+----+----+----+----+----+")

    for row in range (0, 8):
        print(" " + str(row), end=" ")
        for col in range (0, 8):
            squareVal = board[row][col]
            print("| " + squareVal, end="  ")
        print("|")
        print("   +----+----+----+----+----+----+----+----+")





def printAttacks(attackMoves, piece):
    print("+----+----+----+----+----+----+----+----+")
    for row in attackMoves:
        for listOfAttacks in row:
            pieceFound = False
            for attackTupple in listOfAttacks:
                attackPiece = attackTupple[0]
                r = attackTupple[1]
                c = attackTupple[2]
                if attackPiece == piece:
                    print("| "+attackPiece+str(r)+str(c) , end="")
                    pieceFound=True
                    break

            if not pieceFound:
                print("| " , end="   ")
        print("|")
        print("+----+----+----+----+----+----+----+----+")

def printPossibleMoves(game):
    movements = ""
    for possibleMove in game.possibleMoves:
        movements = movements + moveAsString(possibleMove, game.board) + ", "
    print("Possible moves: " + movements)

def moveAsString(move, board):
    origin=board[move.r1][move.c1]
    return origin + str(move)

def printGame(game):
    printBoard(game.board)
    print(" is white? " + str(game.isWhitesTurn()))

    print(" is white king under attack? " + str(game.whiteMovements.isKingUnderAttack))
    print(" is black king under attack? " + str(game.blackMovements.isKingUnderAttack))
    print(" score: " + str(game.bestMoveScoreAndDepth()))
    print("last Move: " + game.lastMoveStr())
    print("state: " + game.state())
    print("previous States: " + str(game.previousPositions))
    print("white king moves: " + str(game.whiteMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.whiteMovements.kingValidMoves)))
    print("black king moves: " + str(game.blackMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.blackMovements.kingValidMoves)))

    print("castle Flags: " + str(game.castle_flags))
    print("can_black_castle_queen_side: " + str(game.can_black_castle_queen_side()))
    print("can_black_castle_king_side: " + str(game.can_black_castle_king_side()))
    print("can_white_castle_queen_side: " + str(game.can_white_castle_queen_side()))
    print("can_white_castle_king_side: " + str(game.can_white_castle_king_side()))



    printPossibleMoves(game)

    if game.isCheckMate():
        print("==== CHECKMATE ======")
