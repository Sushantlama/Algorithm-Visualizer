from snake import Snake
from tkinter import *

root = Tk(className="python")
root.resizable(False,False)
snake = Snake(root)
root.bind("<KeyPress-Left>", lambda e: snake.left(e))
root.bind("<KeyPress-Right>", lambda e: snake.right(e))
root.bind("<KeyPress-Up>", lambda e: snake.up(e))
root.bind("<KeyPress-Down>", lambda e: snake.down(e))

root.mainloop()


