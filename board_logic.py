import functools
import random
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QButtonGroup, QMessageBox, QPushButton
from board_ui import Ui_tic_tac_toe_board


class Board(QDialog, Ui_tic_tac_toe_board):
    # The class where method creates and control all logic in the game.

    def __init__(self, size, players):
        super(Board, self).__init__()
        self._init_ui(players)
        self._init_btns()
        self._init_board(size, players)  # start game

    def _init_ui(self, players):
        """ Loading GUI from board_ui.py and stylesheet from dark_orange folder
            Fill in labels with players name
         """
        self.setupUi(self)
        self.player1_name_counter.setText(players[0].name)
        self.player2_name_counter.setText(players[1].name)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())

    def _init_btns(self):
        self.exit_btn.clicked.connect(self.exit_board)  # make connections between exit_btn and slot func
        self.new_game_btn.clicked.connect(self.new_game_btn_clicked)  # make connections between exit_btn and slot func
        self.btn_grp_board = QButtonGroup()  # creates QButtonGroup where are added QPushButton from board of the game.

    def _init_board(self, size, players):
        """
        Method initializes game logic and beginning state of the game.
        :param size: size of the board of the game. Passed from DlgMain class.
        :param players: tuple contains 2 objects of Player class. Passed from DlgMain class.
        """
        self.size = size  # size of the board of the game
        self.board = np.zeros(shape=(size, size), dtype=object)  # create array which store buttons (in board of the game)
        # The array which store game state and represents situation on the board of the game. Use for control state of the game
        self.push_list = np.zeros(shape=(size, size), dtype="str")
        self.possible_moves = []  # position (row, column) of cells which are still empty (not occupied by any of player)
        self.player1 = players[0]  # instance of Player class. Passed from DlgMain class
        self.player2 = players[1]  # instance of Player class Passed from DlgMain class
        self.create_board(size)
        self.sec = 7  # set time for move.
        self.previous_player = None  # store information what player made moves before.
        self.current_turn(None)  # start game
        self.current_turn_label_changer()  # display what player start game(player who has "X" always start game)

    def create_board(self, size):
        """
        Method creates board iterates through every single cell in the board.
        1. Appends cell position(row, column) to list which store empty(free) cell on the board (possible_moves).
        2. Use every single cell as instances of TicTacToeCell(create button - inherited from QPushButton,
            param: i=row, j=column)
        3. Add each button to QButtonGroup
        4. Set cell in push_list as empty cell (symbol "-" represents empty cell)
        5,6. Made signal/slot connection.
        7. Add button (created in step 2) to layout ttt_board which displaying board game.
        :param size: size of the board selected by user in main menu
        """
        for i in range(size):
            for j in range(size):
                self.possible_moves.append((i, j))  # 1
                self.board[i][j] = TicTacToeCell(i, j)  # 2
                self.btn_grp_board.addButton(self.board[i][j])  # 3
                self.push_list[i][j] = "-"  # 4
                self.board[i][j].clicked.connect(functools.partial(self.button_clicked, i, j))  # 5
                self.board[i][j].clicked.connect(self.current_turn_label_changer)  # 6
                self.ttt_board.addWidget(self.board[i][j], i, j)  # 7

    # SLOT FUNCTIONS

    def exit_board(self):
        """
        Method stops timer and close second window (board of the game) and return to main menu of app.
        Slot function connected with exit_btn which is displaying below board of the game.
        When button is clicked then method is called.
        """
        try:
            self.timer.stop()
            self.close()
        except AttributeError:
            self.close()

    def button_clicked(self, row, col):
        """
        Slot function connected with buttons in board game.
        When QPushButton is clicked on the board then call this method
        :param row: clicked row by user, needed for called another method within this func
        :param col: clicked column by user, needed for called another method within this func
        """
        try:
            if not self.player2.ai:  # if player1 and player2 are both user then set time for move in 5sec in self.sec
                self.sec = 5
            if self.timer.isActive():  # if timer is active then restart timer from beginning (using start() func)
                self.timer.start()
            else:
                self.create_timer()  # if instance does not exist then called method which create it.
        except AttributeError:
            self.create_timer()
        player = self.current_turn(self.previous_player)  # Set what player should make move on the board.
        button = self.sender()  # from what button got signal
        button.capture(player.shape)
        self.push_list[row][col] = player.shape  # Replace empty cell by shape of current player.
        self.control_state(player, row, col)

    def new_game_btn_clicked(self):
        """This method is connected with new_game_btn. When button is clicked then this method is called."""
        # Try/except is used to catch AttributeError when instance's not created yet.
        try:
            self.timer.stop()  # Instance of class QTimer() is stopped.
        except AttributeError:
            pass
        self.move_countdown.display(0)  # sets countdown lcd timer on value = 0
        self.player1.shape, self.player2.shape = self.player2.shape, self.player1.shape  # Replace shapes for next round.
        self._init_board(self.size, (self.player1, self.player2))  # Initialize board of the game but we keep the same settings.
        self.current_turn_label_changer()  # Sets label which display who should make a move.

    def reset_game(self):
        """
        Method stops countdown timer, and setting it on value 0.
        After that disables all button on the board
        """
        self.timer.stop()
        self.move_countdown.display(0)
        for btn in self.btn_grp_board.buttons():
            btn.setEnabled(False)

    # MANAGES TIMER

    def create_timer(self):
        """
            Method called when button (QPushButton) on the board is clicked.
            1. Creates instance object of QTimer class
            2. Makes connection with timeout(signal) and slot func - self.evt_update_timer
            and set interval to call method every single second till self.sec = 0.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.evt_update_timer)
        self.timer.setInterval(950)  # 1000ms = 1s
        self.timer.start()

    def evt_update_timer(self):
        """Slot function connected with countdown timer (QTimer object).
            Every single interval called method subtract 1 sec from self.set.
            If self.sec == 0
        """
        self.sec -= 1
        self.move_countdown.display(self.sec)
        if self.sec == 0:
            self.evt_finished_timer(self.previous_player)

    def evt_finished_timer(self, player):
        """
        Method called from slot function evt_update_timer. Method is called when time in countdown timer is over.
        :param player: instance of the player who had the previous move.
        If player is None (at the very beginning of the game) display popup with specific information
        In any other situation if time is over player who has current move lost and 1 win goes to opponent
        """
        if player is None:
            QMessageBox.information(self, "Game status", "Game Over!\nNobody wins because only one player got move")
        else:
            QMessageBox.information(self, "Game status", f"Time for move is over!\n{player.name} WIN!")
            player.counter_wins += 1  # increase opponent's winnings counter
        self.update_lcd()
        self.reset_game()

    # UPDATE LABEL IN GUI

    def update_lcd(self):
        """ Update lcd counter (displaying in GUI) after every round. If player wins then this number increase """
        self.player1_wins_counter.display(self.player1.counter_wins)
        self.player2_wins_counter.display(self.player2.counter_wins)

    def current_turn_label_changer(self):
        """
        It's slot function connected with button on the board game.
        Method sets new text into label displaying in GUI.
        It's important to know who need to make next move.
        """
        # When previous_player is None then try/except catch this error and force to start player who drawn "X" shape.
        # Logic the same in "current_turn" method.
        try:
            if self.previous_player == self.player1:
                self.current_turn_changed.setText(self.player2.name)
            elif self.previous_player == self.player2:
                self.current_turn_changed.setText(self.player1.name)
            else:
                if self.player2.shape == "X":
                    self.current_turn_changed.setText(self.player2.name)
                else:
                    self.current_turn_changed.setText(self.player1.name)
        except AttributeError:
            if self.player2.name == "X":
                self.current_turn_changed.setText(self.player2.name)
            else:
                self.current_turn_changed.setText(self.player1.name)

    # CONTROL STATE OF THE BOARD AND GAME STATUS

    def current_turn(self, previous_player):
        """
        Method manages current turn(movement). First call of this method is from __init__ of the board with arg: None.
        :param previous_player: copy of instance player who already made his move.
        :return: instance of player who will make next move.
        If player is AI, then will call method which control AI movements and logic.
        """
        self.previous_player = previous_player
        if self.previous_player is None:  # previous player is None when method is called first time.
            # Player who draw "X" makes first move.
            if self.player1.shape == "X":
                return self.player1
            if self.player2.shape == "X":
                if self.player2.ai:
                    self.ai_move()
                    return
                return self.player2
        else:  # after first movements, when previous player is known this part of code is called.
            if self.previous_player.shape == self.player1.shape:
                if self.player2.ai:
                    self.ai_move()
                    return
                else:
                    return self.player2
            elif self.previous_player.shape == self.player2.shape:
                return self.player1

    def control_state(self, player, row, column):
        """
        This method is responsible for control state of the board of the game. If is_win and is_draw are False then
        remove selected row and column from empty cells list. After that we call method for next turn(move).
        :param player:  player whose made already movement.
        :param row: chosen row (by player)
        :param column: chosen row (by player)
        """
        # Check that after movement(on the board game) is the end of the game.
        if self.is_win():  # If sb wins:
            self.reset_game()  # Call method responsible for clear board of the game
            QMessageBox.information(self, "Game status", f"{player.name} WIN!")  # Display popup with results.
            player.counter_wins += 1  # add win to counter_wins attribution in player instance.
            self.update_lcd()  # update gui information about number of winners.
            return
        if self.is_draw():
            self.reset_game()  # Call method responsibilities for clear board of the game.
            QMessageBox.information(self, "Game status", "DRAW!")  # Display popup with info about draw.
            return
        self.possible_moves.remove((row, column))  # Remove (row, column) from list of empty cells in the board.
        self.current_turn(player)  # Call method responsible for control what player will make another move.

    def is_win(self):
        """
        Transposition to check rows, then columns and return True or False. If return True then finish game.
        Push_list was created for control game logic and current events. It's a copy of current situation in GUI board.
        """
        for new_board in [self.push_list, np.transpose(self.push_list)]:
            result = self.check_rows(new_board)
            if result:
                return result
        # Check diagonals and return True or False
        return self.check_diagonals()

    def check_rows(self, board):
        # Iterates through board and if
        for row in board:
            # Check if exists only one shape(X or O) in row and symbol can't be "-".
            # Symbol "-" represents empty cell in the board of the game.
            if len(set(row)) == 1 and set(row) != {"-"}:
                return True
        return False

    def check_diagonals(self):
        # Check diagonal ((0,0), (1,1), (2,2)....etc)
        check_one = set([self.push_list[i][i] for i in range(len(self.push_list))])
        # Check if exists only one shape(X or O) in first diagonal and symbol there can't be "-".
        # Symbol "-" represents empty cell in the board of the game.
        if len(check_one) == 1 and check_one != {"-"}:
            return True
        # check diagonal (from last column in first row to last row and first column)
        check_two = set([self.push_list[i][len(self.push_list) - i - 1] for i in range(len(self.push_list))])
        # Check if exists only one shape(X or O) in second diagonal and symbol there can't be "-".
        # Symbol "-" represents empty cell in the board of the game.
        if len(check_two) == 1 and check_two != {"-"}:
            return True
        return False

    def is_draw(self):
        """Checks existing empty cells. If not, then return True and finish game."""
        for row in range(len(self.push_list)):
            for column in range(len(self.push_list[row])):
                if self.push_list[row][column] == "-":
                    return False
        return True

    # AI - CONTROL MOVEMENTS AND LOGIC

    def ai_move(self):
        """
        Depends on selected difficulty (at the beginning of the game)
        calls different method responsible for AI moves
        """
        if self.player2.difficulty == "Easy":
            self.sec = 10  # 10secs - set time for player(user) move
            self.easy_level()

        elif self.player2.difficulty == "Intermediate":
            self.sec = 7  # 7secs - set time for player(user) move
            self.intermediate_level()

        elif self.player2.difficulty == "Hard":
            self.sec = 3  # 3secs - set time for player(user) move
            self.intermediate_level()

    def easy_level(self):
        """
        1. Iterates through empty cells on the board,
        2. Fill in empty cell for shape of AI and check if AI could win in this move.
        3. If yes then call method to display this move on board
            and call method responsible for control state of the board.
        4. If no then empty this cell and choose random cells calling method random_move.
        """
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.push_list[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column].capture(self.player2.shape)  # Responsible for display move on the GUI board
                self.control_state(self.player2, row, column)  # Responsible for control state of the board.
                return
            else:
                self.push_list[row][column] = "-"
        self.random_move()  # Method responsible for random moves.

    def intermediate_level(self):
        """
        1. Iterates through empty cells on the board,
        2. Fill in empty cell for shape of AI and check if AI could win in this move.
        3. If yes then call method to display this move on board
            and call method responsible for control state of the board.
        4. If no then check if player 1 could win and block cell cause this winning.
        """
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
        self.random_move()  # Method responsible for random moves.

    def random_move(self):
        """Makes random move by AI"""
        position = random.choice(self.possible_moves)  # Choose random empty cells.
        row, column = int(position[0]), int(position[1])
        self.push_list[row][column] = self.player2.shape  # Replace empty cell by shape of player 2.
        self.board[row][column].capture(self.player2.shape)  # Responsible for display move on the GUI board
        self.control_state(self.player2, row, column)  # Responsible for control state of the board.
        return


class TicTacToeCell(QPushButton):
    # The class responsible for behaviour of QPushButton in the board of the game.

    def __init__(self, row, column):
        super().__init__()
        self.text = ''
        # Size of the button adjust and depends on size of the board.
        self.size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.size.setHorizontalStretch(0)
        self.size.setVerticalStretch(0)
        self.size.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.size)
        self.row = row  # store information what row has object and where is in the board.
        self.column = column  # store information what column has object and where is in the board.

    def captured(self):
        return self.text

    def capture(self, shape):
        """
        This method sets shape in the occupied button and change his status on disabled.
        :param shape: passed shape of the player who occupy this cell/button
        """
        self.text = shape
        self.setText(shape)
        self.setEnabled(False)

    def reset(self):
        """
        This method restores buttons(in the board) to default value.
        :return:
        """
        self.text = ''
        self.setText(self.text)
        self.setEnabled(True)

    def __repr__(self):
        return f'[{self.text}]'