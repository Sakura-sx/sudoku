import os
import curses

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(True)

mistakes = 0
max_mistakes = 3

cursorpos = (0, 0)

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


solved_board = [[3, 7, 8, 1, 4, 5, 9, 6, 2],
                [4, 2, 9, 6, 7, 3, 1, 8, 5],
                [5, 6, 1, 2, 9, 8, 3, 7, 4],
                [1, 9, 6, 8, 2, 4, 7, 5, 3],
                [7, 4, 5, 9, 3, 6, 2, 1, 8],
                [8, 3, 2, 5, 1, 7, 4, 9, 6],
                [2, 5, 7, 3, 8, 1, 6, 4, 9],
                [9, 8, 4, 7, 6, 2, 5, 3, 1],
                [6, 1, 3, 4, 5, 9, 8, 2, 7]]

existing_numbers = [[False for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            existing_numbers[i][j] = True

curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

(y,x) = screen.getmaxyx()
if y < 31 or x < 51:
    screen.addstr(y//2, x//2-len(f"Screen is too small! (required: 31x51, current: {y}x{x})")//2, f"Screen is too small! (required: 31x51, current: {y}x{x})", curses.color_pair(6) | curses.A_BOLD)
    screen.addstr(y//2 + 1, x//2-22, "Please resize your window to at least 31x51!", curses.color_pair(2) | curses.A_BOLD)
    screen.addstr(y//2 + 2, x//2-14, "Press any key to continue...", curses.color_pair(2) | curses.A_BOLD)
    screen.refresh()
    screen.getch()
    curses.endwin()
    exit()


def new_game():
    global mistakes
    global max_mistakes
    global board
    global existing_numbers
    global cursorpos

    print_board()
    screen.addstr(f"Mistakes: {mistakes}/{max_mistakes}\n")
    screen.refresh()
    while True:
        key = screen.getch()
        if key == curses.KEY_UP:
            cursorpos = (max(0, cursorpos[0] - 1), cursorpos[1])
        elif key == curses.KEY_DOWN:
            cursorpos = (min(8, cursorpos[0] + 1), cursorpos[1])
        elif key == curses.KEY_LEFT:
            cursorpos = (cursorpos[0], max(0, cursorpos[1] - 1))
        elif key == curses.KEY_RIGHT:
            cursorpos = (cursorpos[0], min(8, cursorpos[1] + 1))
        elif key >= ord('0') and key <= ord('9'):
            if not existing_numbers[cursorpos[0]][cursorpos[1]]:
                board[cursorpos[0]][cursorpos[1]] = key - ord('0')
            if not validate_board():
                mistakes += 1
                board[cursorpos[0]][cursorpos[1]] = 0
        print_board()
        screen.addstr(f"Mistakes: {mistakes}/{max_mistakes}\n")
        if mistakes >= max_mistakes:
            screen.addstr("You lost! You made too many mistakes.\n")
            screen.addstr("Press any key to continue...\n")
            screen.getch()
            break
        if complete_board():
            screen.addstr("You won! You solved the puzzle.\n")
            screen.addstr("Press any key to continue...\n")
            screen.getch()
            break
        curses.napms(100)
    curses.endwin()

def print_board():
    screen.clear()
    screen.addstr("╔═" + "═" * 6 + "╦═" + "═" * 6 + "╦═" + "═" * 6 + "╗\n")
    
    cursor_value = board[cursorpos[0]][cursorpos[1]]
    
    for i in range(9):
        screen.addstr("║ ")
        for j in range(9):
            cell_value = board[i][j]
            display_char = str(cell_value) if cell_value != 0 else " "
            
            if i == cursorpos[0] and j == cursorpos[1]:
                screen.attron(curses.A_REVERSE)
                screen.addstr(display_char)
                screen.attroff(curses.A_REVERSE)
            elif cursor_value != 0 and cell_value == cursor_value:
                screen.addstr(display_char, curses.color_pair(4) | curses.A_BOLD)
            elif (cursorpos[0] == i or cursorpos[1] == j):
                if existing_numbers[i][j]:
                    screen.addstr(display_char, curses.color_pair(3))
                else:
                    if cell_value == 0:
                        screen.addstr(display_char, curses.color_pair(3))
                    else:
                        screen.addstr(display_char, curses.color_pair(3))
            elif existing_numbers[i][j]:
                screen.addstr(display_char, curses.color_pair(2))
            else:
                if cell_value == 0:
                    screen.addstr(display_char, curses.color_pair(2))
                else:
                    screen.addstr(display_char, curses.color_pair(1))
            
            if j % 3 == 2:
                screen.addstr(" ║")
            screen.addstr(" ")
        screen.addstr("\n")
        if i % 3 == 2 and i != 8:
            screen.addstr("╠═" + "═" * 6 + "╬═" + "═" * 6 + "╬═" + "═" * 6 + "╣\n")
        elif i == 8:
            screen.addstr("╚═" + "═" * 6 + "╩═" + "═" * 6 + "╩═" + "═" * 6 + "╝\n")
    screen.refresh()

def validate_board():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                if board[i][j] != solved_board[i][j]:
                    return False
    return True

def complete_board():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True


selected_option = 0
while True:
    screen.clear()
    screen.box()
    screen.addstr(y//2-3, x//2-9, "Welcome to Sudoku!", curses.color_pair(2) | curses.A_BOLD)
    if selected_option == 0:
        screen.addstr(y//2, x//2-7, "[ New Sudoku ]", curses.color_pair(4) | curses.A_BOLD)
    else:
        screen.addstr(y//2, x//2-5, "New Sudoku", curses.color_pair(2) | curses.A_BOLD)
    if selected_option == 1:
        screen.addstr(y//2 + 1, x//2-4, "[ Load ]", curses.color_pair(4) | curses.A_BOLD)
    else:
        screen.addstr(y//2 + 1, x//2-2, "Load", curses.color_pair(2) | curses.A_BOLD)
    if selected_option == 2:
        screen.addstr(y//2 + 2, x//2-4, "[ Exit ]", curses.color_pair(4) | curses.A_BOLD)
    else:
        screen.addstr(y//2 + 2, x//2-2, "Exit", curses.color_pair(2) | curses.A_BOLD)
    screen.refresh()
    key = screen.getch()
    if key == curses.KEY_UP:
        selected_option = (selected_option - 1) % 3
    elif key == curses.KEY_DOWN:
        selected_option = (selected_option + 1) % 3
    elif key == curses.KEY_ENTER or key == ord('\n'):
        if selected_option == 0:
            new_game()
        elif selected_option == 1:
            print("TODO")
        elif selected_option == 2:
            curses.endwin()
            exit()
    curses.napms(100)