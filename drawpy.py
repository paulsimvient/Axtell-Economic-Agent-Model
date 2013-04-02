 
import pygame
from MiddleMen import *
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue      = ( 0,   0,   255)

# This sets the width and height of each grid location
width=19
height=19

gridSize = 40
 
# This sets the margin between each cell
margin=1
 
# Create a 2 dimensional array. A two dimesional
# array is simply a list of lists.
grid=[]
for row in range(gridSize):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(gridSize):
        grid[row].append(0) # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
#grid[6][1] = 1
 
#menu
 
print "random neighbor"

neighbor_sim = False
print "good",'A', 'B', 'C'
 
# Initialize pygame
pygame.init()
  
# Set the height and width of the screen
size=[800,800]
screen=pygame.display.set_mode(size)
 
# Set title of screen
pygame.display.set_caption("mid terms")
 
#Loop until the user clicks the close button.
done=False

#play the middle men game
middleMen = playGame()

 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
 
#build agent by type 
middleMen.BuildAgents(gridSize, gridSize, neighbor_sim)

#counts ticks
Counter = 0

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
     
                
    #do next agent move   
    middleMen.AgentNext()
    

    # Set the screen background
    screen.fill(black)
 
    # Draw the grid
    for row in range(gridSize):
        for column in range(gridSize):
            color = white
            if grid[row][column] == 1:
                color = red
            pygame.draw.rect(screen,color,[(margin+width)*column+margin,
                                           (margin+height)*row+margin,width,height])
    
   
    for agent in Agents:
        pygame.draw.rect(screen,agent.Color,[(margin+width)*agent.Location[1] +margin,
                                        (margin+height)*agent.Location[0] +margin,width,height])
       
 
    #count trial
    Counter += 1
    if Counter % 100 == 0: 
        countRed = 0 
        countGreen = 0
        countBlue = 0
        
        for agent in Agents:
            if agent.Color == red:
                countRed +=1
            if agent.Color == green:
                countGreen +=1 
            if agent.Color == blue:
                countBlue +=1             
        
        #print countBlue,",", countGreen, ",",countRed
        
    # Limit to 20 frames per second
    #clock.tick(10)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
