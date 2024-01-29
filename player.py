class Player:
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker
    def draw(self , board , i , j):
        if i in range(3) and j in range(3):
            if board[i][j] == "_":
                board[i][j] = self.marker
           