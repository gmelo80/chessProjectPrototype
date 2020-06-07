from chess import Game
from positions import  *
from printfunctions import *
import tkinter as tk



from tkinter import *
import time


Board= [
    [' ', ' ', ' ', ' ', 'k', ' ', ' ', ' '],
    [' ', ' ', ' ', 'p', ' ', 'p', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'K', ' ', ' ', ' ']];

Board = INITIAL_POSITION
# Board = KING_AND_PAWS_POSITION
game = Game(Board, True)

originClick=None
destClick=None
ComputerIsMoving=False
IsGameEnd=False

canvas_width = 500
square_width = canvas_width / 8

root = tk.Tk()
images = []

canvas = Canvas(root,
                width=square_width * 8,
                height=(200 + square_width * 8))

def undoLastMove():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    game.undo()
    game.undo()
    drawGame(canvas, game, square_width, images)

def play():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    canvas.after(20)
    canvas.update()
    canvas.after(50, doComputerMove)


def calcScore():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    print(" board score: " + str(round(game.calculate_snapshot_core(), 3)))
    print(" score details: " + str(game.score_details))


def autoPlay():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    while not IsGameEnd:
        canvas.after(20)
        canvas.update()
        canvas.after(50, doComputerMove)


def tryComputerMove():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    if not game.isWhitesTurn() and int(evalTimeBtn.get()) > 0:
        doComputerMove()


def doComputerMove():
    global originClick, destClick, game, square_width, images, root, ComputerIsMoving
    ComputerIsMoving = True
    destClick = None
    originClick = None
    #game.doBestMove(30, 6)
    timeEval = evalTimeBtn.get()
    print("evaluating for " + str(timeEval) + " seconds")
    game.do_best_move(int(timeEval))
    drawGame(canvas, game, square_width, images)
    printGame(game)
    ComputerIsMoving = False


def callback(event):
    global originClick, destClick, game, square_width, images, root
    row = int(event.y // square_width)
    col = int(event.x // square_width)
    #print ("clicked at x y:", event.x, event.y)
    #print ("clicked at r c:", row, col)
    if row >=0 and row < 8 and col >=0 and col < 8:
        squarePos = (row, col)
        if originClick == None:
            originClick = squarePos
        elif originClick == squarePos:
            destClick = None
        elif destClick == None:
            destClick = squarePos
        elif destClick == squarePos:
            destClick = None
        else:
            destClick = None
            originClick = None
    else:
        destClick = None
        originClick = None
    print(str(originClick) + " --- " +str(destClick))
    drawGame(canvas, game, square_width, images)

    if destClick != None and originClick != None:
        if game.moveIfPossible(originClick[0],originClick[1],destClick[0], destClick[1]):
            originClick = destClick
            destClick = None
            printGame(game)
        else:
            destClick = None
            originClick = None
        drawGame(canvas, game, square_width, images)


        canvas.after(20)
        canvas.update()
        canvas.after(50, tryComputerMove)





def drawGame(canvas, game, square_width, images):
    images.clear()
    index = 0
    global originClick, destClick,IsGameEnd

    for row in range(0, 8):
        for col in range(0, 8):
            color = "yellow" if (row + col) % 2 == 0 else "blue"
            x1 = col * square_width
            y1 = row * square_width
            x2 = x1 + square_width
            y2 = y1 + square_width

            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            if originClick != None and originClick[0] == row and originClick[1] == col:
                canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=5)

            squareVal = game.board[row][col]
            #print("" + squareVal + " on " + str(row) + "," + str(col))
            if squareVal != " ":
                #print("draw " + squareVal + " on " + str(row) + "," + str(col))
                images.append(createImageForPiece(squareVal))
                canvas.create_image(x1, y1, anchor=NW, image=images[-1])
    if game.isCheckMate():
        canvas.create_text(250, 520, fill="red", font="Times 40 italic bold", text="CHECKMATE!")
        IsGameEnd=True
    if game.isStaleMate():
        canvas.create_text(250, 520, fill="blue", font="Times 40 italic bold", text="STALEMATE!")
        IsGameEnd = True

    if game.is_draw_by_repetion():
            canvas.create_text(250, 520, fill="blue", font="Times 40 italic bold", text="DRAW!")
            IsGameEnd = True


def createImageForPiece(piece):
    prefix = "w_" if piece.isupper() else "b_"
    path = "images/"+prefix+piece.lower()+".png"
    return PhotoImage(file=path)





canvas.bind("<Button-1>", callback)
canvas.pack()
drawGame(canvas, game, square_width, images)

frame = tk.Frame(root)
frame.pack()
undoBtn = tk.Button(frame,
                   text="UNDO LAST MOVE",
                   fg="black",
                   bg="blue",
                   bd=10,
                   command=undoLastMove)
undoBtn.pack(side=tk.LEFT)

autoPlayBtn = tk.Button(frame,
                   text="Auto Play",
                   fg="black",
                   bg="blue",
                   bd=10,
                   command=autoPlay)
autoPlayBtn.pack(side=tk.LEFT)

autoPlayBtn = tk.Button(frame,
                   text="Play Move",
                   fg="black",
                   bg="blue",
                   bd=10,
                   command=play)
autoPlayBtn.pack(side=tk.LEFT)

var = StringVar(root)
var.set("5")
evalTimeBtn = Spinbox(frame, from_=0, to=10, textvariable=var)

evalTimeBtn.pack()

calcScoreBtn = tk.Button(frame,
                   text="Calc score",
                   fg="black",
                   bg="blue",
                   bd=10,
                   command=calcScore)
calcScoreBtn.pack(side=tk.LEFT)

root.mainloop()