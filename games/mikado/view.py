from tkinter import *
from .gameControler import *
from .gameModel import *

class GameView(Tk) :

    """
    A class for display the GUI of the game
    """

    def __init__(self, controler: object):
        """
        Initializes the visual interface for the Mikado game.

        Args:
            controler (GameController): The controller instance that handles 
                the communication between the model and this view.
                
        Note:
            This class inherits from a Tkinter parent
            to create the main game window and its graphical components.
    """
        super().__init__()

        #Link the controller to this view
        self.controler = controler
        self.controler.view = self

        #Windows configuartion
        self.title("Mikado Game")
        self.resizable(False, False)

        #GUI components initialization
        self.canvas = Canvas(self, width=700, height=200)
        self.canvas.pack()

        #initiate the labal message to say whose turn it is
        self.label_message = Label(self, font="Arial 20")
        self.label_message.pack()

        # initiate the variable for the button frame
        self.button_frame = None
        self.reset_button_frame = None

        self.add_button()

    def update_view(self) :
        """
        Refreshes the entire user interface.
        
        Clears the canvas, redraws the remaining matchsticks, 
        and updates the status message label.
        """
        self.canvas.delete("all")

        self.draw_matches(self.controler.get_nb_matches())

        status_message = self.controler.get_status_message()
        self.label_message.config(text=status_message)


    def add_button(self) :
        """
        Initialise and display the action buttons
        """
        self.button_frame = ButtonFrame(self, self.controler)
        self.button_frame.pack()
    
    def add_reset_button(self) :
        """
        Initialise and display the restart buttons
        """
        self.reset_button_frame = ResetButtonFrame(self, self.controler)
        self.reset_button_frame.pack()

    def end_game(self) :
        """
        Handles the GUI transition to the 'Game Over' state.
        
        Removes move buttons, clears the matchstick display, shows the 
        final result, and offers a restart option.
        """
        self.button_frame.destroy()
        self.canvas.delete("all")
        self.label_message.config(text=f"game over. . . {self.controler.get_loser()} you loose !!")

        self.add_reset_button()


    def reset(self) :
        """
        Restores the GUI to its initial game state
        """
        self.update_view()
        self.reset_button_frame.destroy()
        self.add_button()

    def draw_matches(self, nb_stick) :
        """
        Renders the graphical representation of the sticks on the canvas.

        Args:
            nb_stick (int): The current number of sticks remaining in the game.
        """
        for i in range(nb_stick) :
            self.canvas.create_rectangle((i*50)+73, 50 , (i*50)+77 , 150 , fill="brown")
            self.canvas.create_oval((i*50)+72, 43 , (i*50)+78 , 55 , fill="red")

    


class ButtonFrame(Frame) :

    """
    A container for the move action buttons (Take 1, 2, or 3 sticks).
    """

    def __init__(self, parent, controler) :
        """
        Initializes the frame and its three action buttons.
        
        Args:
            parent (Widget): The parent Tkinter container.
            controler (GameController): The controller to make moves.
        """ 
        super().__init__(parent)

        self.controler = controler

        self.button1 = Button(self, text="take 1", width=10,
                              command = lambda : self.controler.handle_human_move(1))
        self.button2 = Button(self, text="take 2", width=10,
                              command = lambda : self.controler.handle_human_move(2))
        self.button3 = Button(self, text="take 3", width=10,
                              command = lambda : self.controler.handle_human_move(3))

        self.button1.pack(side="left", pady=25, padx = 25)
        self.button2.pack(side="left",pady=25, padx = 25)
        self.button3.pack(side="left",pady=25, padx = 25)
    
class ResetButtonFrame(Frame) :

    """
    A container for the restart button
    """
    def __init__(self, parent, controler) :
        """
        Initializes the frame with a restart button.
        
        Args:
            parent (Widget): The parent Tkinter container.
            controler(GameControler): the controller for restart the game
        """
        super().__init__(parent)

        self.controler = controler

        self.reset_button = Button(self, text="Restart A New Game", width=30,
                                   command= lambda : self.controler.reset_game())
        self.reset_button.pack(pady=25)