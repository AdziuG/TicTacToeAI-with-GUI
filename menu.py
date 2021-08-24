import random
from PyQt5.QtWidgets import QDialog
from board_logic import Board
from board_ui import Ui_tic_tac_toe_board
from main_menu_ui import Ui_Dialog
import dark_orange


class DlgMain(QDialog, Ui_Dialog, Ui_tic_tac_toe_board):
    """
    This class creates main menu:
    1. Initialize GUI (main menu)
    2. Creates signal/slot( if ai or human radio button is checked)
    3. Creates start game btn and signal/slot which initialize Tic Tac Toe board of the game
    """
    def __init__(self):
        super(DlgMain, self).__init__()
        self._init_ui()
        self.ai_btn.clicked.connect(self._event_opponent_choice_clicked)
        self.human_btn.clicked.connect(self._event_opponent_choice_clicked)
        self.difficulties = self.group_btns_levels.checkedButton().text()
        self.start_game_btn.clicked.connect(self._main_menu)

    def _init_ui(self):
        """ Loading GUI from main_menu_ui.py and stylesheet from dark_orange folder """
        self.setupUi(self)
        with open("dark_orange/style.qss", 'r') as style:
            self.setStyleSheet(style.read())

    def _main_menu(self):
        """
        1. Create players and keep them in players variable.
        2. Create instance of Board class (with attributes inputted by user in graphical menu).
        3. Initialize 2nd window with board of the game
        """
        players = self._create_players(self.player1_name.text(), self.player2_name.text())
        self.board = Board(self.board_size.value(), players)
        self.board.show()

    def _event_opponent_choice_clicked(self):
        """
        Checks if radio button is clicked (AI or Human),
        activate specific part of lower menu in GUI(depends on a choice)
        """
        rbt = self.sender()  # rbt keeps information about selected button.
        if rbt.text() == "AI":  # If AI radio button is active:
            self.ai_difficulty_gbtns.setEnabled(True)  # Enabled group with radio buttons with AI difficulty levels.
            self.player2_name.setEnabled(False)  # Disabled QLineEdit with 2nd player name.
            self.player2_label.setEnabled(False)  # Disabled QLabel for QLineEdit.
        elif rbt.text() == "Human":  # The opposite situation than above
            self.player2_name.setEnabled(True)
            self.player2_label.setEnabled(True)
            self.ai_difficulty_gbtns.setEnabled(False)
        return rbt.text()

    def _create_players(self, player1_name, player2_name):
        """
        This method creates players using class Player and gathered selected data.
        Parameters player1_name, player2_name are from forms in GUI which is fill in by users
        """
        shapes = ["X", "O"]
        if player1_name == "":
            player1_name = "Player 1"
        self.player1 = Player(name=player1_name, shape=random.choice(shapes))  # Creates 1st player (it's always user)
        shapes.remove(self.player1.shape)  # Remove selected shape from shapes list
        if self.ai_btn.isChecked():  # If user checked radio button "AI" in GUI
            self.player2 = Player(name="AI", shape=random.choice(shapes))
            self.player2.difficulty = self.group_btns_levels.checkedButton().text()  # Additional attribute to verify what difficulties was chosen.
            self.player2.ai = True  # Additional attribute to verify if 2nd player is AI
        elif self.human_btn.isChecked():  # If user checked radio button "Human" in GUI
            if player2_name == "":
                player2_name = "Player 2"
            self.player2 = Player(name=player2_name, shape=random.choice(shapes))
        return self.player1, self.player2


class Player(Ui_tic_tac_toe_board):
    # This class is using to create players

    def __init__(self, name, shape):
        """Create new instance of player with specific attributes"""
        self.name = str(name)
        self.shape = str(shape)  # X or O
        self.counter_wins = 0  # counts winning games
        self.difficulty = ""  # Additional attribute to verify what difficulties was choose.
        self.ai = False  # Additional attribute to verify if 2nd player is AI.