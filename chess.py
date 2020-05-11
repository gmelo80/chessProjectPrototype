from printfunctions import printBoard
from printfunctions import printAttacks
from printfunctions import printPossibleMoves
from positions import INITIAL_POSITION

import time


def pawnAttackSquares(is_white, row, col):
    attackSquares = []
    increment = -1 if is_white else 1;
    if (col-1) >= 0: attackSquares.append((row+increment,col-1))
    if (col+1) < 8: attackSquares.append((row+increment,col+1))
    return attackSquares

def kingAttackSquares(row, col):
    attackSquares = []
    maxRow = min(row + 1, 7)
    minRow = max(row - 1, 0)
    maxCol = min(col + 1, 7)
    minCol = max(col - 1, 0)

    for r in range(minRow, maxRow + 1):
        for c in range(minCol, maxCol + 1):
            if (r != row or c != col):
                attackSquares.append((r, c))
    return attackSquares

def knightAttackSquares(row, col):
    attackSquares = []
    maxRow = min(row + 2, 7)
    minRow = max(row - 2, 0)
    maxCol = min(col + 2, 7)
    minCol = max(col - 2, 0)
    for r in range(minRow, maxRow + 1):
        for c in range(minCol, maxCol + 1):
            if (abs(r - row) == 2 and abs(c - col) == 1) or (abs(r - row) == 1 and abs(c - col) == 2):
                attackSquares.append((r, c))
    return attackSquares

def queenAttackSquares(row, col, board):
    return bishopAttackSquares(row, col, board) + rookAttackSquares(row, col, board)


def bishopAttackSquares(row, col, board):
    attackSquares = []

    c = col
    for r in range(row+1, 8):
        c += 1
        if c > 7: break
        attackSquares.append((r, c))
        if board[r][c] != ' ':
            break;
    c = col
    for r in range(row-1, -1, -1):
        c += 1
        if c > 7: break
        attackSquares.append((r, c))
        if board[r][c] != ' ':
            break;

    c = col
    for r in range(row+1, 8):
        c -= 1
        if c < 0: break
        attackSquares.append((r, c))
        if board[r][c] != ' ':
            break;

    c = col
    for r in range(row-1, -1, -1):
        c -= 1
        if c < 0: break
        attackSquares.append((r, c))
        if board[r][c] != ' ':
            break;

    return attackSquares

def rookAttackSquares(row, col, board):
    attackSquares = []

    for r in range(row+1, 8):
        attackSquares.append((r, col))
        if board[r][col] != ' ':
            break;

    for r in range(row-1, -1, -1):
        attackSquares.append((r, col))
        if board[r][col] != ' ':
            break;

    for c in range(col+1, 8):
        attackSquares.append((row, c))
        if board[row][c] != ' ':
            break;

    for c in range(col-1, -1, -1):
        attackSquares.append((row, c))
        if board[row][c] != ' ':
            break;

    return attackSquares


def attackSquares(piece, row, col, board):
    if piece.upper() == 'K':
        return kingAttackSquares(row, col)
    elif piece.upper() == 'R':
        return rookAttackSquares(row, col, board)
    elif piece.upper() == 'B':
        return bishopAttackSquares(row, col, board)
    elif piece.upper() == 'Q':
        return queenAttackSquares(row, col, board)
    elif piece.upper() == 'N':
        return knightAttackSquares(row, col)
    elif piece.upper() == 'P':
        return pawnAttackSquares(piece.isupper(), row, col)

    return []


