# board constants
BOARD_ROWS = 8
BOARD_COLS = 10

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
       
 
def clear_board(board):
    for r_id, row in enumerate(board):
        for c_id,col in enumerate(row):
            board[r_id][c_id] = " "

        
        
def draw():
    sketch_board[cursor[0]][cursor[1]] = "X"
        
        
def valid_move(r,c):
    if r >= 0 and r < BOARD_ROWS and c >= 0 and c < BOARD_COLS:
        return True
    else:
        print("Invalid move")
        return False       
        
    
def update_pos(r = cursor[0],c = cursor[1]) :
    print(r,c)
    if valid_move(r,c):
        cursor[0] = r
        cursor[1] = c
        if sketch_board[cursor[0]][cursor[1]] != "X":
            sketch_board[r][c] = "O"
    else:
       sketch_board[cursor[0]][cursor[1]] = "O"
    
        
def parse_cmd(cmd):
    pcmd = str.lower(cmd.strip())
    if pcmd == "quit":
        exit()
    elif pcmd == "clear":
        clear_board(sketch_board)
        
    #preemptive update sketch board to remove old cursor location  if not drawn on  
    if sketch_board[cursor[0]][cursor[1]] != "X":
        sketch_board[cursor[0]][cursor[1]] = " "
    
    if pcmd == "w":
        update_pos(cursor[0]-1, cursor[1])
    elif pcmd == "a":
        update_pos(cursor[0],cursor[1]-1)
    elif pcmd == "s":
        update_pos(cursor[0]+1, cursor[1])
    elif pcmd == "d":
        update_pos(cursor[0], cursor[1]+1)
    elif pcmd == "x":
        draw()
        
update_pos()
print_board(sketch_board)
while True:
    cmd = input("w - up; a - left; d - right; s - down; clear - clear board; quit - quit game: ")
    parse_cmd(cmd)
    print_board(sketch_board)
