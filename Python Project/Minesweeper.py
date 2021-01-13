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
size1 = 10
size2 = 10
nrOfBombs = 25
board = [[0 for x in range(size2)] for y in range(size1)]
playerBoard = [[-1 for x in range(size2)] for y in range(size1)]
game = False
root = tk.Tk()
frames = []
timer = 30
game_nr = 0
first_square = False


def on_closing():
    """
    A function that is called when pressing the close button.
    It sets a boolean variable on False so that every open thread closes.
    """
    global game
    global root
    game = False
    root.destroy()


def thread_function(t, nr):
    """
    This function is a thread function.
    If the user sets a timer value other than 0, a new thread will open,
    and using this function it will keep track of the time passed since
    the start of the game. If the time runs out before the user
    wins/loses the game, a pop-up will show up,
    informing the user that he lost and a boolean variable will
    be set to False so that the user will no longer
    be able to click on the board,
    and will have to start a new game.
    If the user starts a new game before the current one finishes
    and therefore this thread is no longer needed, a global value
    will be incremented and when this function will check that
    this variable has been changed, comparing it to a local variable
    that wasn't changed globally,
    the function whill break out of the loop and finish.
    Args:
        t (int): The timer value in seconds.
        nr (int): The number of the game the user has started.
    """
    global game
    global root
    global size1
    global size2
    global game_nr

    local_nr = nr
    time_label = tk.Label(root)
    time_label.place(x=size2 * 25 / 2 - 35 / 2, y=100, width=35, height=25)
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
    """
    This function initialises the player board, and the game board.
    The game board is a matrix of 0's and -1's, -1 meaning a bomb
    and 0 not a bomb. The player board is a matrix of what the player
    currently sees on the board, which squares are covered, which
    squares have been uncovered(clicked), squares that have been
    flagged as bombs and squares that show the number of bombs
    next to them(a number from 1 to 8).

    The function also places the bombs on the board in a randomly manner.
    Firstly, it calculates the chance for a bomb to be placed on a square.
    That chance will be equal to nrOfBombs / nrOfSquares.
    Afterwards, it iterates through the board,
    and generates a random number between 0 and 1 for each square.
    If the generated number is smaller than the chance to place,
    a bomb will be placed on that square.
    The loop will stop if all the bombs have been placed before the
    iteration through the board ends. If by the end of the iteration,
    there still remain bombs to be placed, random squares will be chosen
    and the bombs will be placed on them, until all bombs have been placed.

    The function takes x, y as parameters,
    which are indexes of the first square the user has pressed on.
    The function needs these so that it doesn't place a bomb on that square.
    Args:
        x (int): The X coordinate of the mouse when clicked.
        y (int): The Y coordinate of the mouse when clicked.
    """
    x = x // 25
    y = y // 25
    global board
    global playerBoard
    global size1
    global size2
    global nrOfBombs

    if nrOfBombs >= size1 * size2:
        nrOfBombs = size1 * size2 - 1

    board = [[0 for x in range(size2)] for y in range(size1)]
    playerBoard = [[-1 for x in range(size2)] for y in range(size1)]
    nrOfSquares = size1 * size2
    placedBombs = 0
    chanceToPlaceBomb = nrOfBombs / nrOfSquares
    ok = True
    for i in range(size1):
        if ok:
            for j in range(size2):
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
        row = random.randint(0, size1 - 1)
        col = random.randint(0, size2 - 1)
        if board[row][col] == 0 and (row != x or col != y):
            board[row][col] = -1
            placedBombs += 1


