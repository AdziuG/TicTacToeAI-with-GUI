import functools
import sys
import random
import time
from pprint import pprint

import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from PyQt5.QtWidgets import *
from main_menu_ui import *
from board_ui import *

"""
class TimerThread(QThread):
    update_timer = pyqtSignal(int)
    finished_timer = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        i = 5
        while self.running and i > 0:
            time.sleep(1)
            print(i)
            self.update_timer.emit(i)
            i -= 1
        self.finished_timer.emit(object)

        #TODO W QTHREAD ZROBIĆ QTIMER. QTIMER ODMIERZA CZAS, GDY KLIKAMY W POLE TO SIĘ RESETUJE I ODMIERZA OD POCZĄTKU.
        # GDY PRZEKROCZY CZAS TO ZAMYKAMY QTHREAD Z WYSKAKUJĄCYMI POPUPAMI

"""

class Player(Ui_tic_tac_toe_board):
    def __init__(self, name, shape):
        self.name = str(name)
        self.shape = str(shape)
        self.counter_wins = 0
        self.difficulty = ""
        self.ai = False


class TicTacToeCell(QPushButton):
    def __init__(self, row, column):
        super().__init__()
        self.text = ''
        self.size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.size.setHorizontalStretch(0)
        self.size.setVerticalStretch(0)
        self.size.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.size)
        self.row = row
        self.column = column

    def captured(self):
        return self.text

    def capture(self, symbol):
        self.text = symbol
        print(f"w capture {symbol}")
        self.setText(symbol)
        self.setEnabled(False)

    def reset(self):
        self.text = ''
        self.setText(self.text)
        self.setEnabled(True)

    def __repr__(self):
        return f'[{self.text}]'


