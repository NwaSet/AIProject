import random

class Game :
    def __init__(self, player1, player2, nb_stick=12, displayable =True):
        self.original_nb_stick = nb_stick
        self.nb_stick = nb_stick
        
        self.player1 = player1
        self.player2 = player2
        
        self.displayable = displayable
        
        self.player1.game = self
        self.player2.game = self
        
        self.shuffle()

        self.controler = None
        
       
    def shuffle(self):
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.player1, self.player2 = players
         
    def reset(self):
        self.nb_stick = self.original_nb_stick
        self.shuffle()
                
    def step(self, action):
        if (action < 1 or action > 3):
            return False

        if action > self.nb_stick:
            action = self.nb_stick

        self.nb_stick -= action
        if self.nb_stick != 0 :
            self.player1, self.player2 = self.player2, self.player1
            self.controler.update_game()
        else :
            self.controler.is_game_over(self.player1.name)
        return True