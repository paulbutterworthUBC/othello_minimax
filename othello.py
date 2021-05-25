import numpy as np
import random
from copy import deepcopy

directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
initial_board = []
for i in range(0, 8):
    initial_board.append([0, 0, 0, 0, 0, 0, 0, 0])
initial_board[3][3] = "B"
initial_board[4][4] = "B"
initial_board[3][4] = "W"
initial_board[4][3] = "W"

class Reversi:
    def __init__(self):
        self.board = initial_board
        self.black_placements = [[3,3],[4,4]]
        self.white_placements = [[3,4],[4,3]]

    def print_board(self):
        for row in self.board:
            new_column = ""
            for column in row:
                if column in ["B", "W"]:
                    new_column += column + "  "
                else:
                    new_column += str(column) + "  "
            print(new_column)

    def available_moves(self, player):
        available_moves = []
        if player == "B":
            for tile in self.black_placements:
                for direction in directions:
                    available_moves += self.check_direction(tile, player, direction)
        if player == "W":
            for tile in self.white_placements:
                for direction in directions:
                    available_moves += self.check_direction(tile, player, direction)
        moves_no_dupes = []
        for move in available_moves:
            if move not in moves_no_dupes:
                moves_no_dupes.append(move)
        return moves_no_dupes

    #assumes that placement is valid (ie. in available_moves)
    def make_move(self, placement, player):
        self.board[placement[0]][placement[1]] = player
        if player == "B":
            self.black_placements.append(placement)
        if player == "W":
            self.white_placements.append(placement)
        matches = []
        for direction in directions:
            matches.append(self.check_line_direction(placement, player, direction))
        matches = [x for x in matches if (len(x) > 0)]
        for match in matches:
            self.change_line(placement, match, player)

    def can_make_move(self, player):
        return self.available_moves(player)

    def is_game_over(self):
        return not (self.can_make_move("B") and self.can_make_move("W"))

    def change_line(self, start, end, player):
        row_change = 0
        column_change = 0
        if end[0] - start[0] > 0:
            row_change = 1
        if end[0] - start[0] < 0:
            row_change = -1
        if end[1] - start[1] > 0:
            column_change = 1
        if end[1] - start[1] < 0:
            column_change = -1
        [row, column] = start
        row += row_change
        column += column_change
        while [row, column] != end:
            self.board[row][column] = player
            if player == "B":
                self.black_placements.append([row, column])
                self.white_placements.remove([row, column])
            if player == "W":
                self.white_placements.append([row, column])
                self.black_placements.remove([row, column])
            row += row_change
            column += column_change  

    def row_column_check(self, row, column, direction):
        row_max = -1
        column_max = -1
        if direction in ["SW", "S", "SE"]:
            row_max = 8
        if direction in ["SE", "E", "NE"]:
            column_max = 8
        return row != row_max and column != column_max

    #checks to make sure row/column index is not OOB
    def row_column_change(self, direction):
        [row_change, column_change] = [0,0]
        if direction in ["NW", "N", "NE"]:
            row_change = -1
        if direction in ["SW", "S", "SE"]:
            row_change = 1
        if direction in ["SW", "W", "NW"]:
            column_change = -1
        if direction in ["SE", "E", "NE"]:
            column_change = 1
        return [row_change, column_change]

    def check_direction(self, cord, player, direction):
        available = []
        [row, column] = cord
        row_column_change = self.row_column_change(direction)
        if self.row_column_check(row + row_column_change[0], column + row_column_change[1], direction):
            row += row_column_change[0]
            column += row_column_change[1]
            if player == "B":
                if self.board[row][column] == "W":
                    while self.row_column_check(row, column, direction):
                        if self.board[row][column] == "B":
                            break
                        elif self.board[row][column] == "W":
                            row += row_column_change[0]
                            column += row_column_change[1]
                            continue
                        elif self.board[row][column] == 0:
                            available.append([row, column])
                            break
            if player == "W":
                if self.board[row][column] == "B":
                    while self.row_column_check(row, column, direction):
                        if self.board[row][column] == "W":
                            break
                        elif self.board[row][column] == "B":
                            row += row_column_change[0]
                            column += row_column_change[1]
                            continue
                        elif self.board[row][column] == 0:
                            available.append([row, column])
                            break
        return available

    def check_line_direction(self, cord, player, direction):
        available = []
        [row, column] = cord
        row_column_change = self.row_column_change(direction)
        if self.row_column_check(row + row_column_change[0], column + row_column_change[1], direction):
            row += row_column_change[0]
            column += row_column_change[1]
            if player == "B":
                if self.board[row][column] == "W":
                    while self.row_column_check(row, column, direction):
                        if self.board[row][column] == "B":
                            return [row, column]
                        elif self.board[row][column] == "W":
                            row += row_column_change[0]
                            column += row_column_change[1]
                            continue
                        elif self.board[row][column] == 0:
                            break
            if player == "W":
                if self.board[row][column] == "B":
                    while self.row_column_check(row, column, direction):
                        if self.board[row][column] == "W":
                            return [row, column]
                        elif self.board[row][column] == "B":
                            row += row_column_change[0]
                            column += row_column_change[1]
                            continue
                        elif self.board[row][column] == 0:
                            break
        return available

    def who_won(self):
        black_count = len(self.black_placements)
        white_count = len(self.white_placements)
        if black_count > white_count:
            return 1
        elif black_count < white_count:
            return -1
        else:
            return 0

loop_count = 0
def minimax(board, is_maximizing, depth, alpha, beta):
    global loop_count
    loop_count += 1
    print(loop_count)
    if board.is_game_over() or depth == 0:
        return [board.who_won(), "", alpha, beta]
    best_move = ""
    if is_maximizing:
        best_value = -float("Inf")
        symbol = "B"
    else:
        best_value = float("Inf")
        symbol = "W"
    for move in board.available_moves(symbol):
        new_board = deepcopy(board)
        new_board.make_move(move, symbol)
        hypothetical_value = minimax(new_board, not is_maximizing, depth - 1, alpha, beta)[0]
        if is_maximizing == True and hypothetical_value > best_value:
            best_value = hypothetical_value
            best_move = move
            alpha = max(alpha, best_value)
        if is_maximizing == False and hypothetical_value < best_value:
            best_value = hypothetical_value
            best_move = move
            beta = min(best_value, beta)
        if alpha >= beta:
            break
    return [best_value, best_move, alpha, beta]

board = Reversi()
while not board.is_game_over():
    board.make_move(minimax(board, True, 6, -float("Inf"), float("Inf"))[1], "B")
    board.print_board()
    print("___________________________")
    if not board.is_game_over():
        board.make_move(minimax(board, False, 3, -float("Inf"), float("Inf"))[1], "W")
        board.print_board()
        print("___________________________")
print(board.who_won())

#depth = 3, W win
#depth = 4, B win
#depth = 5, W win