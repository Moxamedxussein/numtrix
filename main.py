import numpy as np 
import random, os, sys
import json
import pygame
from login import open_login_form

block_size = 64
logged_in, current_user, current_user_num, high_score, n_row, n_col = open_login_form()
play_width = block_size * n_col
play_height = block_size * n_row 
add_width = 200
add_height = 100
screen_width = play_width + add_width 
screen_height = play_height + add_height 


# board = np.array([(0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,0,0,0,0,0,0,0,0),
#                   (0,0,4,0,0,8,7,0,0,0),
#                   (0,3,2,6,8,9,3,2,8,0),
#                   (1,8,3,7,4,2,1,9,5,6)], dtype=np.int8)

block_img =    {1: "asset/1.svg",
                2: "asset/2.svg",
                3: "asset/3.svg",
                4: "asset/4.svg",
                5: "asset/5.svg",
                6: "asset/6.svg",
                7: "asset/7.svg",
                8: "asset/8.svg",
                9: "asset/9.svg",}

sound_file = {"combine": "asset/combine.mp3",
              "disappear": "asset/disappear.mp3",
              "game_over": "asset/game_over.mp3",
              "background": "asset/background.mp3",
             }

def write_json(data):
    with open("settings.json", "w") as json_file:
        json.dump(data, json_file)

def read_json():
    with open("settings.json", "r") as json_file:
        return json.load(json_file)

def play_sound(name):
    sound = pygame.mixer.Sound(sound_file[name])
    sound.play()

def first_nonzero(board):
    invalid_val=len(board)
    mask = board!=0
    row = np.array(np.where(mask.any(axis=0), mask.argmax(axis=0), invalid_val), dtype=np.int8)
    return row

def move_ele_to_right(board):
    for row_num, lst in enumerate(board):
        lst = lst[lst != 0]
        if len(lst):
            for _ in range(0, len(board[row_num])-len(lst)):
                lst = np.insert(lst, 0, 0)
            board[row_num] = lst

def combine_surrounding(board, row, col):
    blocks, scores = [], 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
                if (0 <= row+dx <= len(board)-1) and (0 <= col+dy <= len(board[0])-1):
                    if board[row+dx][col+dy] and board[row][col]:
                        if board[row+dx][col+dy] == board[row][col]:
                            blocks.append(Block(row, col, int(board[row][col])))
                            blocks.append(Block(row+dx, col+dy, int(board[row+dx][col+dy])))
                            if board[row+dx][col+dy] + board[row][col] == 18:
                                board[row+dx][col+dy] = 0
                                board[row][col] = 0
                                scores += 20
                                play_sound("disappear")
                            else:
                                scores += 10
                                play_sound("combine")
                                if row+col > row+dx+col+dy:
                                    board[row][col] += 1
                                    board[row+dx][col+dy] = 0
                                else:
                                    board[row][col] = 0
                                    board[row+dx][col+dy] += 1
    return blocks, scores

def get_dup_in_lst(lst):
    res = []
    for i in range(1, len(lst)):
        if lst[i-1] != 0 and lst[i] != 0:
            if lst[i-1] == lst[i]:
                res.append(i)
    return res

def check_board_for_matches(board, blocks):
    scores, row_count, col_count = 0, 0, 0
    # Check row
    for row_num, row in enumerate(board):
        dup_col_num = get_dup_in_lst(row)
        if len(dup_col_num):
            for col_num in dup_col_num:
                blocks.append(combine_surrounding(board, row_num, col_num))
                move_ele_to_right(board.T)
        else:
            row_count += 1
    # Check column
    for col_num, col in enumerate(board.T):
        dup_row_num = get_dup_in_lst(col)
        if len(dup_row_num):
            for row_num in dup_row_num:
                blocks.append(combine_surrounding(board, row_num, col_num))
                move_ele_to_right(board.T)
        else:
            col_count += 1
    move_ele_to_right(board.T)
    if row_count == n_row and col_count == n_col:
        print("checking for matches", blocks)
        return blocks
    check_board_for_matches(board, blocks)
    return blocks

def drop_block(board, current_block):
    row_level = first_nonzero(board)[current_block.x]-1
    if row_level == -1:
        print("You lose!")
        return True
        # print("Row level dropping at ", row_level)
    current_block.dest = row_level
    return False
    # print(first_nonzero(board)[current_block.x]-1)

class Block(object):
    def __init__(self, row, column, num):
        self.x = column 
        self.y = row
        self.num = num
        self.dest = -1
        
