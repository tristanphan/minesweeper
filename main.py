import tkinter as tk
import random

restarts = True
while restarts:
    restarts = False
    window = [720, 600]
    screen = tk.Tk()
    screen.config(width=window[0], height=window[1])
    screen.title("Minesweeper for Python")
    firstMove = True
    gameEnd = False
    clickedFrames = []


    class Frames:
        def __init__(self, input_row, input_column, input_size, input_color):
            self.row = input_row
            self.column = input_column
            self.size = input_size
            self.color = input_color
            self.frame = tk.Frame(screen,
                                  height=self.size,
                                  width=self.size,
                                  bg=input_color,
                                  bd=5,
                                  highlightbackground="#000000",
                                  highlightcolor="#000000",
                                  relief="raised")
            self.frame.pack_propagate(0)
            self.frame.bind("<Enter>", self.enter)
            self.frame.bind("<Leave>", self.leave)
            self.frame.grid(row=self.row, column=self.column)
            self.text = tk.Label(self.frame, text="", bg=input_color, fg=input_color, font=("Helvetica", 15))
            self.text.pack()
            self.frame.lift()
            self.clickStatus = False
            self.flagOn = False
            self.isBomb = False

        def flag(self, event=None):
            if not self.clickStatus and not gameEnd:
                if self.flagOn:
                    self.text.config(bg=self.color, fg=self.color)
                    self.frame.config(bg=self.color)
                    self.flagOn = False
                else:
                    self.text.config(bg="#ff8f87", fg="#ff8f87")
                    self.frame.config(bg="#ff8f87")
                    self.flagOn = True
                check_win()

        def mine(self, event=None):
            global firstMove
            if self.clickStatus and not self.flagOn and not gameEnd:
                fill_in(self)
            if not self.clickStatus and not self.flagOn and not gameEnd:
                if firstMove:
                    firstMove = False
                    generate_squares(self)
                self.clickStatus = True
                self.text.config(fg="#000000")
                if self.isBomb:
                    self.frame.config(relief="sunken")
                    lost(self)
                else:
                    generate_area(self)
                    self.frame.config(relief="sunken")
                clickedFrames.append(self)
            check_win()

        def enter(self, event=None):
            self.frame.focus_set()
            self.frame.bind("f", self.flag)
            self.frame.bind("<Button-2>", self.flag)
            self.frame.bind("c", self.mine)
            self.frame.bind("<Button-1>", self.mine)

        def leave(self, event=None):
            self.frame.unbind("f")
            self.frame.unbind("c")
            self.frame.bind("<Button-1>", self.mine)
            self.frame.bind("<Button-2>", self.mine)

        def __str__(self):
            return f"frameR{self.row}C{self.column}"


    # Window Settings
    size = 30
    columns = window[0] // size
    rows = window[1] // size
    color = ["#FFFFFF", "#C0C0C0"]
    allSquares = []

    # Create Blocks
    for column in range(columns):
        for row in range(rows):
            exec(f"frameR{row}C{column} = Frames(row,column,size,color[1])")
            allSquares.append(f"frameR{row}C{column}")

    bombCount = 99
    bombs = []

    def generate_squares(frame):
        while len(bombs) != bombCount:
            skip = False
            random_column = random.randrange(0, columns)
            random_row = random.randrange(0, rows)
            if ((not eval(f"frameR{random_row}C{random_column}") in bombs)
                    and eval(f"frameR{random_row}C{random_column}") != frame):
                for this_row in range(frame.row - 1, frame.row + 2):
                    for this_column in range(frame.column - 1, frame.column + 2):
                        if not (this_row < 0 or this_row > rows - 1 or this_column < 0 or this_column > columns - 1):
                            if random_column == this_column and random_row == this_row:
                                skip = True
                if not skip:
                    bombs.append(eval(f"frameR{random_row}C{random_column}"))
        for i in bombs:
            exec(f"{i}.text.config(text=\"O\")")
            exec(f"{i}.isBomb = True")


    def generate_area(frame):
        bomb_around = 0
        for this_row in range(frame.row - 1, frame.row + 2):
            for this_column in range(frame.column - 1, frame.column + 2):
                if not (this_row < 0 or this_row > rows - 1 or this_column < 0 or this_column > columns - 1):
                    if eval(f"frameR{this_row}C{this_column}.isBomb"):
                        bomb_around += 1
        if bomb_around == 0:
            bomb_around = ""
            for this_row in range(frame.row - 1, frame.row + 2):
                for this_column in range(frame.column - 1, frame.column + 2):
                    if not (this_row < 0 or this_row > rows - 1 or this_column < 0 or this_column > columns - 1):
                        if not (this_row == frame.row and this_column == frame.column):
                            exec(f"frameR{this_row}C{this_column}.mine(None)")
        frame.text.config(text=bomb_around)


    def fill_in(frame):
        flag_count = 0
        for this_row in range(frame.row - 1, frame.row + 2):
            for this_column in range(frame.column - 1, frame.column + 2):
                if not (this_row < 0 or this_row > rows - 1 or this_column < 0 or this_column > columns - 1):
                    if not (this_row == frame.row and this_column == frame.column):
                        if eval(f"frameR{this_row}C{this_column}.flagOn"):
                            flag_count += 1

        if frame.text['text'] == flag_count:
            free_blocks = []
            for this_row in range(frame.row - 1, frame.row + 2):
                for this_column in range(frame.column - 1, frame.column + 2):
                    if not (this_row < 0 or this_row > rows - 1 or this_column < 0 or this_column > columns - 1):
                        if (not eval(f"frameR{this_row}C{this_column}.clickStatus")
                                and not eval(f"frameR{this_row}C{this_column}.flagOn")):
                            free_blocks.append(f"frameR{this_row}C{this_column}")
            for i in free_blocks:
                exec(f"{i}.mine(None)")


    def lost(frame):
        for self in bombs:
            if frame != self:
                self.frame.config(relief="raised")
            self.text.config(fg="#FF0000", bg="#FF0000")
            self.frame.config(bg="#FF0000")
        global gameEnd
        gameEnd = True


    def check_win():
        if len(clickedFrames) == rows * columns - bombCount:
            won = True
        else:
            won = False
        if won:
            global gameEnd
            gameEnd = True
            cleared_blocks = allSquares.copy()
            for i in bombs:
                cleared_blocks.remove(str(i))
            for i in cleared_blocks:
                eval(f"{i}.frame.config(bg=\"#00FF00\", relief=\"raised\")")
                eval(f"{i}.text.config(bg=\"#00FF00\", fg=\"#00FF00\")")
            for i in bombs:
                i.frame.config(bg="#FF0000")
                i.text.config(bg="#FF0000", fg="#FF0000")


    def restart(event=None):
        global restarts
        restarts = True
        screen.destroy()


    def quits(event=None):
        screen.destroy()


    screen.bind("<space>", restart)
    screen.bind("<Escape>", quits)
    screen.mainloop()
