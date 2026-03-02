from games.gamesView import *
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()

    controller = GameSelectionController()
    view = GameSelectionView(root, controller)
    view.pack()

    root.mainloop()