def initGUI():
    """
    This function sets up all the GUI elements the user will need.
    These include the board and the entry fields for the sizes,
    the time and the number of bombs.
    """
    global root
    global frames
    global size2
    center_frame = tk.Frame(root, width=25 * size2, height=25 * size2)
    upper_frame = tk.Frame(root, width=25 * size2, height=150, bg='grey65')

    mine_str = StringVar()
    mine_str.trace(
        "w", lambda name, index, mode, mine_str=mine_str: callback2(mine_str))

    mine_label = tk.Label(upper_frame, text="Mines")
    mine_entry = tk.Entry(upper_frame, textvariable=mine_str)
    mine_label.place(x=(size2 * 25) / 2 - 35 / 2 - 90,
                     y=60,
                     width=35,
                     height=25)
    mine_entry.place(x=(size2 * 25) / 2 - 35 / 2 - 40,
                     y=60,
                     width=35,
                     height=25)

    size1_str = StringVar()
    size1_str.trace(
        "w", lambda name, index,
        mode, size_str=size1_str: callback11(size1_str))

    size_label = tk.Label(upper_frame, text="Size")
    size1_entry = tk.Entry(upper_frame, textvariable=size1_str)
    size_label.place(x=(size2 * 25) / 2 - 100 / 2 + 40,
                     y=60,
                     width=35,
                     height=25)
    size1_entry.place(x=(size2 * 25) / 2 - 100 / 2 + 90,
                      y=60,
                      width=35,
                      height=25)

    ######
    size2_str = StringVar()
    size2_str.trace(
        "w", lambda name, index,
        mode, size_str=size1_str: callback12(size2_str))
    size2_entry = tk.Entry(upper_frame, textvariable=size2_str)
    size2_entry.place(x=(size2 * 25) / 2 - 5 / 2 + 90,
                      y=60,
                      width=35,
                      height=25)

    #######
    time_str = StringVar()
    time_str.trace(
        "w", lambda name, index, mode, time_str=time_str: callback3(time_str))

    time_label = tk.Label(upper_frame, text="Time")
    time_entry = tk.Entry(upper_frame, textvariable=time_str)
    time_label.place(x=(size2 * 25) / 2 - 35 / 2 - 90,
                     y=100,
                     width=35,
                     height=25)
    time_entry.place(x=(size2 * 25) / 2 - 35 / 2 - 40,
                     y=100,
                     width=35,
                     height=25)

    start_btn = tk.Button(upper_frame, command=initGame, text="New Game")
    start_btn.place(x=(25 * size2) / 2 - 35, y=10, width=70, height=25)

    upper_frame.pack(side="top")
    center_frame.pack(side="bottom")
    for i in range(size1):
        line_frames = []
        for j in range(size2):
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
    """
    Loads the images the application will need.
    """
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
    """
    Called when pressing the start button,
    this function resets all the variables to their initial values,
    before the game has started.
    It also calls the initGUI() function and starts the timer thread if needed.
    """
    global game
    global board
    global playerBoard
    global frames
    global size1
    global size2
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
    """
    Called when pressing left click,
    the function identifies whether or not the player has pressed on a square.
    If the answers is yes, it checks different things such as:
      - if the pressed square is flagged, nothing will happen,
      the user has to unflag it with right click

      - if the pressed square is a bomb, the player loses,
      a pop-up message will appear, and the showBombs() function will be called

      - if the pressed square is clear, but it has adjacent bombs,
      it will display the number of adjacent bombs

      - if the pressed square is clear and it doesn't have adjacent bombs,
      it will call a recursive function that uncovers all the
      adjecent squares which don't have bombs next to them
    Args:
        event (tkinter.Event): The event given by the GUI library.
    """
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
                        if i != 0 or j != 0:
                            if x + i >= 0 and x + i < size1:
                                if y + j >= 0 and y + j < size2:
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
                            if i != 0 or j != 0:
                                if (x + i >= 0) and (x + i < size1):
                                    if (y + j >= 0) and (y + j < size2):
                                        if playerBoard[x + i][y + j] == -1:
                                            uncoverBoard(x + i, y + j)
                ok = True
                for i in range(0, size1):
                    for j in range(0, size2):
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
    """
    A function that is called when the game finishes.
    It can show when the player wins, clicks on a bomb or loses on time.
    Args:
        msg (string): The string that will be displayed on the pop-up.
    """
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
    """
    This function is called when the player clicks on a bomb.
    In that moment the position of all the bombs will be shown to the player.
    Args:
        x (int): The row number of the clicked square.
        y (int): The column number of the clicked square.

    """
    for i in range(0, size1):
        for j in range(0, size2):
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
    """
    This is the recursive function that is called on every neighbour
    of a square that doesn't have any adjcent bombs.
    If the square at x, y doesn't have an adjcent bomb,
    then the recursive function will be called on its neighbours as well.
    If it does, then the number of adjcent bombs will be displayed
    and no recursive call will be made.
    Args:
        x (int): The row number of the clicked square.
        y (int): The column number of the clicked square.
    """
    adjBombs = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if x + i >= 0 and x + i < size1:
                    if y + j >= 0 and y + j < size2:
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
                if i != 0 or j != 0:
                    if (x + i >= 0) and (x + i < size1):
                        if y + j >= 0 and y + j < size2:
                            if playerBoard[x + i][y + j] == -1:
                                uncoverBoard(x + i, y + j)


def rightClick(event):
    """
    This function is called when pressing the right click.
    If the square pressed is already flagged, it will un-flag it.
    If it isn't flagged, it will flag it.
    Flagged squares will be ignored in the recursive
    proccess of uncovering squares,
    since it is presumably a bomb.
    Args:
        event (tkinter.Event): The event given by the GUI library.
    """
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


def callback11(size1_str):
    """
    This function keeps track of the input in the size1 text field.
    It updates the variable size1 if certain conditions are met.
    This variable will be used when pressing the 'New Game' button.
    Args:
        size1_str (StringVar): The value typed in the respective entry field.
    """
    global size1
    if size1_str.get().isnumeric() and int(size1_str.get()) <= 30:
        if len(size1_str.get()) > 1:
            size1 = int(size1_str.get())


def callback12(size2_str):
    """
    This function keeps track of the input in the size2 text field.
    It updates the variable size2 if certain conditions are met.
    This variable will be used when pressing the 'New Game' button.
    Args:
        size2_str (StringVar): The value typed in the respective entry field.
    """
    global size2
    if size2_str.get().isnumeric() and int(size2_str.get()) <= 30:
        if len(size2_str.get()) > 1:
            size2 = int(size2_str.get())


def callback2(mine_str):
    """
    This function keeps track of the input in nrOfBombs text field.
    It updates the variable nrOfBombs if certain conditions are met.
    This variable will be used when pressing the 'New Game' button.
    Args:
        mine_str (StringVar): The value typed in the respective entry field.
    """
    global nrOfBombs
    if mine_str.get().isnumeric():
        if len(mine_str.get()) > 0:
            nrOfBombs = int(mine_str.get())


def callback3(time_str):
    """
    This function keeps track of the input in timer text field.
    It updates the variable timer if certain conditions are met.
    This variable will be used when pressing the 'New Game' button.
    Args:
        time_str (StringVar): The value typed in the respective entry field.
    """
    global timer
    if time_str.get().isnumeric():
        if len(time_str.get()) > 0:
            timer = int(time_str.get())


root.protocol("WM_DELETE_WINDOW", on_closing)
root.wm_title("Minesweeper")
root.bind('<Button-1>', leftClick)
root.bind('<Button-3>', rightClick)
loadImages()
initGUI()
root.mainloop()
