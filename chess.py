from printfunctions import printBoard
from printfunctions import printAttacks
from printfunctions import printPossibleMoves
from positions import INITIAL_POSITION
from printfunctions import printGame

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
    try:
        # first clean up the attacks
        whiteKingSquare= None;
        blackKingSquare = None;

        whitePawnMoves = []
        blackPawnMoves = []

        whiteAttackMoves = []
        blackAttackMoves = []

        whiteCaptures = []
        blackCaptures = []

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
                    attackRow = attackSquare[0]
                    attackCol = attackSquare[1]
                    attacked_piece = board[attackRow][attackCol]
                    if isWhitePiece(piece):
                        whiteAttackMoves[attackRow][attackCol].append(moveOrigin)
                        if isBlackPiece(attacked_piece):
                            whiteCaptures.append(Capture(piece,attacked_piece, r,c,attackRow,attackCol))
                    else:
                        blackAttackMoves[attackRow][attackCol].append(moveOrigin)
                        if isWhitePiece(attacked_piece):
                            blackCaptures.append(Capture(piece,attacked_piece, r,c,attackRow,attackCol))

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


        whiteMoves = Movements(whiteAttackMoves, whiteKingSquare, whiteKingIsUnderAttack, whiteKingValidMoves, whitePawnMoves, whiteCaptures, True, True)
        blackMoves = Movements(blackAttackMoves, blackKingSquare, blackKingIsUnderAttack, blackKingValidMoves, blackPawnMoves, blackCaptures, True, True)

        return (whiteMoves, blackMoves)
    except (RuntimeError, TypeError, NameError):
        print("Error calc moves for the board")
        printBoard(board)


def isWhitePiece(piece):
    return piece != ' ' and piece.isupper()



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


PIECE_SCORE_MAP = {
    " ": 0,
    "K": 0,
    "R": 5,
    "N": 3,
    "B": 3.1,
    "Q": 9,
    "P": 1
}

class MoveNode:
    def __init__(self, r1, c1, r2, c2, rank, score, piece, captured_piece, evaluation_completed=False, nodesEvaluated=1):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
        self.rank = rank
        self.score = score
        self.evaluation_completed = evaluation_completed
        self.piece = piece
        self.nodesEvaluated = nodesEvaluated
        self.captured_piece = captured_piece;



    def is_same(self, node):
        return self.c1== node.c1 and self.c2 == node.c2 and self.r1== node.r1 and self.r2 == node.r2;




    def __str__(self):
        prefix = "";
        if self.piece.upper() != 'P':
            prefix = self.piece
            if self.piece.upper() == 'N' or self.piece.upper() == 'R':
                prefix = prefix + str(chr(97+self.c1)) + str(8-self.r1)

        return prefix + str(chr(97+self.c2))+ str(8-self.r2) +"(" + str(round(self.rank,3)) +"/" + str(round(self.score,3)) +"/" + str(self.evaluation_completed) + "/" + str(self.nodesEvaluated) +")"

class SquarePositionValue:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return "(" + self.value+str(self.row) +"-"+str(self.col)+")"

