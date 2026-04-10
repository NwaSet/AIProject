from tkinter import * 

POSSIBLE_PLAYER_COLOR = ["brown", "pink", "blue"]

class playerSelection(Frame) :

    def __init__(self, parent, player_number) :
        super().__init__(parent)

        self.label_player_number = Label(self, font="Arial 20", text=f"P{player_number}.")

        self.label_player_name = Label(self, font="Arial 14", text="Player name :")
        self.player_name = Text(self, height=1, width=20)

        self.player_type = StringVar(value="ai")
        self.label_player_type = Label(self, font="Arial 14", text="Player type :")
        self.player_type_sellection_1 = Radiobutton(self, text="IA", variable=self.player_type, value="ai")

        self.player_type_sellection_2 = Radiobutton(self, text="Human", variable=self.player_type, value="human")

        self.player_color = StringVar(value=POSSIBLE_PLAYER_COLOR[0])

        self.label_player_color = Label(self, font="Arial 14", text="Player color :")
        self.player_color_selection_1 = Radiobutton(self, text = "brown", variable=self.player_color, value=POSSIBLE_PLAYER_COLOR[0], bg="lightblue")
        self.player_color_selection_2 = Radiobutton(self, text = "pink", variable=self.player_color, value=POSSIBLE_PLAYER_COLOR[1], bg="lightblue")
        self.player_color_selection_3 = Radiobutton(self, text = "blue", variable=self.player_color, value=POSSIBLE_PLAYER_COLOR[2], bg="lightblue")

        self.label_player_number.pack()

        self.label_player_name.pack()
        self.player_name.pack()

        self.label_player_type.pack()
        self.player_type_sellection_1.pack()
        self.player_type_sellection_2.pack()

        self.label_player_color.pack()
        self.player_color_selection_1.pack()
        self.player_color_selection_2.pack()
        self.player_color_selection_3.pack()

        
    
    def get_dto(self) :
        return {
            "player_name" : self.player_name,
            "player_type" : self.player_type,
            "player_color" : self.player_type,
        }