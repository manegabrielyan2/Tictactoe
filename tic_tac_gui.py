import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox
    
    )
from board import Board
from player import Player

class TicTacToeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setContentsMargins(30 , 30 , 30 , 30)
        self.board = None
        self.players = []

        self.create_widgets()
        self.set_up_layouts()
        with open('design.css' , 'r') as file:
            self.setStyleSheet(file.read())
        
    def create_widgets(self):
        self.info_label = QLabel("Please enter your names to start the game!")
        self.info_label.setStyleSheet("font-size : 18px")
        self.player1_label = QLabel("Player X's name:")
        self.player1_edit = QLineEdit()
        self.player2_label = QLabel("Player O's name:")
        self.player2_edit = QLineEdit()
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)

    def set_up_layouts(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.info_label)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.player1_label)
        hbox1.addWidget(self.player1_edit)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.player2_label)
        hbox2.addWidget(self.player2_edit)
        vbox.addLayout(hbox2)

        vbox.addWidget(self.start_button)
        self.setLayout(vbox)

    def accept_player(self , pl1 , pl2):
        self.players = [pl1 , pl2]

    def start_game(self):
        player1_name = self.player1_edit.text()
        player2_name = self.player2_edit.text()
        if player1_name and player2_name:
            player1 = Player(player1_name , 'X')
            player2 = Player(player2_name , 'O')
            self.board = Board()
            self.accept_player(player1 , player2)
            self.game_window = GameWindow(self.board, self.players)
            self.game_window.show()
            self.close()
        else:
            QMessageBox.critical(self , "Error" , "Please enter your names.")

class GameWindow(QWidget):
    def __init__(self, board, players):
        super().__init__()
        self.board = board
        self.players = players
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setContentsMargins(60 , 60 , 60 , 60)

        self.buttons = []
        layout = QVBoxLayout()

        for i in range(3):
            row = QHBoxLayout()
            for j in range(3):
                button = QPushButton('')
                button.setFixedSize(100 , 100)
                button.clicked.connect(lambda k , i=i , j=j: self.on_button_click(i , j))
                self.buttons.append(button)
                row.addWidget(button)
            layout.addLayout(row)
        self.setLayout(layout)
        with open('design.css' , 'r') as file:
            self.setStyleSheet(file.read())

    def on_button_click(self, i, j):
        current_player = self.players[0] if len([1 for m in self.board.board for n in m if n != '_']) % 2 == 0 else self.players[1]
        current_player.draw(self.board.board, i , j)
        self.update_buttons()
        winner = self.check_winner()
        if winner == 'Draw':
            QMessageBox.information(self, "Draw", "This is a draw!")
            self.close()
        elif winner:
            QMessageBox.information(self, "Congrats", f"{winner} won this turn!")
            self.close()

    def update_buttons(self):
        for i, button in enumerate(self.buttons):
            n = i // 3
            m = i % 3
            button.setText(self.board.board[n][m])

    def check_winner(self):
        for i in range(3):
            if self.board.board[i] == [self.players[0].marker for i in range(3)]:
                return self.players[0].name
            elif self.board.board[i] == [self.players[1].marker for i in range(3)]:
                return self.players[1].name
            elif [self.board.board[j][i] for j in range(3)] == [self.players[0].marker for i in range(3)]:
                return self.players[0].name
            elif [self.board.board[j][i] for j in range(3)] == [self.players[1].marker for i in range(3)]:
                return self.players[1].name

        if [self.board.board[i][i] for i in range(3)] == [self.players[0].marker for i in range(3)]:
            return self.players[0].name
        elif [self.board.board[i][i] for i in range(3)] == [self.players[1].marker for i in range(3)]:
            return self.players[1].name
        elif [self.board.board[0][2] , self.board.board[1][1] , self.board.board[2][0]] == [self.players[0].marker for i in range(3)]:
            return self.players[0].name
        elif [self.board.board[0][2] , self.board.board[1][1] , self.board.board[2][0]] == [self.players[1].marker for i in range(3)]:
            return self.players[1].name
        countt = 0
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] != '_':
                    countt += 1
        if countt == 9:
            return 'Draw'
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToeGUI()
    window.show()
    sys.exit(app.exec())
