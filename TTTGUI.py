import sys
import random
import numpy as np

from PyQt5.QtWidgets import *
from main_menu_ui import *
from board_ui import *

class Player:
    def __init__(self, name, shape):
        self.name = str(name)
        self.shape = str(shape)
        self.counter = 0
        self.difficulty = ""
        self.ai = False

class Board(QDialog, Ui_tic_tac_toe_board):

    def __init__(self, size):
        super(Board, self).__init__()
        self.setupUi(self)
        self.size = size  # zrobić if, że musi być wiekszy lub rowny 3
        self.board = np.zeros(shape=(size, size), dtype="object")
        self.possible_moves = []
        self.create_board(size)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())

    def create_board(self, size):
        for i in range(size):
            for j in range(size):
                self.possible_moves.append((i, j))
                print(self.possible_moves)
                self.board[i][j] = QPushButton("-")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.board[i][j].sizePolicy().hasHeightForWidth())
                self.board[i][j].setSizePolicy(sizePolicy)
                # used lambda and "_" as argument because clicked signal always has a bool argument as the first arg
                self.board[i][j].clicked.connect(lambda _, i=i, j=j: self.evt_clicked_ttt_board(i, j))
                self.ttt_board.addWidget(self.board[i][j], i, j)

    def evt_clicked_ttt_board(self, row, col):
        rcv = self.sender()
        print(rcv.settext(), row, col)

    def current_turn(self):
        if self.player1.counter == self.player2.counter:
            if self.player1.shape == "X":
                self.player1.counter += 1
                return self.player_move(self.player1)
            else:
                self.player2.counter += 1
                if self.player2.ai:
                    return self.ai_move()
                else:
                    return self.player_move(self.player2)
        else:
            if self.player1.shape == "O":
                self.player1.counter += 1
                return self.player_move(self.player1)
            else:
                self.player2.counter += 1
                if self.player2.ai:
                    return self.ai_move()
                else:
                    return self.player_move(self.player2)

    def player_move(self, player):
        #todo timer/countdown depends on difficulty level
        difficulty_level = self.player2.difficulty
        if difficulty_level:
            if difficulty_level == "1":
                seconds = 10
            if difficulty_level == "2":
                seconds = 7
            if difficulty_level == "3":
                seconds = 5


        row, column = int(input(f"{player.name}, enter the row for {player.shape}: ")), int(input(f"{player.name}, enter the column for {player.shape}: "))
        self.insert_char(player.shape, row, column)



    # depends on selected difficulty call different method responsibilities for AI moves
    def ai_move(self):
        if self.player2.difficulty == "1":
            self.easy_level()
        if self.player2.difficulty == "2":
            self.intermediate_level()
        if self.player2.difficulty == "3":
            self.hard_level()

    def easy_level(self):
        # Check if AI could win in next move
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.board[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column] = "-"
                self.insert_char(self.player2.shape, row, column)
            else:
                self.board[row][column] = "-"

        # random choice from possible moves list, then call insert_char with that row/column
        position = random.choice(self.possible_moves)
        self.insert_char(self.player2.shape, int(position[0]), int(position[1]))


    def insert_char(self, char, row, column):
        # check free position in the board
        if self.is_free_space(row, column):
            # insert char into specific position in the board
            self.board[row][column] = char
            # remove (row, column) from list of empty cells in the board
            self.possible_moves.remove((row, column))
            self.display_board()
            # check that after insertion is the end of the game
            if self.is_draw():
                print("Draw!")
                exit() #todo: change to call clear board
            if self.is_win(): # do poprawy informacja kto wygrywa
                if char == "X":
                    print("AI wins!")
                    exit() #todo: change to call clear board
                else:
                    print("Player wins!")
                    exit() #todo: change to call clear board
        else:
            print("This position is not empty, please insert it somewhere else")
            self.current_turn()
            return

class DlgMain(QDialog, Ui_Dialog, Ui_tic_tac_toe_board):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())
        self.ai_btn.clicked.connect(self.event_opponent_choice_clicked)
        self.human_btn.clicked.connect(self.event_opponent_choice_clicked)
        self.start_game_btn.clicked.connect(self.main_menu)


    def main_menu(self):
        self.difficulties = self.group_btns_levels.checkedButton().text()
        self.create_players(self.player1_name.text(), self.player2_name.text())
        self.board = Board(self.board_size.value())
        self.board.show()

    def create_players(self, player_name="Human1", player2_name="Human2"):
        shapes = ["X", "O"]
        self.player1 = Player(name=player_name, shape=random.choice(shapes))
        # Remove selected shape from shapes list
        shapes.remove(self.player1.shape)
        if self.ai_btn.isChecked():
            self.player2 = Player(name="AI", shape=random.choice(shapes))
            self.player2.difficulty = self.difficulties
            self.player2.ai = True
            return
        elif self.human_btn.isChecked():
            self.player2 = Player(name=player2_name, shape=random.choice(shapes))
            return


    # Checks what opponent user choose and activate specific part of lower menu(depends on a choice)
    def event_opponent_choice_clicked(self):
        rbt = self.sender()
        if rbt.text() == "AI":
            self.ai_difficulty_gbtns.setEnabled(True)
            self.player2_name.setEnabled(False)
            self.player2_label.setEnabled(False)
            self.difficulties = self.group_btns_levels.checkedButton().text()
        elif rbt.text() == "Human":
            self.player2_name.setEnabled(True)
            self.player2_label.setEnabled(True)
            self.ai_difficulty_gbtns.setEnabled(False)
        return rbt.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg_main = DlgMain()
    dlg_main.show()
    sys.exit(app.exec_())