import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

chosen_size = int(min(screen_height, screen_width)*0.9)

DIMENSION = 8
WIDTH, HEIGHT = chosen_size, chosen_size
FPS = 60
SQUARE_SIZE = HEIGHT//DIMENSION
BOARD_RANKS = ['8', '7', '6', '5', '4', '3', '2', '1']
BOARD_FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']