BOARD_ROWS = 8
BOARD_COLS = 8
sketch_board = [[" " for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)]
cursor = [0,0]
        
def print_board(board):
    for r_id, row in enumerate(board):
        if r_id == 0:
            [print(f"   {i}", end = " ") if i ==0 else print(f"{i} ", end = "") for i in range(BOARD_COLS)]
            print("")
        print(f"{r_id}.", end= " ")   
        for c_id,col in enumerate(row):
            print(col, end = " ")
        print("")
        
        
def draw_pos(r,c):
    sketch_board[cursor[0]][cursor[1]] = "X"
    
def valid_move(val):
    if val < BOARD_ROWS and val < BOARD_COLS:
        return
    
def reset_board(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            print(type(col))
            board[row][col] = " "
    
def parse_cmd(cmd):
    if str.lower(cmd) == "clear":
        reset_board(sketch_board) 
    elif str.lower(cmd) == "exit":
        exit()
    elif str.lower(cmd) == "l":
        valid_move(cursor[1]-1)
        cursor[1] -= 1
    elif str.lower(cmd) == "d":
        valid_move(cursor[0]+1)
        cursor[0] += 1
    elif str.lower(cmd) == "r":
        valid_move(cursor[1]+1)
        cursor[1] += 1
    elif str.lower(cmd) == "u":
        valid_move(cursor[0]-1)
        cursor[0] -= 1
    elif str.lower(cmd) == "w":
        draw_pos(cursor[0], cursor[1])
    else:
        print("Invalid command")
       
            
      
print_board(sketch_board)
while True:
    usr_input = input("Please enter a coordinate in the row, column fashion <x,x>. An X will appear at that location:\n")
    parse_cmd(usr_input)
    print_board(sketch_board)
        
        
