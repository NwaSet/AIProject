class Game :
    None

class Player :
    def __init__(self, name):
        self.name = name
        self.nb_win = 0
        self.nb_loose = 0
    
    @property
    def nb_game(self) :
        return self.nb_loose + self.nb_win
    
    def play(self) :
        pass

    def win(self) :
        pass

    def loose(self) :
        pass
        

class Human(Player) :
    None

class Ai(Player) :
    None
