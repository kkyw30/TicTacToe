import pygame as pg,sys
from pygame.locals import *
import time

#initialize global variables
player = 'x'
winner = None
isGameOver = False 

width = 400
height = 400
white = (255, 255, 255)
blue = (0, 0, 245)
yellow = (255, 255, 0)
line_color = (10, 10, 10)
text_color = (245, 0, 0) 

#TicTacToe 3x3 board
TTT = [[None]*3,[None]*3,[None]*3]

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


def game_start(): 
    # display welcome message
    screen.fill(blue) 
    font = pg.font.Font('freesansbold.ttf', 32) 
    text = font.render('Welcome to TicTacToe! + \n + "Connect 3 in a" + \n + "row to win!', True, blue, line_color)
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


# method for redrawing original symbol in square (will use in highlighting part or check_win function) 
def redrawXO(row, col, winner):
    global TTT, player 

    # always draw 30 pixels below the nearest line 
    if row == 1:
        xcoord = 30
    if row == 2:
        xcoord = width/3 + 30
    if row == 3:
        xcoord = width/3*2 + 30

    if col == 1:
        ycoord = 30
    if col == 2:
        ycoord = height/3 + 30
    if col == 3:
        ycoord = height/3*2 + 30

    # determine which image to draw based on who won 
    if(winner == 'x'):
        screen.blit(x_pic,(ycoord,xcoord))
    else:
        screen.blit(o_pic,(ycoord,xcoord))
    pg.display.update()

def check_win():
    global TTT, winner, isGameOver

    # check for winning rows
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            isGameOver = True

            # highlight each square in the row 
            for i in range(0,3):
                if row == 0:
                    top_coord = 0
                elif row == 1:
                    top_coord = height/3
                elif row == 2:
                    top_coord = height/3*2
                left_coord = i*width/3
                pg.draw.rect(screen, yellow, pg.Rect(left_coord, top_coord, width/3, height/3))
                redrawXO(row+1,i+1,winner) 
            break

    # check for winning columns
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            isGameOver = True 

            # highlight each square in the column 
            for i in range(0,3):
                if col == 0:
                    left_coord = 0
                elif col == 1:
                    left_coord = width/3
                elif col == 2:
                    left_coord = width/3*2
                top_coord = i*height/3
                pg.draw.rect(screen, yellow, pg.Rect(left_coord, top_coord, width/3, height/3))
                redrawXO(i+1,col+1,winner)
            break

    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        isGameOver = True 

        # highlight each square on diagonal 
        pg.draw.rect(screen, yellow, pg.Rect(0,0,width/3, height/3))
        redrawXO(1,1,winner)
        pg.draw.rect(screen, yellow, pg.Rect(width/3, height/3, width/3, height/3))
        redrawXO(2,2,winner)
        pg.draw.rect(screen, yellow, pg.Rect(width/3*2, height/3*2, width/3, height/3))
        redrawXO(3,3,winner)
       

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        isGameOver = True 

        # highlight each square on diagonal
        pg.draw.rect(screen, yellow, pg.Rect(width/3*2, 0, width/3, height/3))
        redrawXO(1,3,winner)
        pg.draw.rect(screen, yellow, pg.Rect(width/3, height/3, width/3, height/3))
        redrawXO(2,2,winner)
        pg.draw.rect(screen, yellow, pg.Rect(0, height/3*2, width/3, height/3))
        redrawXO(3,1,winner) 
    
    # check if game is a draw 
    counter = 0
    for row in range(0,3):
        for col in range (0,3):
            if TTT[row][col] is not None:
                counter+=1
    if counter == 9 and winner is None: 
        isGameOver = True 
        winner = None 
    draw_status()

# method to draw the symbols on the board
def drawXO(row,col):
    global TTT, player 

    # always draw 30 pixels below the nearest line 
    if row == 1:
        xcoord = 30
    if row == 2:
        xcoord = width/3 + 30
    if row == 3:
        xcoord = width/3*2 + 30

    if col == 1:
        ycoord = 30
    if col == 2:
        ycoord = height/3 + 30
    if col == 3:
        ycoord = height/3*2 + 30
    
    TTT[row-1][col-1] = player
    if(player == 'x'):
        screen.blit(x_pic,(ycoord,xcoord))
        player = 'o'
    else:
        screen.blit(o_pic,(ycoord,xcoord))
        player = 'x'
    pg.display.update()   
    

def mouseClick():
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()
    row = 0
    col = 0 

    #get column from x
    if x <= width/3:
        col = 1
    elif x <= width/3*2:
        col = 2
    elif x <= width:
        col = 3
    else:
        # display error message
        font = pg.font.Font(None, 30) 
        text = font.render('Please click on board', 1, text_color) 
        screen.fill((0,0,0), (0,400,500,100))
        text_rect = text.get_rect(center=(width/2, 500-50))
        screen.blit(text, text_rect) 
        pg.display.update()
        
    #get row from y 
    if y <= height/3:
        row = 1
    elif y <= height/3*2:
        row = 2
    elif y <= height:
        row = 3
    else:
        # display error message
        font = pg.font.Font(None, 30) 
        text = font.render('Please click on board', 1, text_color) 
        screen.fill((0,0,0), (0,400,500,100))
        text_rect = text.get_rect(center=(width/2, 500-50))
        screen.blit(text, text_rect) 
        pg.display.update()
    
    # draw the X or O on screen if cell is empty 
    if(row and col and TTT[row-1][col-1] is None):
        global player 
        drawXO(row,col)
        check_win()
        
        
# method to reset the game
def reset():
    global TTT, winner, player, isGameOver 
    time.sleep(3)
    player = 'x'
    isGameOver = False 
    winner=None
    game_start()
    TTT = [[None,None,None],[None,None,None],[None,None,None]]
    

game_start()

# run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            mouseClick()
            if(isGameOver):
                reset()
            
    pg.display.update()
    CLOCK.tick(fps)
