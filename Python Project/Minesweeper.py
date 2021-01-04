# 0 - square uncovered
# -1 - square covered
# (1-8) adjacent bombs
# -2 flagged

import random
import tkinter as tk
import time
from tkinter import *
import threading

images = []
size = 10
nrOfBombs = 25
board = [[0 for x in range(size)] for y in range(size)]
playerBoard = [[-1 for x in range(size)] for y in range(size)]
game = False
root = tk.Tk()
frames = []
timer = 30
game_nr = 0
first_square = False


def on_closing():
    global game
    global root
    game = False
    root.destroy()


def thread_function(t, nr):
    global game
    global root
    global size
    global game_nr

    local_nr = nr
    time_label = tk.Label(root)
    time_label.place(x=size * 25 / 2 - 35 / 2, y=100, width=35, height=25)
    while t and game_nr == local_nr and game:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        try:
            time_label.config(text=timer)
        except:
            continue
        time.sleep(1)
        t -= 1
    if game_nr == local_nr:
        game = False
        if t == 0:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            try:
                time_label.config(text=timer)
            except:
                pass
            time.sleep(1)
            t -= 1
            timer = '{:02d}:{:02d}'.format(mins, secs)
            try:
                time_label.config(text=timer)
            except:
                pass
            popup('You lost on time!')


def initBoard(x, y):
    x = x // 25
    y = y // 25
    global board
    global playerBoard
    global size
    global nrOfBombs

    if nrOfBombs >= size * size:
        nrOfBombs = size * size - 1

    board = [[0 for x in range(size)] for y in range(size)]
    playerBoard = [[-1 for x in range(size)] for y in range(size)]
    nrOfSquares = size * size
    placedBombs = 0
    chanceToPlaceBomb = nrOfBombs / nrOfSquares
    ok = True
    for i in range(size):
        if ok:
            for j in range(size):
                if ok:
                    if board[i][j] == 0 and (i != x or j != y):
                        randNum = random.random()
                        if randNum < chanceToPlaceBomb:
                            board[i][j] = -1
                            placedBombs += 1
                            if placedBombs == nrOfBombs:
                                ok = False
                else:
                    break
        else:
            break
    while placedBombs != nrOfBombs:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if board[row][col] == 0 and (row != x or col != y):
            board[row][col] = -1
            placedBombs += 1


def initGUI():
    global root
    global frames
    center_frame = tk.Frame(root, width=25 * size, height=25 * size)
    upper_frame = tk.Frame(root, width=25 * size, height=150, bg='grey65')

    mine_str = StringVar()
    mine_str.trace(
        "w", lambda name, index, mode, mine_str=mine_str: callback2(mine_str))

    mine_label = tk.Label(upper_frame, text="Mines")
    mine_entry = tk.Entry(upper_frame, textvariable=mine_str)
    mine_label.place(x=(size * 25) / 2 - 35 / 2 - 90,
                     y=60,
                     width=35,
                     height=25)
    mine_entry.place(x=(size * 25) / 2 - 35 / 2 - 40,
                     y=60,
                     width=35,
                     height=25)

    size_str = StringVar()
    size_str.trace(
        "w", lambda name, index, mode, size_str=size_str: callback1(size_str))

    size_label = tk.Label(upper_frame, text="Size")
    size_entry = tk.Entry(upper_frame, textvariable=size_str)
    size_label.place(x=(size * 25) / 2 - 35 / 2 + 40,
                     y=60,
                     width=35,
                     height=25)
    size_entry.place(x=(size * 25) / 2 - 35 / 2 + 90,
                     y=60,
                     width=35,
                     height=25)

    time_str = StringVar()
    time_str.trace(
        "w", lambda name, index, mode, time_str=time_str: callback3(time_str))

    time_label = tk.Label(upper_frame, text="Time")
    time_entry = tk.Entry(upper_frame, textvariable=time_str)
    time_label.place(x=(size * 25) / 2 - 35 / 2 - 90,
                     y=100,
                     width=35,
                     height=25)
    time_entry.place(x=(size * 25) / 2 - 35 / 2 - 40,
                     y=100,
                     width=35,
                     height=25)

    start_btn = tk.Button(upper_frame, command=initGame, text="New Game")
    start_btn.place(x=(25 * size) / 2 - 35, y=10, width=70, height=25)

    upper_frame.pack(side="top")
    center_frame.pack(side="bottom")
    for i in range(size):
        line_frames = []
        for j in range(size):
            frame = tk.Frame(center_frame,
                             width=25,
                             height=25,
                             bg='grey30',
                             relief='raised',
                             bd=1)
            frame.grid(row=i, column=j)
            line_frames.append(frame)
        frames.append(line_frames)


def loadImages():
    images.append(PhotoImage(file='1.png'))
    images.append(PhotoImage(file='2.png'))
    images.append(PhotoImage(file='3.png'))
    images.append(PhotoImage(file='4.png'))
    images.append(PhotoImage(file='5.png'))
    images.append(PhotoImage(file='6.png'))
    images.append(PhotoImage(file='7.png'))
    images.append(PhotoImage(file='8.png'))
    images.append(PhotoImage(file='bomb.png'))
    images.append(PhotoImage(file='flag.png'))


