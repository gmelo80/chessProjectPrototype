from printfunctions import printBoard
from printfunctions import printAttacks
from printfunctions import printPossibleMoves
from positions import INITIAL_POSITION


def pawnAttackSquares(is_white, row, col):
    attackSquares = []
    increment = -1 if is_white else 1;
    if col-1 >=0: attackSquares.append((row+increment,col-1))
    if col+1 <8: attackSquares.append((row+increment,col+1))
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


def calculateMovements(board):
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
            elif piece == 'p'and board[r+1][c] == ' ':
                blackPawnMoves.append((r,c,r-1,c))
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


    whiteMoves = Movements(whiteAttackMoves, whiteKingSquare, whiteKingIsUnderAttack, whiteKingValidMoves, whitePawnMoves)
    blackMoves = Movements(blackAttackMoves, blackKingSquare, blackKingIsUnderAttack, blackKingValidMoves, blackPawnMoves)

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




class Game:

    def __init__(self, board, whiteStarts):
        self.MAX_SCORE = 1000000
        self.attackScore = 0.0
        self.kindMoveFactor = 0.01
        self.pieceScoreMap = {
            " ": 0,
            "K": 0,
            "R": 5,
            "N": 3,
            "B": 3.1,
            "Q": 9,
            "P": 1
        }
        self.board = board
        self.whiteStarts = whiteStarts
        self.movementHistory = []
        self.previousPositions = {}
        self.whiteMovements = []
        self.blackMovements = []
        self.possibleMoves = []
        self.calculateMoves()


    def state(self):
        stateStr = ""
        for row in self.board:
            stateStr += rowAsStr(row) + "-"
        return stateStr


    def calculateMoves(self):
        (self.whiteMovements, self.blackMovements) = calculateMovements(self.board)
        self.possibleMoves = self.generatePossibleMoves()


    def generatePossibleMoves(self):
        if self.isWhitesTurn():
            attackMoves = self.whiteMovements.attacks
        else:
            attackMoves = self.blackMovements.attacks

        possibleMoves = []
        for r2 in range(0, 8):
            for c2 in range(0, 8):
                for attack in attackMoves[r2][c2]:
                    r1 = attack[1]
                    c1 = attack[2]
                    if self.tryMove(r1, c1, r2, c2):
                        moveNode = MoveNode(r1, c1, r2, c2, self.score())
                        possibleMoves.append(moveNode)
                        self.undo()

        return sorted(possibleMoves, key=lambda moveNode : moveNode.calculate_snapshot_core, reverse=self.isWhitesTurn())



    def move(self, r1, c1, r2, c2):
        if not self.passBasicValidation(r1, c1, r2, c2):
            return False;

        if not self.tryMove(r1, c1, r2, c2):
            print("invalid move king is in a attacked square")
            return False
        else:
            self.calculateMoves()
            return True;


    def tryMove(self, r1, c1, r2, c2):

        squareValue1 = self.board[r1][c1]
        squareValue2 = self.board[r2][c2]

        if isSameColor(squareValue1, squareValue2):
            return False

        if squareValue1.upper() == 'P':
            if squareValue2 == ' ' and c1 != c2:
                return False

        isWhitesTurn = self.isWhitesTurn()
        move = (r1, c1, squareValue1, r2, c2, squareValue2, self.whiteMovements, self.blackMovements, self.possibleMoves)
        self.board[r1][c1] = ' '
        self.board[r2][c2] = squareValue1
        self.movementHistory.append(move)

        positionStr = self.state()
        if positionStr in self.previousPositions:
            self.previousPositions[positionStr] = self.previousPositions[positionStr] + 1
        else:
            self.previousPositions[positionStr] = 1



        (self.whiteMovements, self.blackMovements) = calculateMovements(self.board)
        #print("trying [" + str(r1) +"," + str(c1) +"->" + str(r2) +"," + str(c2) +"]" )
        if self.isKingUnderAttack(isWhitesTurn):
           # print("king - under attack undo")
            self.undo()
            return False

        return True

    def lastMoveStr(self):
        if self.movementHistory:
            r1, c1, squareValue1, r2, c2, squareValue2, whiteMovements, blackMovements, possibleMoves = self.movementHistory[-1]
            return str((r1, c1)) + " -> " + str((r2, c2))
        else:
            return "none"



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
            if squareValue2 == ' ' and c1 != c2:
                return False


        if self.isWhitesTurn():
            if not self.whiteMovements.attacks[r2][c2]:
                print("invalid move for white, valid moves for " + squareValue1 + " are:")
                printAttacks(self.whiteMovements.attacks, squareValue1)
                return False
        else:
            if not self.blackMovements.attacks[r2][c2]:
                print("invalid move for black, valid moves for " + squareValue1 + " are:")
                printAttacks(self.blackMovements.attacks, squareValue1)
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
            lastPieceMoved = self.movementHistory[-1][2]
            return isBlackPiece(lastPieceMoved)

    def undo(self):
        if len(self.movementHistory) > 0:
            move = self.movementHistory.pop()
            (r1, c1, val1, r2, c2, val2, self.whiteMovements, self.blackMovements, self.possibleMoves) = move
            positionStr = self.state()
            self.board[r1][c1] = val1
            self.board[r2][c2] = val2

            self.previousPositions[positionStr] = self.previousPositions[positionStr] - 1
            if self.previousPositions[positionStr] == 0:
                self.previousPositions.pop(positionStr)

            return True
        else:
            print("no moves to undo")
            return False

    def score(self):

        points = 0.0
        for r in range(0,8):
            for c in range(0,8):
                points += self.positionScore(r,c)

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


    def bestMoveScoreAndDepth(self):
        if self.possibleMoves:
            return self.possibleMoves[0].calculate_snapshot_core, self.possibleMoves[0].nodesEvaluated
        else:
            if self.isCheckMate():
                sign = -1.0 if self.isWhitesTurn() else 1.0
                return self.MAX_SCORE * sign, self.MAX_SCORE

            if self.isStaleMate():
                return 0.0, self.MAX_SCORE


    def evaluateBestNode(self):
        moveNode = self.possibleMoves[0]
        self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2)

        newScore, depth = self.bestMoveScoreAndDepth()
        self.undo()
        moveNode.calculate_snapshot_core = newScore
        moveNode.nodesEvaluated = moveNode.nodesEvaluated + 1
        self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode : moveNode.calculate_snapshot_core, reverse=self.isWhitesTurn())

    def doBestMove(self, maxMoves, depth):
        self.evaluateMoveScore(maxMoves, depth)
        bestMoveNode = self.possibleMoves[0]
        self.move(bestMoveNode.r1, bestMoveNode.c1, bestMoveNode.r2, bestMoveNode.c2)

    def evaluateMoveScore(self, maxMoves, depth):
        if depth == 0:
            newScore, depth = self.bestMoveScoreAndDepth()
            return newScore
        else:
            #print(" before eval " + str(depth))
            #printPossibleMoves(self)
            movementsToCheck = min(maxMoves, len(self.possibleMoves))
            for moveNumber in range(0, movementsToCheck):
                moveNode = self.possibleMoves[moveNumber]
                self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2)

                newMaxMoves = max(1, maxMoves/4)
                moveNode.calculate_snapshot_core = self.evaluateMoveScore(maxMoves, depth - 1)
                moveNode.nodesEvaluated = depth
                self.undo()

            #print(" after eval " + str(depth))
            #printPossibleMoves(self)
            self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode: moveNode.calculate_snapshot_core, reverse=self.isWhitesTurn())
            newScore, depth = self.bestMoveScoreAndDepth()
            return newScore



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
    def __init__(self, attacks, kingPosition, isKingUnderAttack, kingValidMoves, pawnMoves):
        self.attacks = attacks
        self.kingPosition = kingPosition
        self.isKingUnderAttack = isKingUnderAttack
        self.kingValidMoves = kingValidMoves
        self.pawnMoves = pawnMoves




