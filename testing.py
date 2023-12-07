import numpy as np 
import json

board = np.array([(0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,0,0,0,0,0,0,0,0,0),
                  (0,3,4,0,0,8,7,0,0,0),
                  (0,3,2,6,8,9,3,9,8,6),
                  (1,3,2,6,8,9,3,9,8,6)], dtype=np.int8)

def first_nonzero(board):
    invalid_val=-1
    mask = board!=0
    row = np.array(np.where(mask.any(axis=0), mask.argmax(axis=0), invalid_val), dtype=np.int8)
    # column = np.array(np.where(mask.any(axis=1), mask.argmax(axis=1), invalid_val), dtype=np.int8)
    # column = np.delete(column, np.argwhere(column==-1))
    # row = np.delete(row, np.argwhere(row==-1))
    return row
# return [(row[len(row)-i-1], column[i]) for i in range(len(row)-1, -1, -1)]

def drop_block(board, column, num):
    return
# print(first_nonzero(board)[column])
    # coord = first_nonzero(board)[column]
    # board[coord[0]-1][coord[1]] = num
    # print(board)

def print_coord(coords, board):
    for coord in coords:
        print(board[coord[0]][coord[1]], end=" ")
    print()
    for coord in coords:
        print(board[coord[0]-1][coord[1]], end=" ")
    print()

def move_ele_to_right(board):
    for row_num, lst in enumerate(board):
        lst = lst[lst != 0]
        for _ in range(0, len(board[row_num])-len(lst)):
            lst = np.insert(lst, 0, 0)
        board[row_num] = lst
    # print()

def combine_surrounding(board, row, col):
    # print(board[row][col])
    # result = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
                if (0 <= row+dx <= len(board)-1) and (0 <= col+dy <= len(board[0])-1):
                    if board[row+dx][col+dy] == board[row][col]:
                        if board[row+dx][col+dy]+1 == 10:
                            board[row+dx][col+dy] = 0
                            board[row][col] = 0
                        else:
                            if row+col > row+dx+col+dy:
                                board[row][col] += 1
                                board[row+dx][col+dy] = 0
                            else:
                                board[row][col] = 0
                                board[row+dx][col+dy] += 1
                    # result.append(board[row+dx][col+dy])
                    # print((row+dx, col+dy))
    # print(result)
    return

def get_dup_in_lst(lst):
    res = []
    for i in range(1, len(lst)):
        if lst[i-1] != 0 and lst[i] != 0:
            if lst[i-1] == lst[i]:
                res.append(i)
    return res

def check_board_for_matches(board):
    row_count, col_count = 0, 0
    # Check row
    for row_num, row in enumerate(board):
        print(row)
        dup_col_num = get_dup_in_lst(row)
        if len(dup_col_num):
            for col_num in dup_col_num:
                combine_surrounding(board, row_num, col_num)
                # move_ele_to_right()
        else:
            row_count += 1
    # print()
    # Check column
    for col_num, col in enumerate(board.T):
        dup_row_num = get_dup_in_lst(col)
        # print(col)
        if len(dup_row_num):
            for row_num in dup_row_num:
                combine_surrounding(board, row_num, col_num)
                move_ele_to_right(board.T)
        else:
            col_count += 1
        # print(dup_row_num)
        # print()
    if row_count == 10 and col_count == 10:
        return
    check_board_for_matches(board)

def combine_matched(board, row, col):     
    return

def write_json(data):
    with open("settings.json", "w") as json_file:
        json.dump(data, json_file)

def read_json():
    with open("settings.json", "r") as json_file:
        return json.load(json_file)

def json_test():
    data = [
        {            
            "name": "user",
            "password": "pass1",
            "high_score": "200",
            "music": "on",
        },
        {
            "name": "admin",
            "password": "pass2",
            "high_score": "300",
            "music": "off",
        },
    ]

    dump_json = json.dumps(data)
    with open("settings.json", "w") as json_file:
        json_file.write(dump_json)
    return

def main():
    # json_test()

    data = read_json()
    data[0]["high_score"] = "1000"
    write_json(data)

    # steps = [25, 40]
    # row_level = 15
    # for i in range(0, 3):
    #     for j in steps:
    #         row_level += j 
    #         print(row_level)

    # print(board)
    # print(board.T)
    # print()
    # print(board.T)
    # print(board)
    # drop_block(board, 6, 7)
    # print()
    # print(board)

if __name__ == "__main__":
    main()