def initGame():
    global game
    global board
    global playerBoard
    global frames
    global size
    global root
    global nrOfBombs
    global game_nr
    global first_square

    first_square = True
    game_nr += 1
    game = False
    frames.clear()
    for child in root.winfo_children():
        child.destroy()
    initGUI()
    game = True
    if timer != 0:
        x = threading.Thread(target=thread_function, args=(timer, game_nr))
        x.start()


def leftClick(event):
    global game
    global first_square

    if game:
        y = root.winfo_pointerx() - root.winfo_rootx()
        x = root.winfo_pointery() - root.winfo_rooty() - 150
        if first_square and x > 0 and y > 0:
            initBoard(x, y)
            first_square = False
        if x > 0 and y > 0 and playerBoard[x // 25][y // 25] != -2:
            y = y // 25
            x = x // 25
            if board[x][y] == 0:
                event.widget.configure(bg='grey70')
                adjBombs = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (i != 0 or
                                j != 0) and (x + i >= 0 and x + i < size) and (
                                    y + j >= 0) and (y + j < size):
                            if board[x + i][y + j] == -1:
                                adjBombs += 1

                if adjBombs != 0:
                    playerBoard[x][y] = adjBombs
                    canvas = tk.Canvas(width=23,
                                       height=23,
                                       master=event.widget,
                                       bd=0,
                                       highlightthickness=0)
                    canvas.create_image(0,
                                        0,
                                        image=images[adjBombs - 1],
                                        anchor=NW)
                    canvas.pack(expand=YES, fill=BOTH)
                else:
                    playerBoard[x][y] = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (i != 0 or j != 0) and (x + i >= 0) and (
                                    x + i < size) and (y + j >= 0) and (y + j <
                                                                        size):
                                if playerBoard[x + i][y + j] == -1:
                                    uncoverBoard(x + i, y + j)
                ok = True
                for i in range(0, size):
                    for j in range(0, size):
                        if board[i][j] == 0 and playerBoard[i][j] < 0:
                            ok = False
                if ok:
                    game = False
                    popup('You won!')
            else:
                canvas = tk.Canvas(width=23,
                                   height=23,
                                   master=event.widget,
                                   bd=0,
                                   highlightthickness=0)
                canvas.create_image(0, 0, image=images[-2], anchor=NW)
                canvas.pack(expand=YES, fill=BOTH)
                showBombs(x, y)
                game = False
                popup('You lost!')


def popup(msg):
    global root
    popup = tk.Tk()
    popup.geometry('%dx%d+%d+%d' %
                   (100, 100, root.winfo_pointerx(), root.winfo_pointery()))
    popup.wm_title("Game Over")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def showBombs(x, y):
    for i in range(0, size):
        for j in range(0, size):
            if board[i][j] == -1 and (x != i or y != j):
                if playerBoard[i][j] == -2:
                    for canvas in frames[i][j].winfo_children():
                        canvas.destroy()
                canvas = tk.Canvas(width=23,
                                   height=23,
                                   master=frames[i][j],
                                   bd=0,
                                   highlightthickness=0)
                canvas.create_image(0, 0, image=images[-2], anchor=NW)
                canvas.pack(expand=YES, fill=BOTH)


def uncoverBoard(x, y):
    adjBombs = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                    i != 0 or j != 0
            ) and x + i >= 0 and x + i < size and y + j >= 0 and y + j < size:
                if board[x + i][y + j] == -1:
                    adjBombs += 1
    if adjBombs != 0:
        playerBoard[x][y] = adjBombs
        canvas = tk.Canvas(width=23,
                           height=23,
                           master=frames[x][y],
                           bd=0,
                           highlightthickness=0)
        canvas.create_image(0, 0, image=images[adjBombs - 1], anchor=NW)
        canvas.pack(expand=YES, fill=BOTH)
    else:
        frames[x][y].configure(bg='grey70')
        playerBoard[x][y] = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (x + i >= 0) and (x + i < size) and (
                        y + j >= 0) and (y + j < size):
                    if playerBoard[x + i][y + j] == -1:
                        uncoverBoard(x + i, y + j)


def rightClick(event):
    global game
    global first_square
    if game and not first_square:
        y = root.winfo_pointerx() - root.winfo_rootx()
        x = root.winfo_pointery() - root.winfo_rooty() - 150
        if x > 0 and y > 0:
            y = y // 25
            x = x // 25
            if playerBoard[x][y] == -1:
                canvas = tk.Canvas(width=23,
                                   height=23,
                                   master=event.widget,
                                   bd=0,
                                   highlightthickness=0)
                canvas.create_image(0, 0, image=images[-1], anchor=NW)
                canvas.pack(expand=YES, fill=BOTH)
                playerBoard[x][y] = -2
            elif playerBoard[x][y] == -2:
                playerBoard[x][y] = -1
                for canvas in frames[x][y].winfo_children():
                    canvas.destroy()


def callback1(size_str):
    global size
    if len(size_str.get()) > 1:
        size = int(size_str.get())


def callback2(mine_str):
    global nrOfBombs
    if len(mine_str.get()) > 0:
        nrOfBombs = int(mine_str.get())


def callback3(time_str):
    global timer
    if len(time_str.get()) > 0:
        timer = int(time_str.get())


root.protocol("WM_DELETE_WINDOW", on_closing)
root.wm_title("Minesweeper")
root.bind('<Button-1>', leftClick)
root.bind('<Button-3>', rightClick)
loadImages()
initGUI()
root.mainloop()
