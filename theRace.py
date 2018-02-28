import pygame
import time
import random

#initiation function for python - initiate pygame
pygame.init()

# get sound
crash_sound = pygame.mixer.Sound("crash.wav")  
pygame.mixer.music.load("car.wav")

#declaring variable
display_width = 800
display_height = 600
#define collors with RGB (Red Green Blue)
black = (0,0,0) #no color, no light on a black screan
white = (254,254,254) #maximum light
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53, 115, 255)

car_width = 50
car_height = 100
#initiate vindow
gameDisplay = pygame.display.set_mode((display_width,display_height))
#initiate title
pygame.display.set_caption('The Race')
#the game clock- it is measure haw many frame per second
clock = pygame.time.Clock()

#create the car - use GIMP Colors -> Colors to Alpha to get over it white
carImg = pygame.image.load('racecar.png')

#set the icon of the game to be carImg
gameIcon = pygame.image.load('racecarIcon.png')
pygame.display.set_icon(gameIcon)

pause = False # define and set pause to false

#this method will count how many object was dodged (avoided) and will ad points
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
    
#define a function to drow objects (obstacles) 
def things(thingx, thingy, thingw, thingh, color): # (x, y, weight, height, collor)
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    
#create the car method
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

#method to return text objects
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#method to display a message to the center of the screen
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',60) #(font type, font size)
    TextSurf, TextRect = text_objects(text, largeText)   #set the tesx and the font and type of text inside the rectangle where will be the text 
    TextRect.center = ((display_width/2) , (display_height/2)) #set this mesage in the center of screen
    gameDisplay.blit(TextSurf, TextRect) # blit() will draw the text on the screen
    
#define crash method
def crash():
    # set the music
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
    message_display('You Crashed')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              quitgame()
        # Call button method
        button("Play Again!", 150, 450, 150, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)

#define the start button method
#the method pass a message, x and y coordinates, width, height, a inactive collor, a active collor and a action/method
def button(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos() # Grab mouse position
    click = pygame.mouse.get_pressed() # Get the click
    # Create the start and quit buttons
    if x+w > mouse[0] > x and y+h > mouse[1] > y: # If the mouse cursor is over the button
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h)) # Color the mouse lighter to look interactive
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(msg, smallText)   #set the tesx and the font and type of text inside the rectangle where will be the text 
    TextRect.center = ((x+(w/2)), (y+(h/2))) #set this mesage in the center of screen
    gameDisplay.blit(TextSurf, TextRect)

# Define the quit game method
def quitgame():
    pygame.quit()
    quit()

# The game intro method
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(white)
        # display the message on the screen
        message_display('The Race')
        # Call button method
        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
       
        pygame.display.update()
        clock.tick(15)

# The unpause method
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    

# Define the game pause method
def paused():
    pygame.mixer.music.pause() # stom the music
    
    message_display('Paused')
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
 
        # Call button method
        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
       
        pygame.display.update()
        clock.tick(15)

# The main game loop
def game_loop():
    
    # set the music
    pygame.mixer.Sound.stop(crash_sound)
    pygame.mixer.music.play(-1) # -1 will play the music in a loop
    global pause

    #set the position for x ang y
    x = (display_width*0.45)
    y = (display_height*0.8)

    x_change = 0

    # The blocks
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    dodged = 0
    
    #state that we are not crashed yet
    gameExit = False

    while not gameExit:
        #event: is everithing that is happened in the frame
        for event in pygame.event.get():
            #if quit then we chrashed
            if event.type == pygame.QUIT:
                quitgame()
                
            #if a key is presed  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5 #decrease the x by 5
                if event.key == pygame.K_RIGHT:
                    x_change = 5 # increase x by 5
                if event.key == pygame.K_p: # if 'p' is pressed then pause the game
                    pause = True
                    paused()  # call the paused method
                    
            #if a key is released 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0  # no mor change if a key is pressed again
                    
        #change the value of x
        x += x_change
        #change the background
        gameDisplay.fill(white)
        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed #each time vhen we run the loop will add 7 pixels to the y start coordinates
        
        #show yhe car
        car(x,y)
        things_dodged(dodged)
        
        #if the car chrash in the wall left or right game exit
        if x > display_width - car_width or x < 0:
            crash()
        # if a thing(square) leaved the screen
        if thing_starty > display_height: 
            thing_starty = 0 - thing_height #reset the y to the top of the screen
            thing_startx = random.randrange(0, display_width) #reset x to random
            dodged += 1  # increase the score
            thing_speed += (dodged * 0.05) # increase the speed
            thing_width += (dodged * 0.2) # increase the width of squares
            
        # check if the car was crashed
        if y < thing_starty+thing_height: #check if y was cross
            # check if x was crossed
            if ((x > thing_startx) and (x < (thing_startx + thing_width))) or (((x + car_width) > thing_startx) and ((x + car_width) < (thing_startx + thing_width))):
                crash()
            
        #update the display
        pygame.display.update()
        #set the speed - frame per second
        clock.tick(60)

#call the intro
game_intro()
#call the game loop
game_loop()
#uninitiate pygame - stop pygame for running
quitgame()

            