def calculateMovements(board, can_castle_status):
    # first clean up the attacks
    whiteKingSquare= None;
    blackKingSquare = None;

    whitePawnMoves = []
    blackPawnMoves = []

    whiteAttackMoves = []
    blackAttackMoves = []
    for r in range(0, 8):
        whiteAttackMoves.append([])
        blackAttackMoves.append([])
        for c in range(0, 8):
            whiteAttackMoves[r].append([])
            blackAttackMoves[r].append([])

    # re-calculate for each piece on the board
    for r in range(0, 8):
        for c in range(0, 8):
            piece = board[r][c]

            pieceAttacksSquares = attackSquares(piece, r, c, board)

            if piece == 'k':
                blackKingAttackSquares = pieceAttacksSquares
                blackKingSquare = (r, c)
            elif piece == 'K':
                whiteKingAttackSquares = pieceAttacksSquares
                whiteKingSquare = (r, c)
            elif piece == 'P' and board[r-1][c] == ' ':
                whitePawnMoves.append((r,c,r-1,c))
                # pawn jump
                if r == 6 and board[r-2][c] == ' ':
                    whitePawnMoves.append((r, c, r - 2, c))
            elif piece == 'p'and board[r+1][c] == ' ':
                blackPawnMoves.append((r,c,r+1,c))
                # pawn jump
                if r == 1 and board[r+2][c] == ' ':
                    blackPawnMoves.append((r, c, r + 2, c))
            for attackSquare in pieceAttacksSquares:
                moveOrigin = (piece, r, c)
                attackRow = attackSquare[0];
                attackCol = attackSquare[1];
                if isWhitePiece(piece):
                    whiteAttackMoves[attackRow][attackCol].append(moveOrigin)
                else:
                    blackAttackMoves[attackRow][attackCol].append(moveOrigin)

    # mark if king is under Attack
    blackKingIsUnderAttack = False
    if whiteAttackMoves[blackKingSquare[0]][blackKingSquare[1]]:
       blackKingIsUnderAttack = True

    whiteKingIsUnderAttack = False
    if blackAttackMoves[whiteKingSquare[0]][whiteKingSquare[1]]:
       whiteKingIsUnderAttack = True

    blackKingValidMoves = []
    for blackKingAttack in blackKingAttackSquares:
        if not whiteAttackMoves[blackKingAttack[0]][blackKingAttack[1]] and not isBlackPiece(board[blackKingAttack[0]][blackKingAttack[1]]):
            blackKingValidMoves.append(blackKingAttack)

    whiteKingValidMoves = []
    for whiteKingAttack in whiteKingAttackSquares:
        if not blackAttackMoves[whiteKingAttack[0]][whiteKingAttack[1]] and not isWhitePiece(board[whiteKingAttack[0]][whiteKingAttack[1]]):
            whiteKingValidMoves.append(whiteKingAttack)

    # check castle moves


    whiteMoves = Movements(whiteAttackMoves, whiteKingSquare, whiteKingIsUnderAttack, whiteKingValidMoves, whitePawnMoves, True, True)
    blackMoves = Movements(blackAttackMoves, blackKingSquare, blackKingIsUnderAttack, blackKingValidMoves, blackPawnMoves, True, True)

    return (whiteMoves, blackMoves)


def isWhitePiece(piece):
    return piece.isupper()



def isBlackPiece(piece):
    return piece != ' ' and not isWhitePiece(piece)

def isSameColor(piece1, piece2):
    return ( isWhitePiece(piece1) and isWhitePiece(piece2) ) or ( isBlackPiece(piece1) and isBlackPiece(piece2))

def rowAsStr(boardRow):
    rowStr = ""
    spaceCount = 0
    for val in boardRow:
        if val == " ":
            spaceCount += 1
        else:
            if spaceCount > 0:
                rowStr = rowStr+ str(spaceCount) + val
            else:
                rowStr = rowStr + val
            spaceCount=0
    if spaceCount > 0:
        rowStr = rowStr + str(spaceCount)

    return rowStr


class MoveNode:
    def __init__(self, r1, c1, r2, c2, score, depthEvaluated=0):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
        self.score = score
        self.depthEvaluated = depthEvaluated

    def __str__(self):
        return "["+str(self.r1)+","+str(self.c1)+" -> "+str(self.r2)+","+str(self.c2)+"]("+str(self.score)+"/"+str(self.depthEvaluated)+")"

class SquarePositionValue:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return "(" + self.value+str(self.row) +"-"+str(self.col)+")"