class Board(QDialog, Ui_tic_tac_toe_board):

    def __init__(self, size, players):
        super(Board, self).__init__()
        self._init_ui(players)
        self._init_btns()
        # start game
        self._init_board(size, players)


    def _init_ui(self, players):
        self.setupUi(self)
        self.player1_name_counter.setText(players[0].name)
        self.player2_name_counter.setText(players[1].name)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())

    def _init_btns(self):
        self.exit_btn.clicked.connect(self.exit_board)
        self.new_game_btn.clicked.connect(self.new_game_btn_clicked)
        self.btn_grp_board = QButtonGroup()

    def _init_board(self, size, players):
        self.size = size
        self.board = np.zeros(shape=(size, size), dtype=object)
        self.push_list = np.zeros(shape=(size, size), dtype="str")
        self.possible_moves = []
        self.player1 = players[0]
        self.player2 = players[1]
        self.create_board(size)
        self.sec = 7
        self.previous_player = None
        self.current_turn_func()
        self.current_turn(None)

    def create_board(self, size):
        for i in range(size):
            for j in range(size):
                self.possible_moves.append((i, j))
                self.board[i][j] = TicTacToeCell(i, j)
                self.btn_grp_board.addButton(self.board[i][j])
                self.push_list[i][j] = "-"
                self.board[i][j].clicked.connect(functools.partial(self.button_clicked, i, j))
                self.board[i][j].clicked.connect(self.current_turn_func)
                # used lambda and "_" as argument because clicked signal always has a bool argument as the first arg
                self.ttt_board.addWidget(self.board[i][j], i, j)

    def exit_board(self):
        try:
            self.timer.stop()
            self.close()
        except AttributeError:
            self.close()

    def button_clicked(self, row, col):
        try:
            if not self.player2.ai:
                self.sec = 5
            if self.timer.isActive():
                self.timer.start()
            else:
                self.create_timer()
        except AttributeError:
            self.create_timer()
        player = self.current_turn(self.previous_player)
        button = self.sender()
        print(self.objectName())
        print(f"Player {player}")
        print(f"row {row}, col {col} w button clicked")
        print(f"w button clicked{player.shape}")
        button.capture(player.shape)
        self.push_list[row][col] = player.shape
        self.control_state(player, row, col)

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.evt_update_timer)
        self.timer.setInterval(950)  # 1000ms = 1s
        self.timer.start()


    def evt_update_timer(self):
        self.sec -= 1
        self.move_countdown.display(self.sec)
        if self.sec == 0:
            self.evt_finished_timer(self.previous_player)


    def evt_finished_timer(self, player):
        if player is None:
            QMessageBox.information(self, "Game status", "Game Over!\nNobody wins because only 1 player got move")
        else:
            QMessageBox.information(self, "Game status", f"Time for move is over!\n{player.name} WIN!")
            player.counter_wins += 1
        self.update_lcd()
        self.reset_game()

    def current_turn_func(self):
        if self.previous_player == self.player1:
            self.current_turn_changed.setText(self.player2.name)
        elif self.previous_player == self.player2:
            self.current_turn_changed.setText(self.player1.name)
        else:
            if self.player2.shape == "X":
                self.current_turn_changed.setText(self.player2.name)
            else:
                self.current_turn_changed.setText(self.player1.name)



    def current_turn(self, previous_player):
        # self.current_turn_func()
        self.previous_player = previous_player
        if self.previous_player is None:
            print(f'previous {previous_player}, self.player1.shape{self.player1.shape}, self.player2.shape{self.player2.shape}')
            if self.player1.shape == "X":
                return self.player1
            if self.player2.shape == "X":
                if self.player2.ai == True:
                    self.ai_move()
                    return
                return self.player2
        else:
            print(f'previous {previous_player.shape}, self.player1.shape{self.player1.shape}, self.player2.shape{self.player2.shape}')
            if self.previous_player.shape == self.player1.shape:
                if self.player2.ai == True:
                    self.ai_move()
                    return
                else:
                    return self.player2
            elif self.previous_player.shape == self.player2.shape:
                return self.player1

    def new_game_btn_clicked(self):
        try:
            self.timer.stop()
        except AttributeError:
            pass
        self.move_countdown.display(0)
        self.player1.shape, self.player2.shape = self.player2.shape, self.player1.shape
        self._init_board(self.size, (self.player1, self.player2))
        self.current_turn_func()


    def reset_game(self):
        self.timer.stop()
        self.move_countdown.display(0)
        for btn in self.btn_grp_board.buttons():
            btn.setEnabled(False)


    def update_lcd(self):
        self.player1_wins_counter.display(self.player1.counter_wins)
        self.player2_wins_counter.display(self.player2.counter_wins)

    def player_move(self, player):
        #todo timer/countdown depends on difficulty level
        """difficulty_level = self.player2.difficulty
        if difficulty_level:
            if difficulty_level == "1":
                seconds = 10
            if difficulty_level == "2":
                seconds = 7
            if difficulty_level == "3":
                seconds = 5
        """

    # depends on selected difficulty call different method responsibilities for AI moves
    def easy_level(self):
        # Check if AI could win in next move
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.push_list[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column].capture(self.player2.shape)
                self.control_state(self.player2, row, column)
                return
            else:
                self.push_list[row][column] = "-"
        # random choice from possible moves list, then call insert_char with that row/column
        position = random.choice(self.possible_moves)
        row, column = int(position[0]), int(position[1])
        self.push_list[row][column] = self.player2.shape
        self.board[row][column].capture(self.player2.shape)
        self.control_state(self.player2, row, column)
        return

    def intermediate_level(self):
        # Check if AI could win in next move, and do it
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.push_list[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column].capture(self.player2.shape)
                self.control_state(self.player2, row, column)
                return
            # Check if player could win in next move, and block them
            else:
                self.push_list[row][column] = self.player1.shape
                if self.is_win():
                    self.push_list[row][column] = self.player2.shape
                    self.board[row][column].capture(self.player2.shape)
                    self.control_state(self.player2, row, column)
                    return
                else:
                    self.push_list[row][column] = "-"

        # random choice from possible moves list, then call insert_char with that row/column
        position = random.choice(self.possible_moves)
        row, column = int(position[0]), int(position[1])
        self.push_list[row][column] = self.player2.shape
        self.board[row][column].capture(self.player2.shape)
        self.control_state(self.player2, row, column)
        return


    # depends on selected difficulty call different method responsibilities for AI moves
    def ai_move(self):
        if self.player2.difficulty == "Easy":
            self.sec = 10
            self.easy_level()

        elif self.player2.difficulty == "Intermediate":
            self.sec = 7
            self.intermediate_level()
        else:
            self.sec = 4
            self.hard_level()


    def control_state(self, player, row, column):
        print(self.possible_moves)
        print(f"current player in control state{player.shape}")
        # remove (row, column) from list of empty cells in the board
        print(f"row i column w control state przed usunięciem {(row, column)}")
        # check that after insertion is the end of the game
        if self.is_win(): # do poprawy informacja kto wygrywa
            self.reset_game()
            QMessageBox.information(self, "Game status", f"{player.name} WIN!")
            player.counter_wins += 1
            self.update_lcd()
            return
        if self.is_draw():
            self.reset_game()
            QMessageBox.information(self, "Game status", "DRAW!")
            return
        self.possible_moves.remove((row, column))
        print(len(self.possible_moves))
        self.current_turn(player)

    # CHECKS CURRENT STATES OF THE GAME
    def is_draw(self):
        for row in range(len(self.push_list)):
            for column in range(len(self.push_list[row])):
                if self.push_list[row][column] == "-":
                    return False
        return True

    def is_win(self):
        # transposition to check rows, then columns
        for new_board in [self.push_list, np.transpose(self.push_list)]:
            result = self.check_rows(new_board)
            if result:
                return result
        return self.check_diagonals()

    def check_rows(self, board):
        for row in board:
            print(f"set row: {set(row)}")
            if len(set(row)) == 1 and set(row) != {"-"}:
                pprint(self.push_list)
                return True
        return False

    def check_diagonals(self):
        # check diagonal ((0,0), (1,1), (2,2)....etc)
        check_one = set([self.push_list[i][i] for i in range(len(self.push_list))])
        print(f"check_one: {check_one}")
        if len(check_one) == 1 and check_one != {"-"}:
            pprint(self.push_list)
            return True
        # check diagonal (from last column in first row to last row and first column)
        check_two = set([self.push_list[i][len(self.push_list) - i - 1] for i in range(len(self.push_list))])
        print(f"check_two: {check_two}")
        if len(check_two) == 1 and check_two != {"-"}:
            pprint(self.push_list)
            return True
        return False


