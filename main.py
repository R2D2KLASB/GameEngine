from player import Player

class GameEngine():
    def __init__(self):
        self.row_size = 10
        self.col_size = 10
        print('Player 1 Setup Ships')
        self.player1 = Player(self.row_size, self.col_size)
        print('Player 2 Setup Ships')
        self.player2 = Player(self.row_size, self.col_size)
        print('Attack coordinate:')
        self.player1.Turn(self.player2)
        print(self.player1)
        print(self.player2)




   

gameEngine = GameEngine()