class HistoryState:
    def __init__(self, square_pos_value_list, piece, captured_piece, r1, c1, r2, c2, white_movements, black_movements, possible_moves, castle_flags):
        self.piece = piece
        self.captured_piece = captured_piece
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
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
        self.attackScore = 0.01
        self.kindMoveFactor = 0.01
        self.pawn_move_score_factor = 0.003
        self.center_score_factor = 1.05
        self.wide_center_score_factor = 1.01
        self.check_store = 0.02
        self.capture_factor = 0.8

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
        # max time in seconds
        self.evaluation_max_time = 6
        self.evaluation_timed_out = False

        self.score_details = {}


    def state(self):
        stateStr = ""
        for row in self.board:
            stateStr += rowAsStr(row) + "-"
        stateStr += "1" if self.castle_flags["black_king_side"] else "0"
        stateStr += "1" if self.castle_flags["black_queen_side"] else "0"
        stateStr += "1" if self.castle_flags["white_king_side"] else "0"
        stateStr += "1" if self.castle_flags["white_queen_side"] else "0"
        #stateStr += "1" if self.isWhitesTurn() else "0"

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

    def can_castle_queen_side(self):
        return self.can_white_castle_queen_side() if self.isWhitesTurn() else self.can_black_castle_queen_side();


    def can_castle_king_side(self):
        return self.can_white_castle_king_side() if self.isWhitesTurn() else self.can_black_castle_king_side();


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
                        moveNode = self.createMoveNode(r1, c1, r2, c2)
                        possibleMoves.append(moveNode)
                        if not self.undo():
                            print("failed undo - 1 -" + str(len(self.movementHistory)))

        for pawnMove in pawnMoves:
            r1 = pawnMove[0]
            c1 = pawnMove[1]
            r2 = pawnMove[2]
            c2 = pawnMove[3]
            if self.tryMove(r1, c1, r2, c2):
                moveNode = self.createMoveNode(r1, c1, r2, c2)
                possibleMoves.append(moveNode)
                if not self.undo():
                    print("failed undo - 2 -" + str(len(self.movementHistory)))

        # generate castle moves
        r1 = r2= movements.kingPosition[0]
        c1 = movements.kingPosition[1]

        if self.can_castle_king_side():
            c2 = c1 + 2
            if self.tryMove(r1, c1, r2, c2, False):
                moveNode = self.createMoveNode(r1, c1, r2, c2)
                possibleMoves.append(moveNode)
                if not self.undo():
                    print("failed undo - castle k -" + str(len(self.movementHistory)))

        if self.can_castle_queen_side():
            c2 = c1 - 2
            if self.tryMove(r1, c1, r2, c2, False):
                moveNode = self.createMoveNode(r1, c1, r2, c2)
                possibleMoves.append(moveNode)
                if not self.undo():
                    print("failed undo - castle q-" + str(len(self.movementHistory)))


        return possibleMoves

    def createMoveNode(self, r1, c1, r2, c2):

        score = self.calculate_snapshot_core()
        rank = score
       #rank = self.calc_rank(score, r1, c1, r2, c2)
        lastMove = self.getLastMove()
        piece = lastMove.piece
        captured_piece = lastMove.captured_piece
        return MoveNode(r1, c1, r2, c2, rank, score, piece, captured_piece)

    def calc_rank(self, score, r1, c1, r2, c2):
        rank = score

        sign = -1 if self.isWhitesTurn() else 1;
        extra = 0.0

        self.whiteMovements

        if self.isCheck():
            extra += 9

        lastMove = self.getLastMove()
        if lastMove:
            piece = lastMove.piece
            captured_piece = lastMove.captured_piece

            attacks = self.blackMovements.attacks if isWhitePiece(piece) else self.whiteMovements.attacks
            if captured_piece != ' ':
                is_captured_defended = True if attacks[r2][c2] else False
                captured_score = self.capture_score(piece, captured_piece, is_captured_defended)
                # print("cap score[", piece, "_", r1, "-", c1, "]", captured_score)
                extra += 100 * captured_score
            else:
                # piece is under attack
                defenses = self.whiteMovements.attacks if isWhitePiece(piece) else self.blackMovements.attacks
                if len(attacks[r1][c1]) > 0:
                    is_piece_defended = True if defenses[r1][c1] else False
                    defense_score = self.defense_score(piece, attacks[r1][c1], is_piece_defended)
                    extra += 10 * defense_score

                if len(attacks[r2][c2]) > 0:
                    is_piece_defended = False
                    for p, r, c in defenses[r2][c2]:
                        if p != piece or c != c1 or r != r1:
                            is_piece_defended = True
                    defense_score = self.defense_score(piece, attacks[r2][c2], is_piece_defended)
                    extra -= 10 * defense_score

        if self.is_castle(piece, c1, c2):
            # print("iscastle score[", piece, "_", r1, "-", c1, "]", 10)
            extra += 5

        fork_score = self.fork_score(piece, r2, c2)
        # print("Fork score[", piece, "_", r1, "-", c1, "]", fork_score)
        extra += fork_score

        rank += sign * extra
        return rank


    def defense_score(self, piece, attacks, is_piece_defended):
        d_score = 0.0
        piece_value = PIECE_SCORE_MAP.get(piece.upper())
        if not is_piece_defended:
            return piece_value
        else:
            for attacker, r, c in attacks:
                attacker_value = PIECE_SCORE_MAP.get(attacker.upper())
                diff_value = piece_value - attacker_value
                d_score = max(d_score, diff_value)

        return d_score

    def fork_score(self, piece, r1, c1):
        if c1 != 0 and c1 != 7 and piece.upper() == 'P':
            c_p1 = c1 - 1
            c_p2 = c1 + 1

            r_p = r1 + 1 if self.isWhitesTurn() else r1 - 1
            p1 = self.board[r_p][c_p1]
            p2 = self.board[r_p][c_p2]
            if p1 == ' ' or p2 == ' ':
                return 0.0
            return 20.0 if (isSameColor(p1, p2) and not isSameColor(piece, p2) ) else 0.0
        else:
            return 0.0


    def is_castle(self, piece, c1, c2):
        return piece.upper() == 'K' and abs(c1 - c2) == 2

    def capture_score(self, piece, captured_piece, is_captured_defended):
        c_score = PIECE_SCORE_MAP.get(captured_piece.upper())
        if is_captured_defended:
            c_score -= PIECE_SCORE_MAP.get(piece.upper())
        return c_score

    def sortPossibleMoves(self):
        self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode: moveNode.score, reverse=self.isWhitesTurn())

    def rankPossibleMoves(self):
        self.possibleMoves = sorted(self.possibleMoves, key=lambda moveNode: moveNode.rank, reverse=self.isWhitesTurn())

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


    def is_castle_move(self, r1, c1, r2, c2):
        return self.board[r1][c1].upper() == 'K' and abs(c1-c2) == 2

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

        if self.is_castle_move(r1, c1, r2, c2):
            # move rook
            if c2 == 6:
                self.board[r1][5] = self.board[r1][7]
                self.board[r1][7] = ' '
                saved_positions += [SquarePositionValue(self.board[r1][5] , r1, 7), SquarePositionValue(' ', r1, 5)]
            if c2 == 2:
                self.board[r1][3] = self.board[r1][0]
                self.board[r1][0] = ' '
                saved_positions += [SquarePositionValue(self.board[r1][3] , r1, 0) , SquarePositionValue(' ', r1, 3)]

        historyState =  self.createHistoryState(saved_positions, squareValue1, squareValue2, r1, c1, r2, c2)
        #HistoryState(saved_positions, self.whiteMovements, self.blackMovements, self.possibleMoves, self.castle_flags.copy())

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
        if self.isKingUnderAttack(isWhitesTurn):
            if not self.undo():
                print("failed undo - under attack undo -" + str(len(self.movementHistory)))
            return False

        return True

    def createHistoryState(self, saved_positions, piece, captured_piece, r1, c1, r2, c2):
        return HistoryState(saved_positions, piece, captured_piece, r1, c1, r2, c2, self.whiteMovements, self.blackMovements, self.possibleMoves, self.castle_flags.copy())

    def getLastMove(self):
        if self.movementHistory:
            return self.movementHistory[-1]



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



    def calculate_snapshot_core(self):


        if self.is_draw_by_repetion():
             return 0.0
        #if self.is_draw():
        #   return 0.0
        #
       # if self.isCheckMate():
       #     return -self.MAX_SCORE if self.isWhitesTurn() else self.MAX_SCORE;


        position_score = 0.0
        pawn_advances_score = 0.0
        white_capture_score = 0.0
        black_capture_score = 0.0
        kind_moves = 0.0
        development = 0.0


        for r in range(0,8):
            for c in range(0,8):
                position_score += self.positionScore(r,c)
                if self.isFinal():
                    pawn_advances_score += self.score_if_is_pawn(r,c)

        if self.isWhitesTurn():
            for capture in self.whiteMovements.captures:
                white_capture_score = max(white_capture_score, self.score_capture(capture))

            if len(self.blackMovements.captures) > 1:
                good_attacks = 0
                for capture in self.blackMovements.captures:
                    if self.score_capture(capture) > 0:
                        good_attacks += 1
                if good_attacks > 1: black_capture_score = - 1.0*self.capture_factor
        else:
            for capture in self.blackMovements.captures:
                black_capture_score = min(black_capture_score, -self.score_capture(capture))

            if len(self.whiteMovements.captures) > 1:
                good_attacks = 0
                for capture in self.whiteMovements.captures:
                    if self.score_capture(capture) > 0:
                        good_attacks += 1
                if good_attacks > 1: white_capture_score = 1.0*self.capture_factor

        if self.isOpening():
            development = self.score_development()


        if self.isFinal():
            if self.isWhitesTurn():
                kind_moves += self.scoreKingMoves(self.whiteMovements.kingValidMoves)
            else:
                kind_moves -= self.scoreKingMoves(self.blackMovements.kingValidMoves)

        self.score_details = {
            "position": position_score,
            "pawn_advances": pawn_advances_score,
            "white_capture": white_capture_score,
            "black_capture": black_capture_score,
            "kind_moves": kind_moves,
            "development": development,
        }
        points = position_score
        points += pawn_advances_score
        points += white_capture_score
        points += black_capture_score
        points += kind_moves
        points += development

        return points


    def score_development(self):
        d_score = 0.0
        if self.board[0][1] == 'n': d_score += 1
        if self.board[0][2] == 'b': d_score += 1
        if self.board[0][5] == 'b': d_score += 1
        if self.board[0][6] == 'n': d_score += 1
        #if self.board[1][3] == 'p': d_score += 1
        if self.board[1][4] == 'p': d_score += 1
        if self.board[7][1] == 'N': d_score -= 1
        if self.board[7][2] == 'B': d_score -= 1
        if self.board[7][5] == 'B': d_score -= 1
        if self.board[7][6] == 'N': d_score -= 1
        #if self.board[7][3] == 'P': d_score -= 1
        if self.board[7][4] == 'P': d_score -= 1
        return 0.2*d_score



    def is_draw(self):
        return self.is_draw_by_repetion() or self.isStaleMate()

    def isCheckMate(self):
        return not self.possibleMoves and self.isCheck()

    def isCheck(self):
        return self.isKingUnderAttack(self.isWhitesTurn())

    def isStaleMate(self):
        return not self.possibleMoves and not self.isKingUnderAttack(self.isWhitesTurn())

    def is_draw_by_repetion(self):
        positionStr = self.state()
        return positionStr in self.previousPositions and self.previousPositions[positionStr] > 3

    def bestMoveScoreAndDepth(self):
        if self.possibleMoves:
            score = self.get_best_move_node().score
            return score, self.num_nodes_evaluated()
        else:
            if self.isCheckMate():
                sign = -1.0 if self.isWhitesTurn() else 1.0
                return self.MAX_SCORE * sign, 1

            if self.isStaleMate():
                return 0.0, 1

    def num_nodes_evaluated(self):
        return sum(node.nodesEvaluated for node in self.possibleMoves)


    def get_best_move_node(self):
        return max(self.possibleMoves, key=lambda moveNode: moveNode.score) if self.isWhitesTurn() else min(self.possibleMoves, key=lambda moveNode: moveNode.score)

    def doBestMove(self, maxMovesArray):
        self.do_timed_evaluated_move_score(maxMovesArray)
        print("total time: ", self.get_evaluation_time(), " secs")
        if self.possibleMoves:
            bestMoveNode = self.get_best_move_node()
            return self.move(bestMoveNode.r1, bestMoveNode.c1, bestMoveNode.r2, bestMoveNode.c2)
        return False

    def do_best_move(self, max_time):
        self.evaluate_until_time(max_time)
        print("GAME after evaluated:: ==========")
        printGame(self)
        if self.possibleMoves:
            self.sortPossibleMoves()
            eval_moves = [m for m in self.possibleMoves if m.evaluation_completed]
            if eval_moves:
                bestMoveNode = eval_moves[0]
            else:
                bestMoveNode = self.possibleMoves[0]
            return self.move(bestMoveNode.r1, bestMoveNode.c1, bestMoveNode.r2, bestMoveNode.c2)
        return False


    def get_evaluation_time(self):
        if self.evaluation_end_time > self.evaluation_start_time:
            return self.evaluation_end_time - self.evaluation_start_time
        else:
            return self.get_current_evaluation_time()

    def get_current_evaluation_time(self):
        return time.time() - self.evaluation_start_time;

    def do_timed_evaluated_move_score(self, searchParams):
        self.evaluation_start_time = time.time()
        self.evaluate_move_score(searchParams, False)
        self.evaluation_end_time = time.time()

    # main function - entry point here
    def evaluate_until_time(self, maxTime):
        self.evaluation_start_time = time.time()
        self.evaluation_max_time = maxTime

        self.rankPossibleMoves()
        pruningDelta = 1.0;

        depth = 4
        MAX_DEPTH = 4
        while not self.evaluation_max_time_reached():
            searchParams = []
            for d in range(0, min(depth, MAX_DEPTH)):
                delta = max(0.0, pruningDelta - d*0.5)
                searchParams.append((1000, delta))

            print("evaluating depth: ", len(searchParams), ", pruningDelta: ", pruningDelta, " all params: ", searchParams)
            self.evaluate_move_score(searchParams, True)
            depth += 1
            if depth >= MAX_DEPTH:
                pruningDelta += 0.1


            print("evaluating time: ", self.get_evaluation_time())
            if self.evaluation_max_time_reached():
                print("timeout")
                break
            else:
                self.rankPossibleMoves()
                print("there is still time left, continuing evaluation. Best moves so far:")
                printPossibleMoves(self)


        self.evaluation_end_time = time.time()
        print("eval depth: " + str(len(searchParams)))



    def evaluation_max_time_reached(self):
        return self.get_current_evaluation_time() >= self.evaluation_max_time;


    def evaluate_move_score(self, searchParams, stop_after_max_time=False):
        self.evaluateMoveScore(searchParams, 0, stop_after_max_time)


    # for each possible move, update the score value by making a tree search
    # this method will execute moves and undo to update the scores
    def evaluateMoveScore(self, searchParams, depth, stop_after_max_time=False):
        self.evaluation_timed_out = stop_after_max_time and self.evaluation_max_time_reached()
        if depth >= len(searchParams):
            return self.bestMoveScoreAndDepth()
        else:
            # it will perform a tree search just on the first moves
            maxMoves, pruningDelta = searchParams[depth]
            movementsToCheck = min(maxMoves, len(self.possibleMoves))

            isWhiteTurn = self.isWhitesTurn()

            self.rankPossibleMoves()


            #print("checking nMoves:" + str(movementsToCheck) + ", depth="+ str(depth) + "/"+str(len(searchParams)) +" on board:")
            #printBoard(self.board)

            pruningScore = self.MAX_SCORE*-1 if isWhiteTurn else self.MAX_SCORE
            for moveNumber in range(0, movementsToCheck):
                if (stop_after_max_time and self.evaluation_max_time_reached()):
                    self.evaluation_timed_out = True
                    break
                self.evaluation_timed_out = False
                moveNode = self.possibleMoves[moveNumber]
               # spaces = "-" * depth
               # print(spaces + "checking move(" + str(moveNumber) + "):" + str(moveNode) , self.isWhitesTurn(), " depth " ,depth, ", pruningScore ", pruningScore, ", delta ", pruningDelta, " isWhite:", isWhiteTurn )
                # do alpha/beta pruning


                # if the next move is not better than pruningDelta _
                if isWhiteTurn:
                    if moveNode.score+pruningDelta < pruningScore:
                        break
                else:
                    if moveNode.score-pruningDelta > pruningScore:
                        break


                # this need to change to move without validation
                #move_sucess = self.move(moveNode.r1, moveNode.c1, moveNode.r2, moveNode.c2)
                move_sucess = self.doValidatedMove(moveNode)

                # update the move score
                score, nodesEvaluated = self.evaluateMoveScore(searchParams, depth + 1)
                moveNode.score = score
                moveNode.nodesEvaluated += nodesEvaluated
                moveNode.evaluation_completed = not self.evaluation_timed_out
                pruningScore = max(score, pruningScore) if isWhiteTurn else min(score, pruningScore)


                if not self.undo():
                    print("failed to undo z", str(moveNode) , " --> " ,move_sucess)
                    printBoard(self.board)


            return self.bestMoveScoreAndDepth()


    def score_if_is_pawn(self, row, col):
        moveScore = 0
        if self.board[row][col]== 'p':
            moveScore = - (row*row)
        elif self.board[row][col]== 'P':
            moveScore = (7 - row)*(7 - row)

        return moveScore * self.pawn_move_score_factor

    def score_capture(self, capture):
        if capture.captured_piece.upper() == 'K':
            return self.check_store
        captor_score = self.pieceScoreMap[capture.captor_piece.upper()]
        captured_score = self.pieceScoreMap[capture.captured_piece.upper()]

        attacks = self.blackMovements.attacks if isWhitePiece(capture.captor_piece) else self.whiteMovements.attacks

        is_captured_defended = True if attacks[capture.r2][capture.c2] else False

        s = (captured_score - captor_score) if is_captured_defended else captured_score
        return self.capture_factor * s


    def positionScore(self, row, col):
        squareValue = self.board[row][col]
        score = 0.0

        if isBlackPiece(squareValue):
            score -= self.pieceScoreMap[squareValue.upper()]
        else:
            score += self.pieceScoreMap[squareValue.upper()]

            # each attacked square also score
        center_factor = self.calc_center_score_factor(row, col)
        score += self.attackScore * len(self.whiteMovements.attacks[row][col])
        score -= self.attackScore * len(self.blackMovements.attacks[row][col])

        return score * center_factor

    def calc_center_score_factor(self, row, col):
        if row > 0+2 and row < 8-2 and col > 0+2 and col < 8-2:
            return self.center_score_factor
        elif row > 0+1 and row < 8-1 and col > 0+1 and col < 8-1:
            return self.wide_center_score_factor
        else:
            return 1.0



    def scoreKingMoves(self, kingValidMoves):
        score = 0.0
        for kingMove in kingValidMoves:
            for i in kingMove:
                if i >= 4: score += 8 - i
                else: score += i+1
        return score * self.kindMoveFactor;

    def isOpening(self):
        return self.number_of_moves() < 10

    def isFinal(self):
        return self.number_of_moves() > 40

    def number_of_moves(self):
        return len(self.movementHistory)

class Capture:
    def __init__(self, captor_piece, captured_piece, r1, c1, r2, c2):
        self.captor_piece = captor_piece
        self.captured_piece = captured_piece
        self.r1 = r1
        self.c1 = c1
        self.c2 = c2
        self.r2 = r2




class Movements:
    def __init__(self, attacks, kingPosition, isKingUnderAttack, kingValidMoves, pawnMoves, captures, canCastleKingSide, canCastleQueenSide):
        self.attacks = attacks
        self.kingPosition = kingPosition
        self.isKingUnderAttack = isKingUnderAttack
        self.kingValidMoves = kingValidMoves
        self.pawnMoves = pawnMoves
        self.captures = captures
        self.canCastleKingSide = canCastleKingSide
        self.canCastleQueenSide = canCastleQueenSide




