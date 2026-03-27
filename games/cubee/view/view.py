import tkinter as tk
from ..controler.controler import gameControler


class View:
    """
    Represent the graphical user interface of the Cubee game.

    This class is responsible for:
    - displaying the game grid
    - showing players and their positions
    - displaying game information such as scores and current player
    - handling the graphical end-of-game screen
    - updating the interface according to the model state

    It interacts with the controller to retrieve model data and to
    trigger player actions.
    """

    def __init__(self, controler: gameControler = None) -> None:
        """
        Initialize the game view.

        - stores the controller reference
        - links the view to the controller
        - retrieves initial model data
        - configures the Tkinter window
        - binds keyboard arrows for human moves
        - creates the canvas and restart button
        """
        self.controler = controler
        self.controler.view = self

        self.data = self.controler.get_model_data()

        self.nb_case = self.data["grid_size"]
        self.grid = self.data["grid"]
        self.players_score = self.data["players"]
        self.player_id = self.data["player_id"]
        self.current_player = self.data["current_player"]
        self.player_names = list(self.players_score.keys())
        self.size = 100
        self.root = tk.Tk()
        self.root.title("Cubee")

        self.root.focus_set()

        self.root.bind(
            "<Left>", lambda event: self.controler.handle_human_move((-1, 0))
        )
        self.root.bind(
            "<Right>", lambda event: self.controler.handle_human_move((1, 0))
        )
        self.root.bind("<Up>", lambda event: self.controler.handle_human_move((0, -1)))
        self.root.bind("<Down>", lambda event: self.controler.handle_human_move((0, 1)))

        self.max_size = self.size * self.nb_case
        self.canva = tk.Canvas(
            self.root,
            width=self.max_size + 200,
            height=self.max_size + 5,
        )
        self.canva.pack(padx=(20, 5))

        self.player_coord = self.data["player_coord"]
        self.player_color = self.data["player_color"]

        self.cases = []
        self.score_text = None

        self.restart_button = tk.Button(
            self.root, text="Restart", command=self.controler.reset_game
        )

    def creation_grid(self) -> None:
        """
        create and diplay the game grid on the canvas
        """
        self.canva.delete("all")
        self.cases = []
        offset = 4

        for row in range(self.nb_case):
            line = []
            for col in range(self.nb_case):
                x = col * self.size + offset
                y = row * self.size + offset

                cell_value = self.grid[row][col]

                if cell_value == self.player_id[0]:
                    fill_color = self.player_color[0]
                elif cell_value == self.player_id[1]:
                    fill_color = self.player_color[1]
                else:
                    fill_color = "white"

                case = self.canva.create_rectangle(
                    x,
                    y,
                    x + self.size,
                    y + self.size,
                    fill=fill_color,
                    outline="gray",
                    width=2,
                    tags="grid",
                )

                line.append(case)
            self.cases.append(line)

        self.canva.create_rectangle(
            offset,
            offset,
            self.max_size + offset,
            self.max_size + offset,
            outline="gray",
            width=2,
        )

    def display_infos(self) -> None:
        """
        show all informations of the game :
        - whos turn it is
        - players colors
        - score
        """
        info_x = self.max_size + 30

        player1_name = self.player_names[0]
        player2_name = self.player_names[1]

        score_p1 = self.players_score[player1_name]
        score_p2 = self.players_score[player2_name]
        current_player_name = str(self.current_player)

        ### label information ###
        self.canva.create_text(
            info_x, 30, text="Informations", font=("Arial", 16, "bold"), anchor="nw"
        )

        ### label current player ###
        self.canva.create_text(
            info_x,
            80,
            text=f"Tour de : {current_player_name}",
            font=("Arial", 14),
            anchor="nw",
        )

        ### label color ###
        self.canva.create_text(
            info_x, 130, text="Couleurs :", font=("Arial", 14, "bold"), anchor="nw"
        )

        # player 1
        self.canva.create_rectangle(
            info_x, 165, info_x + 20, 185, fill=self.player_color[0], outline="black"
        )
        self.canva.create_text(
            info_x + 30,
            175,
            text=f"{player1_name} ({self.player_color[0]})",
            font=("Arial", 12),
            anchor="w",
        )

        # player 2
        self.canva.create_rectangle(
            info_x, 205, info_x + 20, 225, fill=self.player_color[1], outline="black"
        )
        self.canva.create_text(
            info_x + 30,
            215,
            text=f"{player2_name} ({self.player_color[1]})",
            font=("Arial", 12),
            anchor="w",
        )

        ### label score ###
        self.canva.create_text(
            info_x, 270, text="Scores :", font=("Arial", 14, "bold"), anchor="nw"
        )

        self.canva.create_text(
            info_x,
            305,
            text=f"{player1_name} : {score_p1}\n{player2_name} : {score_p2}",
            font=("Arial", 12),
            anchor="nw",
        )

    def game_over(self) -> None:
        """
        pack on the canvas the game over and show the button to restart a new game
        """
        loser = self.controler.get_loser()
        info_x = self.max_size + 30

        # Position sous les infos
        y_base = 380

        self.canva.create_text(
            info_x,
            y_base,
            text="GAME OVER",
            font=("Arial", 20, "bold"),
            fill="red",
            anchor="nw",
            tags="game_over",
        )

        self.canva.create_text(
            info_x,
            y_base + 30,
            text=f"player {loser}, you lose !",
            font=("Arial", 12),
            anchor="nw",
            tags="game_over",
        )

        self.restart_button = tk.Button(
            self.root, text="Restart", command=self.controler.reset_game, width=20
        )

        self.canva.create_window(
            info_x,
            y_base + 70,
            window=self.restart_button,
            anchor="nw",
            tags="game_over",
        )

    def display_player(self) -> None:
        """
        show the circle where the players are
        """
        self.canva.delete("player")

        radius = self.size // 3

        for i, (col, row) in enumerate(self.player_coord):
            x_center = col * self.size + self.size / 2 + 4
            y_center = row * self.size + self.size / 2 + 4

            x0 = x_center - radius
            y0 = y_center - radius
            x1 = x_center + radius
            y1 = y_center + radius

            self.canva.create_oval(
                x0,
                y0,
                x1,
                y1,
                fill=self.player_color[i],
                outline="black",
                width=2,
                tags="player",
            )

    def refresh_data(self) -> None:
        """
        Met à jour les données venant du modèle
        """
        self.data = self.controler.get_model_data()
        self.nb_case = self.data["grid_size"]
        self.grid = self.data["grid"]
        self.players_score = self.data["players"]
        self.player_id = self.data["player_id"]
        self.player_coord = self.data["player_coord"]
        self.player_color = self.data["player_color"]
        self.current_player = self.data["current_player"]

    def update_view(self) -> None:
        """
        update all view to show the new game status
        """
        self.refresh_data()
        self.creation_grid()
        self.display_player()
        self.display_infos()

    def run(self) -> None:
        """
        start the mainloop
        and update the view one first time
        """
        self.update_view()
        self.root.mainloop()
