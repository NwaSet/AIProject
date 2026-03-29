from games.games_view import *


if __name__ == "__main__":
    controller = GameSelectionController()
    view = GameSelectionView(controller)
    view.mainloop()

