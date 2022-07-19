import pygame as pg,sys
from pygame.locals import *
import random 
from random import randint 
import time 
from time import sleep 

# global variables 
player = 'human' 
winner = None 
isGameOver = False 
board = [[None, None, None], [None, None, None], [None, None, None]]
human = ''
computer = '' 
r = -1 
c = -1 

# board dimensions and colors
width = 400 
height = 400 
blue = (0,0,245)
white = (245,245,245)
line_color = (10,10,10)
text_color = (245,0,0)

#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

# load and resize the images we will use
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

    # switch to main game window 
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    
    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)


# method to generate random number to determine who goes first
def random_num_generate():
    global human, computer, player               
    rand = randint(1,2)
    if rand == 1:
        human = 'x'                           # we're still assuming that x always goes first 
        computer = 'o'
        player = 'human' 
    else:
        human = 'o'
        computer = 'x' 
        player = 'computer' 

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
    global board, player, r, c, player

    possibilities = get_empty_squares()
    selected = random.choice(possibilities)
    r = selected[0]
    c = selected[1]
    board[r][c] = player  
    drawXO() 
    player = 'human' 
    print('computer played') 
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


def drawXO():
    global board, player, r, c

    # always draw 30 pixels below the nearest line 
    if r == 0:
        xcoord = 30
    if r == 1:
        xcoord = width/3 + 30
    if r == 2:
        xcoord = width/3*2 + 30

    if c == 0:
        ycoord = 30
    if c == 1:
        ycoord = height/3 + 30
    if c == 2:
        ycoord = height/3*2 + 30
    
    board[r][c] = player
    if(player == 'human'):
        if human == 'x':
            screen.blit(x_pic,(ycoord,xcoord))
        else: 
            screen.blit(o_pic,(ycoord,xcoord))
    else:
        if computer == 'x':
            screen.blit(x_pic,(ycoord,xcoord))
        else:
            screen.blit(o_pic,(ycoord,xcoord)) 
    pg.display.update() 


def mouseClick():
    global r, c, player

    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()

    #get column from x
    if x <= width/3:
        c = 0
    elif x <= width/3*2:
        c = 1
    elif x <= width:
        c = 2
    else:
        # display error message
        font = pg.font.Font(None, 30) 
        text = font.render('Please click on board', 1, text_color) 
        screen.fill((0,0,0), (0,400,500,100))
        text_rect = text.get_rect(center=(width/2, 500-50))
        screen.blit(text, text_rect) 
        pg.display.update()
        return 
        
    #get row from y 
    if y <= height/3:
        r = 0
    elif y <= height/3*2:
        r = 1
    elif y <= height:
        r = 2
    else:
        # display error message
        font = pg.font.Font(None, 30) 
        text = font.render('Please click on board', 1, text_color) 
        screen.fill((0,0,0), (0,400,500,100))
        text_rect = text.get_rect(center=(width/2, 500-50))
        screen.blit(text, text_rect) 
        pg.display.update()
        return 

    print(r) # make sure mouse click is being registered 
    print(c)
    drawXO()
    print('human played') 
    player = 'computer' 
    
    # draw the X or O on screen if cell is empty 
    #drawXO(row,col) 

# method to make moves and play game 
def make_moves():
    global board, winner, player, isGameOver, human, computer
    
    random_num_generate() 
    print("human is: ", human)
    print("computer is: ", computer) 
    print(player) 
    
    pygame_start() 

    while isGameOver == False: 
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit() 
                sys.exit() 
        if player == 'human':
            mouseClick() 
            sleep(2)
            #check_win()
        elif player == 'computer': 
            random_move() 
            sleep(2)
            #check_win() 
        check_win() 
        if winner is not None:
            print(winner.upper() + " Wins!") 
            break 
    return winner 

make_moves()   
