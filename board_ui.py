# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'board_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tic_tac_toe_board(object):
    def setupUi(self, tic_tac_toe_board):
        tic_tac_toe_board.setObjectName("tic_tac_toe_board")
        tic_tac_toe_board.resize(813, 826)
        self.verticalLayoutWidget = QtWidgets.QWidget(tic_tac_toe_board)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 40, 681, 671))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.board_main_ly = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.board_main_ly.setContentsMargins(0, 0, 0, 0)
        self.board_main_ly.setObjectName("board_main_ly")
        self.widget_3 = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widget_3.setObjectName("widget_3")
        self.gridLayoutWidget = QtWidgets.QWidget(self.widget_3)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 681, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.ttt_board = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.ttt_board.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.ttt_board.setContentsMargins(0, 1, 0, 1)
        self.ttt_board.setObjectName("ttt_board")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget_3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 450, 679, 221))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.lower_menu = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.lower_menu.setContentsMargins(0, 0, 0, 0)
        self.lower_menu.setObjectName("lower_menu")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.player1_counter = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.player1_counter.setObjectName("player1_counter")
        self.player1_wins_counter = QtWidgets.QLCDNumber(self.player1_counter)
        self.player1_wins_counter.setGeometry(QtCore.QRect(100, 30, 111, 51))
        self.player1_wins_counter.setObjectName("player1_wins_counter")
        self.player1_name_counter = QtWidgets.QLabel(self.player1_counter)
        self.player1_name_counter.setGeometry(QtCore.QRect(20, 10, 49, 16))
        self.player1_name_counter.setObjectName("player1_name_counter")
        self.verticalLayout_2.addWidget(self.player1_counter)
        self.player2_counter = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.player2_counter.setObjectName("player2_counter")
        self.player2_wins_counter = QtWidgets.QLCDNumber(self.player2_counter)
        self.player2_wins_counter.setGeometry(QtCore.QRect(100, 30, 111, 51))
        self.player2_wins_counter.setObjectName("player2_wins_counter")
        self.player2_name_counter = QtWidgets.QLabel(self.player2_counter)
        self.player2_name_counter.setGeometry(QtCore.QRect(20, 10, 49, 16))
        self.player2_name_counter.setObjectName("player2_name_counter")
        self.verticalLayout_2.addWidget(self.player2_counter)
        self.lower_menu.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.new_game_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_game_btn.sizePolicy().hasHeightForWidth())
        self.new_game_btn.setSizePolicy(sizePolicy)
        self.new_game_btn.setObjectName("new_game_btn")
        self.verticalLayout_3.addWidget(self.new_game_btn)
        self.exit_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_btn.sizePolicy().hasHeightForWidth())
        self.exit_btn.setSizePolicy(sizePolicy)
        self.exit_btn.setObjectName("exit_btn")
        self.verticalLayout_3.addWidget(self.exit_btn)
        self.history_movements = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.history_movements.setObjectName("history_movements")
        self.verticalLayout_3.addWidget(self.history_movements)
        self.lower_menu.addLayout(self.verticalLayout_3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.move_countdown = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.move_countdown.setObjectName("move_countdown")
        self.verticalLayout.addWidget(self.move_countdown)
        self.gridLayout_3.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.current_turn_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.current_turn_label.setObjectName("current_turn_label")
        self.gridLayout_2.addWidget(self.current_turn_label, 1, 0, 1, 1)
        self.remaining_time_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.remaining_time_label.setObjectName("remaining_time_label")
        self.gridLayout_2.addWidget(self.remaining_time_label, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.lower_menu.addLayout(self.gridLayout_3)
        self.board_main_ly.addWidget(self.widget_3)
        self.board_main_ly.setStretch(0, 2)

        self.retranslateUi(tic_tac_toe_board)
        QtCore.QMetaObject.connectSlotsByName(tic_tac_toe_board)

    def retranslateUi(self, tic_tac_toe_board):
        _translate = QtCore.QCoreApplication.translate
        tic_tac_toe_board.setWindowTitle(_translate("tic_tac_toe_board", "Board"))
        self.player1_name_counter.setText(_translate("tic_tac_toe_board", "PLAYER 1"))
        self.player2_name_counter.setText(_translate("tic_tac_toe_board", "PLAYER 2"))
        self.new_game_btn.setText(_translate("tic_tac_toe_board", "NEW GAME"))
        self.exit_btn.setText(_translate("tic_tac_toe_board", "EXIT"))
        self.history_movements.setText(_translate("tic_tac_toe_board", "HISTORY"))
        self.current_turn_label.setText(_translate("tic_tac_toe_board", "CURRENT TURN: PLAYER"))
        self.remaining_time_label.setText(_translate("tic_tac_toe_board", "REMAINING TIME FOR YOUR MOVE:"))
