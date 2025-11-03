import os

board = [[0 for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        board[i][j] = 0

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
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
print_board()