def get_rand_block():
    # return Block(0.0, n_col//2, random.choice(range(9, 10)))
    # return Block(0.0, n_col//2, random.choice(range(1, 2)))
    return Block(0.0, n_col//2, random.choice(range(1, 10)))

def draw_block(screen, block, color=False, normal=True):
    sx = block.x*block_size
    sy = block.y*block_size + add_height - (block_size if normal else 0)
    image = pygame.image.load(block_img[block.num])
    if color:
        image.fill((0, 0, 0))
        # print("Blackening at", block.x, block.y)
    screen.blit(image, pygame.Rect(sx, sy, block_size, block_size))

def draw_grid(screen, board):
    sx = 0
    sy = 0
    for i in range(len(board)):
        pygame.draw.line(screen, (128, 128, 128), (sx, sy + i * block_size + add_height), (play_width, sy+i*block_size+add_height), 3)
        for j in range(len(board[i])):
            pygame.draw.line(screen, (128, 128, 128), (sx+j*block_size, sy+add_height), (sx+j*block_size, screen_width), 3)

def draw_window(screen, board): 
    screen.fill((0,0,0,)) # Fill background with color R,G,B
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                image = pygame.image.load(block_img[board[i][j]])
                screen.blit(image, pygame.Rect(j*block_size, i*block_size+add_height, block_size, block_size))

def draw_info(screen, font, texts):
    pygame.draw.rect(screen, (123, 128, 138), (play_width, 0, screen_width-play_width, screen_height))
    steps = [50, 25]
    row_level, temp = 0, 0
    for i in range(0, len(texts), 2):
        for count, j in enumerate(steps):
            row_level += j
            text = font.render(str(texts[count+i]), True, (255, 255, 255))
            screen.blit(text, (play_width+10, row_level))
            temp += 1
        temp = 0

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                return

def main():
    global n_row, n_col
    logged_in, current_user, current_user_num, high_score, n_row, n_col = open_login_form()
    if logged_in:
        handle_game(current_user, current_user_num, high_score, n_row, n_col)

def handle_game(current_user, current_user_num, high_score, n_row, n_col):
    settings = read_json()
    
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(sound_file["background"])
    pygame.mixer.music.play(-1, 0.0)

    board = np.zeros((n_row, n_col))
    screen = pygame.display.set_mode([screen_width, screen_height])
    font = pygame.font.SysFont("arialblack", 20)
    pygame.display.set_caption("Numtrix")
    current_block, next_block = get_rand_block(), get_rand_block()
    clock = pygame.time.Clock()
    disappearing_block = []
    fall_speed, delay, count, total_scores = 0.25, 100, 0, 0
    running, show = True, True
    current_time = pygame.time.get_ticks()
    change_time = current_time + delay
    background = pygame.image.load("asset/Gameover.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current_block.x = np.clip(current_block.x-1, 0, (play_width//block_size)-1)
                if event.key == pygame.K_s:
                    if(drop_block(board, current_block)):
                        screen.fill((0, 0, 0))
                        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0)) 
                        pygame.display.update()
                        wait()
                        print("Resumed!")
                        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
                if event.key == pygame.K_d:
                    current_block.x = np.clip(current_block.x+1, 0, (play_width//block_size)-1)

        if current_block.dest != -1:
            current_block.y += fall_speed
        if current_block.y > current_block.dest+1:
            board[current_block.dest][current_block.x] = current_block.num
            disappearing_block = check_board_for_matches(board, [])
            current_block = next_block
            next_block = get_rand_block()
    
        current_time = pygame.time.get_ticks()

        # keys = pygame.key.get_pressed() 
        # if keys[pygame.K_a]:
        #     current_block.x = np.clip(current_block.x-1, 0, (play_width//block_size)-1)
        # if keys[pygame.K_s]:
        #     drop_block(board, current_block)
        # if keys[pygame.K_d]:
        #     current_block.x = np.clip(current_block.x+1, 0, (play_width//block_size)-1)

        draw_window(screen, board)
        draw_grid(screen, board)
        draw_block(screen, current_block)
        draw_info(screen, font,
                 ("Current Scores: ", total_scores, "High Score: ", high_score, "Current user: ", current_user))

        # if len(disappearing_block) and not (None in disappearing_block) and not ([] in disappearing_block):
        if len(disappearing_block):
            if count > 4:
                total_scores += sum([i[-1] for i in disappearing_block])                 
                if total_scores > int(settings[current_user_num]["high_score"]):
                    data = read_json()
                    data[current_user]["high_score"] = total_scores
                    write_json(data)
                print("Total scores: ", total_scores)
                count = 0
                disappearing_block = [] 
                show = True 
            if current_time >= change_time:
                change_time = current_time + delay 
                show = not show
                count += 1
            for pair in disappearing_block: 
                for blocks in pair[:-1]:
                    [draw_block(screen, block, True if show else False, False) for block in blocks]
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    if logged_in:
        handle_game(current_user, current_user_num, high_score, n_row, n_col)
