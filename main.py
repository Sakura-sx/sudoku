import os

board = [[0 for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        board[i][j] = 0

board = [[0, 0, 8, 1, 4, 0, 9, 0, 2],
         [0, 2, 0, 6, 7, 3, 0, 0, 0],
         [0, 6, 1, 2, 0, 0, 3, 7, 4],
         [1, 9, 0, 0, 2, 4, 0, 5, 3],
         [7, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 3, 2, 0, 0, 0, 0, 9, 0],
         [0, 0, 7, 3, 8, 0, 6, 0, 9],
         [9, 0, 0, 7, 0, 0, 5, 0, 1],
         [6, 1, 0, 0, 0, 0, 0, 2, 0]]

def print_board():
    board_str = ""
    board_str += "╔═" + "═" * 6 + "╦═" + "═" * 6 + "╦═" + "═" * 6 + "╗\n"
    for i in range(9):
        board_str += "║ "
        for j in range(9):
            board_str += f"{board[i][j]}"
            if j % 3 == 2:
                board_str += " ║"
            board_str += " "
        board_str += "\n"
        if i % 3 == 2 and i != 8:
            board_str += "╠═" + "═" * 6 + "╬═" + "═" * 6 + "╬═" + "═" * 6 + "╣\n"
        elif i == 8:
            board_str += "╚═" + "═" * 6 + "╩═" + "═" * 6 + "╩═" + "═" * 6 + "╝\n"
    print(board_str)

def validate_board():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                for k in range(9):
                    if board[i][k] == board[i][j] and k != j:
                        return False
                    if board[k][j] == board[i][j] and k != i:
                        return False
                    if board[i//3*3+k//3][j//3*3+k%3] == board[i][j] and k != i%3*3+j%3:
                        return False
    return True

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
print_board()

if validate_board():
    print("The board is valid")
else:
    print("The board is invalid")


while True:
