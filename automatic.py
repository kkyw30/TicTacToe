import pygame as pg,sys
from pygame.locals import *
import random 
import time 
from time import sleep 

# global variables 
player = 'x' 
winner = None 
isGameOver = False 
board = [[None, None, None], [None, None, None], [None, None, None]]

# board dimensions and colors
width = 400 
height = 400 
blue = (0,0,245)
white = (245,245,245)
line_color = (10,10,10)

#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

# load and resize the iamges we will use
x_pic = pg.image.load('x.png')
o_pic = pg.image.load('o.png')
x_pic = pg.transform.scale(x_pic, (80,80))
o_pic = pg.transform.scale(o_pic, (80,80))

def pygame_start():
    # display welcome message
    screen.fill(blue) 
    font = pg.font.Font('freesansbold.ttf', 32) 
    text = font.render('Welcome to TicTacToe!', True, blue, line_color)
    textRect = text.get_rect() 
    textRect.center = (width // 2, height // 2) 
    screen.blit(text, textRect)
    pg.display.update() 
    pg.time.delay(3000) 

    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    
    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)

# get list of all available squares
def get_empty_squares():
    global board 

    possibilities = [] 
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col] == None:
                possibilities.append((row, col))    # list of 2d array indices
    
    return possibilities

# make a random move 
def random_move():
    global board, player

    possibilities = get_empty_squares()
    selected = random.choice(possibilities)
    row = selected[0]
    col = selected[1]
    board[row][col] = player  
    drawXO(row,col)  
    draw_status() 

def draw_status():
    # determine what message to display
    if winner == None and not isGameOver:
        message = player.upper() + "'s Turn"
    elif winner is not None and isGameOver:
        message = winner.upper() + " won!"
    elif winner == None and isGameOver:
        message = "DRAW" 

    # display the right message
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global isGameOver, winner, board 
    
    # check rows for win 
    for row in range(0,3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            isGameOver = True 
            winner = board[row][0] 

    # check columns for win
    for col in range(0,3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            isGameOver = True 
            winner = board[0][col] 
    
    # check diagonals for win 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None: 
        isGameOver = True 
        winner = board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None: 
        isGameOver = True 
        winner = board[0][2]

    # check for draw 
    counter = 0
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col] is not None: 
                counter += 1
    if counter == 9 and winner == None: 
        isGameOver = True 
    draw_status() 

# method to make moves and play game 
def make_moves():
    global board, winner, player, isGameOver 

    pygame_start() 
    while isGameOver == False: 
        print(player.upper() + ' move') 
        random_move()
        print(board)  
        sleep(2) 
        # update the player 
        if player == 'x':
            player = 'o'
        else: 
            player = 'x'
        check_win() 
        if winner is not None:
            print(winner.upper() + " Wins!") 
            break 
    return winner 

def drawXO(row,col):
    global board, player 

    # always draw 30 pixels below the nearest line 
    if row == 0:
        xcoord = 30
    if row == 1:
        xcoord = width/3 + 30
    if row == 2:
        xcoord = width/3*2 + 30

    if col == 0:
        ycoord = 30
    if col == 1:
        ycoord = height/3 + 30
    if col == 2:
        ycoord = height/3*2 + 30
    
    board[row][col] = player
    if(player == 'x'):
        screen.blit(x_pic,(ycoord,xcoord))
        #player = 'o'
    else:
        screen.blit(o_pic,(ycoord,xcoord))
        #player = 'x'
    pg.display.update() 

make_moves()   
    

