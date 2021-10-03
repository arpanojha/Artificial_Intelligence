# skeleton code credits to CS551 course

import random

# default is a 4x4 board -- you can change this
ROWS = 4
COLS = ROWS

### these are helper functions
def transpose_board(board):
    return [list(col) for col in zip(*board)]

def is_any_row_full(board):
    return ["x"] * COLS in board

def is_any_col_full(board):
    return ["x"] * COLS in transpose_board(board)

def is_any_diag_full(board):
    return is_any_row_full([[board[i][i] for i in range(0,ROWS)], [board[i][COLS-i-1] for i in range(0,ROWS)]])

def board_to_string(board):
    return "  " + " ".join([str(b) for b in range(0,COLS)]) + "\n" + \
        "\n".join([chr(r+ord('a')) + " " + " ".join(board[r]) for r in range(0,ROWS)])

### check if the current board has any row, col, or diag complete
def check_win(board):
    return is_any_row_full(board) or is_any_col_full(board) or is_any_diag_full(board)

### add a piece to the board, returning a new copy of the board (not updating existing board)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + ["x",] + board[row][col+1:]] + board[row+1:]

def get_valid_x_y(board):
    valid_moves=[]
    for i in range(0,ROWS):
        for j in range(0,COLS):
            if board[i][j]!='x':
                valid_moves.append((i,j))
    return valid_moves

def successors(board):
    valid_moves=get_valid_x_y(board)
    fringe_successor=[]
    for (i,j) in valid_moves:
        fringe_successor.append(add_piece(board, i, j))
    return fringe_successor


### code to get a human-entered move
def get_human_move(board):
    move = input('Please enter where you want to place a tile (in a format like a1): ')
    (r, c) = ((ord(move[0]) - ord('a')), int(move[1]))
    while((not (0 <= r < ROWS and 0 <= c <= COLS)) or board[r][c] == 'x'):
        print('Invalid move!')
        move = input('Please enter where you want to place a tile (in a format like a1): ')
        (r, c) = ((ord(move[0]) - ord('a')), int(move[1]))

    return (r,c)

def max_value(board,depth):
    m=[]
    depth-=1
    if check_win(board):
   #     print("max won ",board_to_string(board))
        return 1
    else:
        if depth ==0:
            return 0
        for suc in successors(board):
            k=min_value(suc,depth)
            m.append(k)
            if k==1:
                return 1
        return max(m)


def min_value(board,depth):
    m=[]
    depth-=1
    if check_win(board):
   #     print("min won ",board_to_string(board))
        return -1
    else:
        if depth==0:
            return 0
        for suc in successors(board):
            k=max_value(suc,depth)
            m.append(k)
            if k==-1:
                return -1
        return min(m)


def r_c_next(board,successor):
    for i in range(0,ROWS):
        for j in range(0,COLS):
            if board[i][j]=='.' and successor[i][j]=='x':
                return (i,j)

def minimax_decision(board):
    if check_win(board):
        return board
    k=successors(board)
    fringe=[]
    for i in k:
        val=min_value(i,7)
        #print(val)
        fringe.append([i,val])
    for [i,val] in fringe:
        print(board_to_string(i),val)
        if val==1:
            q=r_c_next(board,i)
            print(q)
            return q

    (r,c) = (random.randrange(0,ROWS), random.randrange(0,COLS))
    while board[r][c] == 'x':
        (r,c) = (random.randrange(0,ROWS), random.randrange(0,COLS))
    return (r,c)

### code to get an AI move
# for right now, this code just returns a random move.
# This is where you'll want to implement minimax!!
#
def get_ai_move(board):
#    for k in fringe:
#        print(board_to_string(k))
    print("AI board:")
    #print(board_to_string(minimax_decision(board)))

    return minimax_decision(board)


### Main program!

# create initial empty board
board = [ ["."] * COLS for i in range(0, ROWS) ]
print(board_to_string(board))

while True:
    (r,c) = get_human_move(board)
    board = add_piece(board, r, c)
    print("-- New board after human move:\n" + board_to_string(board))
    if(check_win(board)):
        print("AI won!!")
        break

    (r,c) = get_ai_move(board)
    board = add_piece(board, r, c)
    print("-- New board after AI move:\n" + board_to_string(board))
    if(check_win(board)):
        print("Human won!!")
        break
