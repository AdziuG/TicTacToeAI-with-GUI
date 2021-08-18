import numpy as np
import random



class Player:
    def __init__(self, name, shape):
        self.name = str(name)
        self.shape = str(shape)
        self.counter = 0
        self.difficulty = ""
        self.ai = False

class Board:

    def __init__(self, size):
        self.size = size  # zrobić if, że musi być wiekszy lub rowny 3
        self.board = np.zeros(shape=(size, size), dtype="U10")
        self.possible_moves = []

    def create_board(self, size):
        for i in range(size):
            for j in range(size):
                self.possible_moves.append((i, j))
                print(self.possible_moves)
                self.board[i][j] = "-"


    # display board game
    def display_board(self):
        print(self.board)

    def create_players(self):
        shapes = ["X", "O"]
        self.player1 = Player(input("Enter your name"), random.choice(shapes))
        print("""
            Do you want to play with computer or human?
            1. Computer
            2. Human
        """)
        choice = input()

        # Remove selected shape from shapes list
        shapes.remove(self.player1.shape)
        while choice != "1" or choice != "2": #todo try, expect żeby nie pobierało innych wartości
            if choice == "1":
                self.player2 = Player(name="AI", shape=random.choice(shapes))
                self.player2.difficulty = self.difficulty_level()
                self.player2.ai = True
                return
            elif choice == "2":
                self.player2 = Player(input("Enter name"), random.choice(shapes))
                return


    # checks empty space on the board
    def is_free_space(self, row, column):
        if self.board[row][column] == "-":
            return True
        return False


    def is_draw(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[int(row)][int(column)] == "-":
                    return False
        return True

    def is_win(self, shape="-"):
        # transposition to check rows, then columns
        for new_board in [self.board, np.transpose(self.board)]:
            result = self.check_rows(new_board, {shape})
            if result:
                return result
        return self.check_diagonals({shape})

    def check_rows(self, board, shape):
        for row in board:
            if len(set(row)) == 1 and set(row) != {"-"}:
                return True
        return False

    def check_diagonals(self, shape):
        # check diagonal ((0,0), (1,1), (2,2)....etc)
        check_one = set([self.board[i][i] for i in range(len(self.board))])
        if len(check_one) == 1 and check_one != {"-"}:
            return True
        # check diagonal (from last column in first row to last row and first column)
        check_two = set([self.board[i][len(self.board) - i - 1] for i in range(len(self.board))])
        if len(check_two) == 1 and check_two != {"-"}:
            return True
        return False

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


    # choose difficulty level of the game at the beginning
    def difficulty_level(self):
        difficulty = ''
        while not (difficulty == '1' or difficulty == '2' or difficulty == '3'):
            print("Please enter a difficulty level:"
                  "1 - easy,"
                  "2 - intermediate,"
                  "3 - hard")
            difficulty = input()
        return difficulty

    # depends on selected difficulty call different method responsibilities for AI moves
    def ai_move(self):
        if self.player2.difficulty == "1":
            self.easy_level()
        if self.player2.difficulty == "2":
            self.intermediate_level()
        if self.player2.difficulty == "3":
            self.hard_level()

    #check and choose who have next move
    def current_turn(self):
        if self.player1.counter == self.player2.counter:
            if self.player1.shape == "X":
                self.player1.counter += 1
                self.player_move(self.player1)
            else:
                self.player2.counter += 1
                if self.player2.ai:
                    self.ai_move()
                else:
                    self.player_move(self.player2)
        else:
            if self.player1.shape == "O":
                self.player1.counter += 1
                self.player_move(self.player1)
            else:
                self.player2.counter += 1
                if self.player2.ai:
                    self.ai_move()
                else:
                    self.player_move(self.player2)

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

    def intermediate_level(self):
        # Check if AI could win in next move, and do it
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.board[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column] = "-"
                self.insert_char(self.player2.shape, row, column)
            self.board[row][column] = "-"

        # Check if player could win in next move, and block them
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.board[row][column] = self.player1.shape
            # if winning after this movie, clear this cell and call insert_char with that row/column indices
            if self.is_win():
                self.board[row][column] = "-"
                self.insert_char(self.player2.shape, row, column)
            self.board[row][column] = "-"

        # random choice from possible moves list, then call insert_char with that row/column
        position = random.choice(self.possible_moves)
        self.insert_char(self.player2.shape, int(position[0]), int(position[1]))

    def hard_level(self):
        # Check if AI could win in next move
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.board[row][column] = self.player2.shape
            if self.is_win():
                self.board[row][column] = "-"
                return self.insert_char(self.player2.shape, row, column)

            self.board[row][column] = "-"

        # Check if player could win in next move, and block them
        for position in self.possible_moves:
            row, column = int(position[0]), int(position[1])
            self.board[row][column] = self.player1.shape
            # if winning after this movie, clear this cell and call insert_char with that row/column indices
            if self.is_win():
                self.board[row][column] = "-"
                return self.insert_char(self.player2.shape, row, column)

            self.board[row][column] = "-"

        # take the center position if free
        if self.player1.counter == 0 or self.player2.counter == 0:
            position = self.possible_moves[len(self.possible_moves) // 2]
            return self.insert_char(self.player2.shape, int(position[0]), int(position[1]))

        # take one of the sides after 1st move
        if self.player2.counter == 1 or self.player1.counter == 1:
            getting_position = [position for position in self.possible_moves if position[0] == 0 if position[1] == self.size-1]
            position = random.choice(getting_position)
            return self.insert_char(self.player2.shape, int(position[0]), int(position[1]))

        # random choice from possible moves list, then call insert_char with that row/column
        position = random.choice(self.possible_moves)
        return self.insert_char(self.player2.shape, int(position[0]), int(position[1]))


board = Board(4)
board.create_board(4)
board.create_players()
board.display_board()
while not board.is_win() or not board.is_draw():
    board.current_turn()