class DlgMain(QDialog, Ui_Dialog, Ui_tic_tac_toe_board):
    def __init__(self):
        super(DlgMain, self).__init__()
        self._init_ui()
        self.ai_btn.clicked.connect(self._event_opponent_choice_clicked)
        self.human_btn.clicked.connect(self._event_opponent_choice_clicked)
        self.start_game_btn.clicked.connect(self._main_menu)

    def _init_ui(self):
        self.setupUi(self)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())


    def _main_menu(self):
        self.difficulties = self.group_btns_levels.checkedButton().text()
        players = self._create_players(self.player1_name.text(), self.player2_name.text())
        self.board = Board(self.board_size.value(), players)
        self.board.show()


    def _create_players(self, player_name="Human1", player2_name="Human2"):
        shapes = ["X", "O"]
        if self.player1_name.text() == "":
            self.player1_name.setText("Player1")
        self.player1 = Player(name=self.player1_name.text(), shape=random.choice(shapes))
        # Remove selected shape from shapes list
        shapes.remove(self.player1.shape)
        if self.ai_btn.isChecked():
            self.player2 = Player(name="AI", shape=random.choice(shapes))
            self.player2.difficulty = self.difficulties
            self.player2.ai = True
        elif self.human_btn.isChecked():
            if self.player2_name.text() == "":
                self.player2_name.setText("Player2")
            self.player2 = Player(name=self.player2_name.text(), shape=random.choice(shapes))
        return (self.player1, self.player2)

    # Checks what opponent user choose and activate specific part of lower menu(depends on a choice)
    def _event_opponent_choice_clicked(self):
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