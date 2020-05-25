import pygame
import sys
import random
import time

pygame.init()

WHITE = (255, 255, 255)
BLUE = (68, 114, 196)
RED = (255, 0, 0)
BLACK = (211, 211, 211)
GREEN = (112, 173, 71)
PURPLE = (112, 48, 160)
ORANGE = (237, 125, 49)
TOURKISE = (0, 255, 255)
YELLOW = (255, 192, 0)

SQ_SIZE = 30

font = pygame.font.Font(pygame.font.get_default_font(), 32)


class Shape:
    def __init__(self, name, body, color, x=5, y=0, axis=[0, 0]):
        self.name = name
        self.body = body
        self.color = color
        self.x = x
        self.y = y
        self.axis = axis

    def rotate(self):
        if self.name != "O":
            for i in range(len(self.body)):
                if self.body[i] != self.axis:
                    # zamenjam x in y ter pomnožim nov x, da mu spremenim predznak
                    x = self.body[i][0]
                    y = self.body[i][1]
                    self.body[i][0] = y * (-1)
                    self.body[i][1] = x


BLOCK_I = Shape("I", [[0, -1], [0, 0], [0, 1], [0, 2]], BLUE)
BLOCK_L = Shape("L", [[0, 1], [0, 0], [0, -1], [1, -1]], GREEN)
BLOCK_J = Shape("J", [[0, 1], [0, 0], [0, -1], [-1, -1]], PURPLE)
BLOCK_Z = Shape("Z", [[0, -1], [0, 0], [-1, 0], [-1, 1]], RED)
BLOCK_S = Shape("S", [[-1, -1], [0, 0], [-1, 0], [0, 1]], TOURKISE)
BLOCK_T = Shape("T", [[-1, 0], [0, 0], [1, 0], [0, -1]], ORANGE)
BLOCK_O = Shape("O", [[0, 1], [0, 0], [-1, 0], [-1, 1]], YELLOW)

blocks = (BLOCK_I, BLOCK_L, BLOCK_J, BLOCK_Z, BLOCK_S, BLOCK_T, BLOCK_O)


def print_board(screen):
    buf_y = 20
    buf_x = 100
    for row in range(20):
        for col in range(10):
            color = board[row][col]
            pygame.draw.rect(screen, color, (col * SQ_SIZE + buf_x, row * SQ_SIZE + buf_y, SQ_SIZE, SQ_SIZE))
    # narišem belo mrežo čez vse
    for row in range(20):
        for col in range(10):
            pygame.draw.rect(screen, WHITE, (col * SQ_SIZE + buf_x, row * SQ_SIZE + buf_y, SQ_SIZE, SQ_SIZE), 1)
    pygame.display.update()


def check_below():
    global board, block

    flag = False
    for i in block.body:
        x = i[0] + block.x
        y_next = i[1] + block.y + 1
        if y_next > 19:
            flag = True
        elif board[y_next][x] != BLACK:
            flag = True
    return flag


def check_left():
    global board, block

    flag = False
    for i in block.body:
        x_next = i[0] + block.x - 1
        y = i[1] + block.y
        if x_next < 0:
            flag = True
        elif board[y][x_next] != BLACK:
            flag = True
    return flag


def check_right():
    global board, block

    flag = False
    for i in block.body:
        x_next = i[0] + block.x + 1
        y = i[1] + block.y
        if x_next > 9:
            flag = True
        elif board[y][x_next] != BLACK:
            flag = True
    return flag


def check_rotate():
    global board, block

    flag = False
    block.rotate()
    for i in block.body:
        x_next = i[0] + block.x
        y_next = i[1] + block.y
        if x_next > 9 or x_next < 0:
            flag = True
        if y_next > 19:
            flag = True
        if board[y_next][x_next] != BLACK:
            flag = True
            # zavrtim 3x da pridem nazaj v orignal
    block.rotate()
    block.rotate()
    block.rotate()
    return flag


def show_block_on_board():
    global board, block, game, next_block
    buf_x = 100
    buf_y = 20
    sq_size = 30
    for i in block.body:
        x = i[0] + block.x
        y = i[1] + block.y
        pygame.draw.rect(screen, block.color, (x * sq_size + buf_x, y * sq_size + buf_y, sq_size, sq_size))
        pygame.draw.rect(screen, WHITE, (x * sq_size + buf_x, y * sq_size + buf_y, sq_size, sq_size), 1)
    # preveri če je še prostor na polju vrstico nižje in če ni izven okvira (y_next>19)
    flag = check_below()
    if flag == True:
        for i in block.body:
            x = i[0] + block.x
            y = i[1] + block.y
            board[y][x] = block.color
        # nov blok
        if block.y > 1:
            # nov lik
            block = next_block
            next_block = random.choice(blocks)
            draw_next_block()
# mogoče ni treba
            block.y = 0
            block.x = 5
        else:
            game = False
            print("GAME OVER")
            show_score()
            pygame.display.update()

            time.sleep(5)

    pygame.display.update()


def check_rows():
    global board, score, block, next_block

    for row in range(20):
        full_row = True
        for col in range(10):
            color = board[row][col]
            if color == BLACK:
                full_row = False
        if full_row == True:
            score += 1
            print(score)
            # zbriše to vrstico
            del board[row]

            # nova vrstiva na začetku
            board.insert(0, [BLACK] * 10)

            # nov lik
            block = next_block
            next_block = random.choice(blocks)
            draw_next_block()

            block.x = 5
            block.y = 0


def show_score():
    global game
    pygame.draw.rect(screen, BLACK, (50, 625, 600, 50))

    if game == True:
        score_label = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_label, (180, 645))
    else:
        score_label = font.render("GAME OVER Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_label, (75, 645))


def draw_next_block():
    pygame.draw.rect(screen, BLACK, (450, 70, 150, 200))
    next_block_label = font.render("Next:", True, (0, 0, 0))
    screen.blit(next_block_label, (485, 70))
    for i in next_block.body:
        x = i[0]
        y = i[1]
        pygame.draw.rect(screen, next_block.color, (x * SQ_SIZE + 520, y * SQ_SIZE + 180, SQ_SIZE, SQ_SIZE))
        pygame.draw.rect(screen, WHITE, (x * SQ_SIZE + 520, y * SQ_SIZE + 180, SQ_SIZE, SQ_SIZE), 1)
    pygame.display.update()




score = 0

pygame.init()
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
screen.fill(BLACK)

block = random.choice(blocks)
block.y=1
next_block = random.choice(blocks)
draw_next_block()

# naredim prazno polje črne barve in začetni parametri
board = [[BLACK] * 10 for i in range(20)]
game = True
clock = pygame.time.Clock()
FPS = 2

pygame.key.set_repeat(10)

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                flag = check_left()
                if flag == False:
                    block.x = block.x - 1
            if event.key == pygame.K_RIGHT:
                flag = check_right()
                if flag == False:
                    block.x = block.x + 1
            if event.key == pygame.K_UP:
                flag = check_rotate()
                if flag == False:
                    block.rotate()
            if event.key == pygame.K_DOWN:
                FPS = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                FPS = 2

    print_board(screen)
    show_score()
    show_block_on_board()
    check_rows()
    block.y += 1