class HistoryState:
    def __init__(self, square_pos_value_list, white_movements, black_movements, possible_moves, castle_flags):
        self.square_pos_value_list = square_pos_value_list
        self.white_movements = white_movements
        self.black_movements = black_movements
        self.possible_moves = possible_moves
        self.castle_flags = castle_flags
    def __str__(self):
        val = ""
        for s in self.square_pos_value_list:
            val += str(s)
        return val


class Game:

    def __init__(self, board, whiteStarts):
        self.MAX_SCORE = 1000000
        self.attackScore = 0.0
        self.kindMoveFactor = 0.01
        self.pawn_move_score_factor = 0.05
        self.pieceScoreMap = {
            " ": 0,
            "K": 0,
            "R": 5,
            "N": 3,
            "B": 3.1,
            "Q": 9,
            "P": 1
        }
        self.castle_flags = {
            "black_king_side": True,
            "black_queen_side": True,
            "white_king_side": True,
            "white_queen_side": True
        }

        self.board = board
        self.whiteStarts = whiteStarts
        self.movementHistory = []
        self.previousPositions = {}
        self.whiteMovements = []
        self.blackMovements = []
        self.possibleMoves = []
        self.calculateMoves()
        self.evaluation_start_time = 0
        self.evaluation_end_time = 0


    def state(self):
        stateStr = ""
        for row in self.board:
            stateStr += rowAsStr(row) + "-"
        return stateStr


    def calculateMoves(self):
        (self.whiteMovements, self.blackMovements) = calculateMovements(self.board, self.castle_flags)
        self.possibleMoves = self.generatePossibleMoves()

    def can_black_castle_queen_side(self):
        if self.castle_flags["black_queen_side"] and self.board[0][4] == 'k' and self.board[0][0] == 'r' and self.board[0][1] == ' ' and self.board[0][2] == ' ' and self.board[0][3] == ' ':
            return not self.whiteMovements.attacks[0][4] and not self.whiteMovements.attacks[0][3] and not self.whiteMovements.attacks[0][2]
        else:
            return False

    def can_black_castle_king_side(self):
        if self.castle_flags["black_king_side"] and self.board[0][4] == 'k' and self.board[0][7] == 'r' and self.board[0][5] == ' ' and self.board[0][6] == ' ':
            return not self.whiteMovements.attacks[0][4] and not self.whiteMovements.attacks[0][5] and not self.whiteMovements.attacks[0][6]
        else:
            return False

    def can_white_castle_queen_side(self):
        if self.castle_flags["white_queen_side"] and self.board[7][4] == 'K' and self.board[7][0] == 'R' and self.board[7][1] == ' ' and self.board[7][2] == ' ' and self.board[7][3] == ' ':
            return not self.blackMovements.attacks[7][4] and not self.blackMovements.attacks[7][3] and not self.blackMovements.attacks[7][2]
        else:
            return False

    def can_white_castle_king_side(self):
        if self.castle_flags["white_king_side"] and self.board[7][4] == 'K' and self.board[7][7] == 'R' and self.board[7][5] == ' ' and self.board[7][6] == ' ':
            return not self.blackMovements.attacks[7][4] and not self.blackMovements.attacks[7][5] and not self.blackMovements.attacks[7][6]
        else:
            return False

    def generatePossibleMoves(self):

        movements = self.whiteMovements if self.isWhitesTurn() else self.blackMovements
        attackMoves = movements.attacks
        pawnMoves = movements.pawnMoves



        possibleMoves = []
        for r2 in range(0, 8):
            for c2 in range(0, 8):
                for attack in attackMoves[r2][c2]:
                    r1 = attack[1]
                    c1 = attack[2]
                    if self.tryMove(r1, c1, r2, c2):
                        moveNode = MoveNode(r1, c1, r2, c2, self.score())
                        possibleMoves.append(moveNode)
                        if not self.undo():
                            print("failed undo - 1 -" + str(len(self.movementHistory)))

        for pawnMove in pawnMoves:
            r1 = pawnMove[0]
            c1 = pawnMove[1]
            r2 = pawnMove[2]
            c2 = pawnMove[3]
            if self.tryMove(r1, c1, r2, c2):
                moveNode = MoveNode(r1, c1, r2, c2, self.score())
                possibleMoves.append(moveNode)
                if not self.undo():
                    print("failed undo - 2 -" + str(len(self.movementHistory)))

        # generate castle moves
        # opositeAttacks = self.blackMovements.attacks if self.isWhitesTurn() else self.whiteMovements.attacks
        # r1 = movements.kingPosition[0]
        # c1 = movements.kingPosition[1]
        # castleScore = 0.01
        # if movements.canCastleKingSide and not movements.isKingUnderAttack:
        #      if len(opositeAttacks[r1][c1+1]) + len(opositeAttacks[r1][c1+2]) == 0:
        #          moveNode = MoveNode(r1, c1, r1, c1+2, self.score() + castleScore)
        #          possibleMoves.append(moveNode)
        #  if movements.canCastleQueenSide and not movements.isKingUnderAttack:
        #      if len(opositeAttacks[r1][c1-1]) + len(opositeAttacks[r1][c1-2]) == 0:
        #          moveNode = MoveNode(r1, c1, r1, c1+2, self.score() + castleScore)
        #          possibleMoves.append(moveNode)


        return sorted(possibleMoves, key=lambda moveNode : moveNode.score, reverse=self.isWhitesTurn())

    def moveIfPossible(self, r1, c1, r2, c2):
        for m in self.possibleMoves:
            if m.r1 == r1 and m.r2 == r2 and m.c1 == c1 and m.c2 == c2:
                return self.move(r1, c1, r2, c2)

        return False



    def move(self, r1, c1, r2, c2, validate=True):
        if validate and not self.passBasicValidation(r1, c1, r2, c2):
           return False;

        if not self.tryMove(r1, c1, r2, c2, validate):
            #squareValue1 = self.board[r1][c1]
            #print("invalid move king is in a attacked square", str(self.isWhitesTurn()), squareValue1, r1, r2, c1, c2)
            #printBoard(self.board)
            return False
        else:
            self.calculateMoves()
            # update castle flags
            self.castle_flags["black_king_side"] = self.castle_flags["black_king_side"] and not ( (r1 == 0) and (c1 == 4 or c1 == 7))
            self.castle_flags["black_queen_side"] = self.castle_flags["black_queen_side"] and not ((r1 == 0) and (c1 == 4 or c1 == 0))
            self.castle_flags["white_king_side"] = self.castle_flags["white_king_side"] and not ((r1 == 7) and (c1 == 4 or c1 == 7))
            self.castle_flags["white_queen_side"] = self.castle_flags["white_queen_side"] and not ((r1 == 7) and (c1 == 4 or c1 == 0))
            return True;

    def doValidatedMove(self, moveNode):
        self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2, False)




    def tryMove(self, r1, c1, r2, c2, validate=True):

        squareValue1 = self.board[r1][c1]
        squareValue2 = self.board[r2][c2]

        if validate and isSameColor(squareValue1, squareValue2):
            return False

        if validate and squareValue1.upper() == 'P':
            if squareValue2 == ' ' and c1 != c2:
                return False

        isWhitesTurn = self.isWhitesTurn()
        #move = (r1, c1, squareValue1, r2, c2, squareValue2, self.whiteMovements, self.blackMovements, self.possibleMoves)

        saved_positions = [SquarePositionValue(squareValue1, r1, c1), SquarePositionValue(squareValue2, r2, c2)]
        historyState = HistoryState(saved_positions, self.whiteMovements, self.blackMovements, self.possibleMoves, self.castle_flags.copy())

        # if pawn promotion
        if squareValue1 == 'P' and r2 == 0: squareValue1 = 'Q'
        elif squareValue1 == 'p' and r2 == 7: squareValue1 = 'q'

        self.board[r1][c1] = ' '
        self.board[r2][c2] = squareValue1
        #self.movementHistory.append(move)
        self.movementHistory.append(historyState)

        positionStr = self.state()
        if positionStr in self.previousPositions:
            self.previousPositions[positionStr] = self.previousPositions[positionStr] + 1
        else:
            self.previousPositions[positionStr] = 1



        (self.whiteMovements, self.blackMovements) = calculateMovements(self.board, self.castle_flags)
        #print("trying [" + str(r1) +"," + str(c1) +"->" + str(r2) +"," + str(c2) +"]" )
        if validate and self.isKingUnderAttack(isWhitesTurn):
            if not self.undo():
                print("failed undo - under attack undo -" + str(len(self.movementHistory)))
            return False

        return True

    def lastMoveStr(self):
        if self.movementHistory:
            lastMoveState = self.movementHistory[-1]
            return str(lastMoveState)
        else:
            return "none"


    # deprecated - no longer in use
    def passBasicValidation(self, r1, c1, r2, c2):
        squareValue1 = self.board[r1][c1]
        squareValue2 = self.board[r2][c2]
        if self.isWhitesTurn():
                if not isWhitePiece(squareValue1):
                    print("invalid move, it is white's turn but the square has [" + squareValue1 + "]")
                    return False;
        else:
            if not isBlackPiece(squareValue1):
                print("invalid move, it is blacks's turn but the square has [" + squareValue1 + "]")
                return False

        # validate capture
        if isSameColor(squareValue1, squareValue2):
            print("invalid move, origin/destination has same color")
            return False

        if squareValue1.upper() == 'P':
            if squareValue2 == ' ':
                return c1 == c2

        if self.isWhitesTurn():
            if not self.whiteMovements.attacks[r2][c2]:
                print(str((r1, c1, r2, c2)) + " - invalid move for white, valid moves for " + squareValue1 + " are:")
                printAttacks(self.whiteMovements.attacks, squareValue1)
                printBoard(self.board)
                return False
        else:
            if not self.blackMovements.attacks[r2][c2]:
                print(str((r1, c1, r2, c2)) + " - invalid move for black, valid moves for " + squareValue1 + " are:")
                printAttacks(self.blackMovements.attacks, squareValue1)
                printBoard(self.board)
                return False
        # is valid
        return True


    def isKingUnderAttack(self, isWhitesTurn):
        if isWhitesTurn:
            return self.whiteMovements.isKingUnderAttack
        else:
            return self.blackMovements.isKingUnderAttack


    def isWhitesTurn(self):
        if not self.movementHistory:
            return self.whiteStarts
        else:
            historyState = self.movementHistory[-1]
            lastPieceMoved = historyState.square_pos_value_list[0].value
            return isBlackPiece(lastPieceMoved)

    def undo(self):
        if len(self.movementHistory) > 0:
            historyState = self.movementHistory.pop()

            self.whiteMovements = historyState.white_movements
            self.blackMovements = historyState.black_movements
            self.possibleMoves = historyState.possible_moves
            self.castle_flags = historyState.castle_flags

            positionStr = self.state()

            for square_pos in historyState.square_pos_value_list:
                self.board[square_pos.row][square_pos.col] = square_pos.value

            self.previousPositions[positionStr] = self.previousPositions[positionStr] - 1
            if self.previousPositions[positionStr] == 0:
                self.previousPositions.pop(positionStr)

            return True
        else:
            print("no moves to undo")
            return False



    def score(self):
        if self.is_draw_by_repetion():
            return 0.0

        points = 0.0
        for r in range(0,8):
            for c in range(0,8):
                points += self.positionScore(r,c)
                points += self.score_if_is_pawn(r,c)

        if self.isFinal():
            if self.isWhitesTurn():
                points += self.scoreKingMoves(self.whiteMovements.kingValidMoves)
            else:
                points -= self.scoreKingMoves(self.blackMovements.kingValidMoves)
        return points

    def isCheckMate(self):
        return not self.possibleMoves and self.isKingUnderAttack(self.isWhitesTurn())

    def isStaleMate(self):
        return not self.possibleMoves and not self.isKingUnderAttack(self.isWhitesTurn())

    def is_draw_by_repetion(self):
        positionStr = self.state()
        return positionStr in self.previousPositions and self.previousPositions[positionStr] > 3

    def bestMoveScoreAndDepth(self):
        if self.possibleMoves:
            return self.possibleMoves[0].score, self.possibleMoves[0].depthEvaluated
        else:
            if self.isCheckMate():
                sign = -1.0 if self.isWhitesTurn() else 1.0
                return self.MAX_SCORE * sign, self.MAX_SCORE

            if self.isStaleMate():
                return 0.0, self.MAX_SCORE


    # no longer in use
    def evaluateBestNode(self):
        moveNode = self.possibleMoves[0]
        self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2)

        newScore, depth = self.bestMoveScoreAndDepth()
        if not self.undo():
            print("failed to undo xx", str(moveNode))
            printBoard(self.board)
        moveNode.score = newScore
        moveNode.depthEvaluated = moveNode.depthEvaluated+1
        self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode : moveNode.score, reverse=self.isWhitesTurn())

    def doBestMove(self, maxMoves, depth):
        self.evaluation_start_time = time.time()
        self.evaluateMoveScore(maxMoves, depth)
        self.evaluation_end_time = time.time()
        print("total time: ", (self.evaluation_end_time - self.evaluation_start_time), " secs")
        if self.possibleMoves:
            bestMoveNode = self.possibleMoves[0]
            return self.move(bestMoveNode.r1, bestMoveNode.c1, bestMoveNode.r2, bestMoveNode.c2)
        return False


    # for each possible move, update the score value by making a tree search
    # this method will execute moves and undo to update the scores
    def evaluateMoveScore(self, maxMoves, depth):
        if depth == 0:
            newScore, depth = self.bestMoveScoreAndDepth()
            return newScore
        else:
            # it will perform a tree search just on the first moves
            movementsToCheck = min(maxMoves, len(self.possibleMoves))
            for moveNumber in range(0, movementsToCheck):
                moveNode = self.possibleMoves[moveNumber]

                # this need to change to move without validation
                #move_sucess = self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2)
                move_sucess = self.doValidatedMove(moveNode)

                # each time it search depth the number of moves are reduced
                newMaxMoves = max(1, maxMoves//4)
                # update the move score
                moveNode.score = self.evaluateMoveScore(newMaxMoves, depth-1)
                moveNode.depthEvaluated = depth
                if not self.undo():
                    print("failed to undo z", str(moveNode) , " --> " ,move_sucess)
                    printBoard(self.board)

            # after the moves in this level is done, sort the moves based on the score and return the best score
            self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode: moveNode.score, reverse=self.isWhitesTurn())
            newScore, depth = self.bestMoveScoreAndDepth()
            return newScore

    def score_if_is_pawn(self, row, col):
        moveScore = 0
        if self.board[row][col]== 'p':
            moveScore = - (row*row)
        elif self.board[row][col]== 'P':
            moveScore = (7 - row)*(7 - row)

        return moveScore * self.pawn_move_score_factor


    def positionScore(self, row, col):
        squareValue = self.board[row][col]
        score = 0.0

        if isBlackPiece(squareValue):
            score -= self.pieceScoreMap[squareValue.upper()]
        else:
            score += self.pieceScoreMap[squareValue.upper()]

            # each attacked square also score
        score += self.attackScore * len(self.whiteMovements.attacks[row][col])
        score -= self.attackScore * len(self.blackMovements.attacks[row][col])



        return score

    def scoreKingMoves(self, kingValidMoves):
        score = 0.0
        for kingMove in kingValidMoves:
            for i in kingMove:
                if i >= 4: score += 8 - i
                else: score += i+1
        return score * self.kindMoveFactor;



    def isFinal(self):
        return True



class Movements:
    def __init__(self, attacks, kingPosition, isKingUnderAttack, kingValidMoves, pawnMoves, canCastleKingSide, canCastleQueenSide):
        self.attacks = attacks
        self.kingPosition = kingPosition
        self.isKingUnderAttack = isKingUnderAttack
        self.kingValidMoves = kingValidMoves
        self.pawnMoves = pawnMoves
        self.canCastleKingSide = canCastleKingSide
        self.canCastleQueenSide = canCastleQueenSide




