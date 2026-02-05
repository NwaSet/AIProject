import random 

class Game :
    def __init__(self, nb, player1,player2,displayable =True):
        self.original_nb = nb
        self.nb = nb
        
        self.player1 = player1
        self.player2 = player2
        
        self.displayable = displayable
        
        
        self.player1.game = self
        self.player2.game = self
        
        self.shuffle()
        
       
    def shuffle(self):
        players = [self.player1, self.player2]
        random.shuffle(players)
        self.player1, self.player2 = players
         
    def reset(self):
        self.nb = self.original_nb
        self.shuffle()
        
    def display(self):
        if self.displayable:
            print(f"Allumettes restantes : {self.nb}")
            
    def step(self, action):
        if (action < 1 or action > 3):
            return False

        if action > self.nb:
            action = self.nb

        self.nb -= action
        return True

    def play (self):
        self.reset
        
        current_player = self.player1
        other_player = self.player2
        
        while self.nb>0:
            self.display()
            
            self.step(current_player.play())
            
            current_player, other_player = other_player, current_player
            
        winner = current_player
        loser = other_player

        winner.win()
        loser.loose()
            
        
        
        

class Player :
    """
    A class represent a player

    Attributs:
        name (str)  : Player name
        game (Game) : Player game where he can be playing, he is not obliged to be in a game. 
    """
    def __init__(self, name, game=None):
        self.name = name
        self.game = game
        self.nb_win = 0
        self.nb_loose = 0
    
    @property
    def nb_game(self) :
        """
        return : the number of game plaied by the player
        """
        return self.nb_loose + self.nb_win
    
    def play(self) :
        choice = random.randint(1,3)
        return choice

    def win(self) :
        self.nb_win += 1

    def loose(self) :
        self.nb_loose += 1
        

class Human(Player) :
    def play(self) :
        choice = int(input("how many sticks do you wan't to take (1 - 3): "))
        return choice

class Ai(Player) :
    None

if __name__ == "__main__":
    player1 = Human("yo")
    player2 = Player("flo")
    
    game = Game(10,player1,player2)
    game.play()
    print(f"{player1.name} a {player1.nb_win} win")
