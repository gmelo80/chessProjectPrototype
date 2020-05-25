
def printBoard(board):

    print("   +----+----+----+----+----+----+----+----+")

    for row in range (0, 8):
        print(" " + str((8-row)), end=" ")
        for col in range (0, 8):
            squareVal = board[row][col]
            print("| " + squareVal, end="  ")
        print("|")
        print("   +----+----+----+----+----+----+----+----+")
    print("     a     b    c    d   e     f   g     h  ")




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
    count = 0
    for possibleMove in game.possibleMoves:
        count += 1
        movements = movements + moveAsString(possibleMove, game.board) + ", "
        if count % 14 == 0:
            movements = movements + "\n"
    print("Possible moves: " + movements)

    eval_moves  = [m for m in game.possibleMoves if m.evaluation_completed]
    movements = ""
    for move_eval in eval_moves:
        movements = movements + moveAsString(move_eval, game.board) + ", "
    print("moves evaluated: " + movements)

def moveAsString(move, board):
    return  str(move)

def printGame(game):
    game.sortPossibleMoves()
    printBoard(game.board)
    print(" is white? " + str(game.isWhitesTurn()))

    print(" is white king under attack? " + str(game.whiteMovements.isKingUnderAttack))
    print(" is black king under attack? " + str(game.blackMovements.isKingUnderAttack))
    print(" bestMove score: " + str(game.bestMoveScoreAndDepth()))
    print(" board score: " + str(round(game.calculate_snapshot_core(), 3)))
    print("last Move [no=" + str(game.number_of_moves()) + "]: " + game.lastMoveStr())
    print("state: " + game.state())
    print("previous States: " + str(game.previousPositions))
    #print("white king moves: " + str(game.whiteMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.whiteMovements.kingValidMoves)))
    #print("black king moves: " + str(game.blackMovements.kingValidMoves) + " -- Score: " + str(game.scoreKingMoves(game.blackMovements.kingValidMoves)))
    print("eval time: " + str(game.get_evaluation_time()) + " secs")
    print("castle Flags: " + str(game.castle_flags))
    #print("can_black_castle_queen_side: " + str(game.can_black_castle_queen_side()))
    #print("can_black_castle_king_side: " + str(game.can_black_castle_king_side()))
    #print("can_white_castle_queen_side: " + str(game.can_white_castle_queen_side()))
    #print("can_white_castle_king_side: " + str(game.can_white_castle_king_side()))

    #print("game score: " + str(game.score()))
    #print("nodes evaluated: " + str(game.num_nodes_evaluated()))



    printPossibleMoves(game)

    if game.isCheckMate():
        print("==== CHECKMATE ======")
