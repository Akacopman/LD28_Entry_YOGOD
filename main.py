#Imports
import pygame
import re #Fixes stupid cx_Freeze bug.
from pygame.locals import *
import sys, os, traceback, random

######### Used to detect screen resolution. Will require a different method on other platforms. #########

import ctypes
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#########################################################################################################

devmode = False



pygame.mixer.pre_init(44100, -16, 2, 2048)


pygame.display.init()
pygame.font.init()
pygame.init()   
#screen_size = [1280, 800] #Test resolution.

surface = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

pygame.display.set_caption("You Only Get One Dollar!")

icon = pygame.image.load("images/icon.png").convert_alpha()        
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Arial',22)

pygame.mixer.music.load("sound/repetetivesong.wav")#load music

pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.5)


playerSpeed = 4
playerX = 100
playerY = 510

LotteryChance = random.randint(1, 25)

Money = 1

companyLogo = str(random.randint(1, 3))

TimesPissed = 0

bg = pygame.image.load("images/bg" + companyLogo + ".png").convert()

bg = pygame.transform.scale(bg, screen_size).convert()

start_screen = pygame.image.load("images/start_screen.png").convert()

start_screen = pygame.transform.scale(start_screen, screen_size).convert()

GameOverScreen = pygame.image.load("images/gameover.png").convert()

GameOverScreen = pygame.transform.scale(GameOverScreen, screen_size).convert()

GameOverScreenPiss = pygame.image.load("images/gameoverpiss.png").convert()

GameOverScreenPiss = pygame.transform.scale(GameOverScreenPiss, screen_size).convert()

GameOverScreenSteam = pygame.image.load("images/gameoversteam.png").convert()

GameOverScreenSteam = pygame.transform.scale(GameOverScreenSteam, screen_size).convert()

GameOverScreenSoda = pygame.image.load("images/gameoversoda.png").convert()

GameOverScreenSoda = pygame.transform.scale(GameOverScreenSoda, screen_size).convert()

GameOverScreenLottery = pygame.image.load("images/gameoverlottery.png").convert()

GameOverScreenLottery = pygame.transform.scale(GameOverScreenLottery, screen_size).convert()

GameOverScreenDrain = pygame.image.load("images/gameoverdrain.png").convert()

GameOverScreenDrain = pygame.transform.scale(GameOverScreenDrain, screen_size).convert()

WinScreenLottery = pygame.image.load("images/wingamelottery.png").convert()

WinScreenLottery = pygame.transform.scale(WinScreenLottery, screen_size).convert()

WinScreen = pygame.image.load("images/wingame.png").convert()

WinScreen = pygame.transform.scale(WinScreen, screen_size).convert()

pygame.mouse.set_visible(False)

KnowsAboutNail = False

GotWaterMoney = False

GotCarpetMoney = False

inUse = False

LoseBySteam = False
LoseBySoda = False

startScreen = True
WonLottery = False

pressedYes = False
pressedNo = False

GameOver = False

HasHammer = False

UsingVendingMachine = False
UsingToilet = False
UsingWaterCooler = False
UsingBossDoor = False
UsingPC = False
UsingWeb = False
UsingToolBox = False
GotBoardMoney = False
ThrewAwayMoney = False

UsingBoard = False

playerFrame = random.randint(1, 3)

UsingWaterCoolerSoda = False
GotSoda = False
GotWaterMoney = False
UsingEmptyCooler = False
UsingLottery = False
LoseByLottery = False

UsingPurse = False
GotPurseMoney = False
UsingEmptyPurse = False

UsingCarpet = False
UsingPoster = False

LostLottery = False

WebResponse = random.randint(1, 3)

COLLIDED_UP = False
COLLIDED_LEFT = False
COLLIDED_RIGHT = False
COLLIDED_DOWN = False

cache={}

designWidth = 1600
designHeight = 900
scaleFactorWidth = screen_size[0] / designWidth
scaleFactorHeight = screen_size[1] / designHeight

logoPosX, logoPosY = scaleFactorWidth * 325, scaleFactorHeight * 100

def get_cache(msg, aa): #Font cache. Work in Progress.
    
    if not msg in cache:
        
      cache[msg] = font.render(msg, aa , (255,255,255))

      if devmode is True:
          print("Added string " + msg + " to the cache.")
      
    return cache[msg]

def drawText(string, posx, posy, aa = None):

    if aa is None:
        aa = False

    msg = string

    textobj=get_cache(msg, aa)
    
    surface.blit(textobj, (posx,posy))

image_cache = {}

def get_image(path):
    
        global image_cache
        
        image = image_cache.get(path)
        
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace("\\", os.sep)
                
                image = pygame.image.load(canonicalized_path).convert_alpha()
                
                
                image_cache[path] = image
                
        return image

def blitImage(imgName, imageX, imageY):

    surface.blit(get_image("images/" + imgName),(imageX, imageY)) #Because I am a lazy arse.


def framecounter(): #Display FPS.

    drawText("FPS: " + str(round(float(clock.get_fps()) ) ), 0, 0)

def textBox(text1, text2, text3, canWalk):

    global inUse
    
    pygame.draw.rect(surface, (0,0,0), (25,scaleFactorHeight * 700, 700,scaleFactorHeight * 150), 0)
    drawText(text1, 50, scaleFactorHeight * 725, True)
    drawText(text2, 50, scaleFactorHeight * 750, True)
    drawText(text3, 50, scaleFactorHeight * 775, True)
    if canWalk == False:
        inUse = True
    

def get_input(): #Input code here

    global playerX
    global playerY 
    global playerSpeed
    global startScreen
    global inUse
    global pressedNo
    global pressedYes
    global Money
    global GameOver
    global UsingVendingMachine
    global UsingToilet
    global UsingWaterCooler
    global UsingBossDoor
    global UsingPC
    global UsingWeb
    global WebResponse
    global GotSoda
    global UsingWaterCoolerSoda
    global GotWaterMoney
    global UsingEmptyCooler
    global UsingLottery
    global UsingPurse
    global GotPurseMoney
    global UsingEmptyPurse
    global LotteryChance
    global LostLottery
    global UsingCarpet
    global GotCarpetMoney
    global TimesPissed
    global UsingBoard
    global UsingToolBox
    global KnowsAboutNail
    global HasHammer
    global GotBoardMoney
    global UsingPoster
    global LoseBySteam
    global LoseBySoda
    global LoseByLottery
    global WonLottery
    global ThrewAwayMoney
    
    keys = pygame.key.get_pressed()
    if startScreen == False:
        if GameOver == False:
            if inUse == False:
                if keys[pygame.K_w]:
                    if playerY > screen_size[1] / 2 + 10:
                        if COLLIDED_UP == False:
                            playerY = playerY - playerSpeed
                if keys[pygame.K_a]:
                    if playerX > 0:
                        if COLLIDED_LEFT == False:
                            playerX = playerX - playerSpeed
                if keys[pygame.K_s]:
                    if playerY < screen_size[1]:
                        if COLLIDED_DOWN == False:
                            playerY = playerY + playerSpeed
                if keys[pygame.K_d]:
                    if playerX < screen_size[0]:
                        if COLLIDED_RIGHT == False:
                            playerX = playerX + playerSpeed


                        
            if keys[pygame.K_e]:
                #Vending Machine
                if playerX > scaleFactorWidth * 1125 and playerX < scaleFactorWidth * 1275 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 500:
                    UsingVendingMachine = True
                    inUse = True
                #Toilet
                if playerX > scaleFactorWidth * 1335 and playerX < scaleFactorWidth * 1465 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 500:
                    UsingToilet = True
                    inUse = True
                #Water Cooler
                if playerX > scaleFactorWidth * 359 and playerX < scaleFactorWidth * 429 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 500:
                    if GotSoda == True:
                        UsingWaterCoolerSoda = True
                        inUse = True
                    elif GotWaterMoney == True:
                        inUse = True
                        UsingEmptyCooler = True
                    else:
                        inUse = True
                        UsingWaterCooler = True
                #Boss Door
                if playerX > scaleFactorWidth * 75 and playerX < scaleFactorWidth * 195 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 500:
                    inUse = True
                    UsingBossDoor = True
                #PC Master Race
                if playerX > scaleFactorWidth * 1171 and playerX < scaleFactorWidth * 1301 and playerY > scaleFactorHeight * 800 and playerY < scaleFactorHeight * 864:
                    inUse = True
                    UsingPC = True
                #Lottery
                if playerX > scaleFactorWidth * 980 and playerX < scaleFactorWidth * 1060 and playerY > scaleFactorHeight * 814 and playerY < scaleFactorHeight * 876:
                    UsingLottery = True
                    inUse = True
                #Purse
                if playerX > scaleFactorWidth * 1371 and playerX < scaleFactorWidth * 1501 and playerY > scaleFactorHeight * 650 and playerY < scaleFactorHeight * 780:
                    if GotPurseMoney == True:
                        UsingEmptyPurse = True
                        inUse = True
                    else:   
                        UsingPurse = True
                        inUse = True
                #Carpet
                if playerX > scaleFactorWidth * 600 and playerX < scaleFactorWidth * 730 and playerY > scaleFactorHeight * 600 and playerY < scaleFactorHeight * 780:
                    if GotCarpetMoney == False:
                        UsingCarpet = True
                        inUse = True
                #Board
                if playerX > scaleFactorWidth * 575 and playerX < scaleFactorWidth * 875 and playerY > scaleFactorHeight * 400 and playerY < scaleFactorHeight * 500:
                    UsingBoard = True
                    inUse = True
                #Toolbox
                if playerX > scaleFactorWidth * 257 and playerX < scaleFactorWidth * 357 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 520:
                    UsingToolBox = True
                    inUse = True
                #Poster
                if playerX > scaleFactorWidth * 925 and playerX < scaleFactorWidth * 1025 and playerY > scaleFactorHeight * 450 and playerY < scaleFactorHeight * 520:
                    UsingPoster = True
                    inUse = True

                
            if keys[pygame.K_1]:
                
                if UsingToilet == True:
                    UsingToilet = False
                    inUse = False
                    TimesPissed += 1
                    Money += 1

                if UsingVendingMachine == True:
                    UsingVendingMachine = False
                    Money -= 1
                    if GotWaterMoney == False:
                        GotSoda = True
                    inUse = False
                    if Money <= 0:
                        LoseBySoda = True
                    
                if UsingWaterCooler == True:
                    UsingWaterCooler = False
                    inUse = False
                    
                if UsingBossDoor == True:
                    UsingBossDoor = False
                    inUse = False
                    
                if UsingPC == True:
                    UsingPC = False
                    LoseBySteam = True

                if UsingWeb == True:
                    UsingWeb = False
                    inUse = False
                    
                if UsingWaterCoolerSoda == True:
                    UsingWaterCoolerSoda = False
                    GotSoda = False
                    GotWaterMoney = True
                    Money += 5
                    inUse = False
                    
                if UsingEmptyCooler == True:
                    UsingEmptyCooler = False
                    inUse = False
                    
                if UsingPurse == True:
                    UsingPurse = False
                    GotPurseMoney = True
                    inUse = False
                    Money += 5
                    
                if UsingEmptyPurse == True:
                    UsingEmptyPurse = False
                    inUse = False
                    
                if UsingLottery == True:
                    if LotteryChance == 1:
                        #Money += 100
                        WonLottery = True
                    else:
                        UsingLottery = False
                        #inUse = False
                        LostLottery = True
                        Money -= 1
                        if Money <=0:
                            LoseByLottery = True
                        
                if LostLottery == True:
                    LostLottery = False
                    inUse = False
                    
                if UsingCarpet == True:
                    UsingCarpet = False
                    inUse = False
                    GotCarpetMoney = True
                    Money += 10
                    
                if UsingBoard == True:
                    UsingBoard = False
                    inUse = False
                    if GotBoardMoney == False:
                        KnowsAboutNail = True
                    if HasHammer == True:
                        if GotBoardMoney == False:
                            Money += 30
                            GotBoardMoney = True
                            KnowsAboutNail = False
                    
                if UsingToolBox == True:
                    UsingToolBox = False
                    inUse = False
                    if KnowsAboutNail == True:
                        HasHammer = True
                        KnowsAboutNail = False
                if UsingPoster == True:
                    UsingPoster = False
                    inUse = False
                    if Money >= 55:
                        Money += 45
                    
            if keys[pygame.K_2]:
                
                if UsingToilet == True:
                    UsingToilet = False
                    Money = 0
                    inUse = False
                    ThrewAwayMoney = True
                    
                if UsingVendingMachine == True:
                    UsingVendingMachine = False
                    inUse = False
                if UsingLottery == True:
                    UsingLottery = False
                    inUse = False
                    
            if keys[pygame.K_3]:

                if UsingToilet == True:
                    inUse = False
                    UsingToilet = False
                
    if keys[pygame.K_SPACE]:
        startScreen = False
        
    

    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            
            if   event.key == K_ESCAPE: return False

    return True




def overlay(): #Overlay code. For HUDS, menus, etc. Is drawn after the draw function.
    global Money


    
    if devmode is True:
        drawText("You Only Get One Dollar", 0, 22, False)
    drawText("Money: " + "$" + str(Money), 5, 0, True)

    if WonLottery == True:
        surface.blit(WinScreenLottery, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True

    if LoseByLottery == True:
        surface.blit(GameOverScreenLottery, (0,0))
        inUse = True
        pygame.mixer.music.fadeout(1000)

    if LoseBySoda == True:
        surface.blit(GameOverScreenSoda, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True
    
    if startScreen == True:
        surface.blit(start_screen, (0,0))
        
    #if Money <= 0:
        #surface.blit(GameOverScreen, (0,0))
        #inUse = True
        
    if TimesPissed >= 6:
        surface.blit(GameOverScreenPiss, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True
        
    if LoseBySteam == True:
        surface.blit(GameOverScreenSteam, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True
        
    if Money >= 100:
        surface.blit(WinScreen, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True
    if ThrewAwayMoney == True:
        surface.blit(GameOverScreenDrain, (0,0))
        pygame.mixer.music.fadeout(1000)
        inUse = True

        

def draw():

    #surface.fill((108,205,224))
    #surface.blit(get_image('images/test_image.jpg'), (20, 20))
    
    


    global playerFrame
    global COLLIDED_RIGHT
    global COLLIDED_LEFT
    global COLLIDED_UP
    global COLLIDED_DOWN
    global ScaleFactorWidth
    global ScaleFactorHeight

    #Hacky desk colisions
    LeftSide = pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1050, scaleFactorHeight * 700,10,200), 0)
    TopSide = pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1050, scaleFactorHeight * 695,390 * scaleFactorWidth,10 * scaleFactorHeight), 0)
    RightSide = pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1440, scaleFactorHeight * 700,10 * scaleFactorWidth ,78 * scaleFactorHeight), 0)
    DownTopSide = pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1100, scaleFactorHeight * 775,340 * scaleFactorWidth,10 * scaleFactorHeight), 0)
    DownLeftSide = pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1135, scaleFactorHeight * 750,10 * scaleFactorWidth,200 * scaleFactorHeight), 0)
    
    playerFrame = random.randint(1, 3)
    
    playerRect = pygame.draw.rect(surface, (255,255,255), (playerX - 45,playerY - 35,75 * scaleFactorWidth,75 * scaleFactorHeight), 0)

    surface.blit(bg, (0,0)) #Resized background





    blitImage("player" + str(playerFrame) + ".png", playerX - 75, playerY - 200)


    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1335,screen_size[1] / 2,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1125,scaleFactorHeight * 470,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 359, scaleFactorHeight * 472,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 359, scaleFactorHeight * 472,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 75, scaleFactorHeight * 472,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1171, scaleFactorHeight * 814,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 955, scaleFactorHeight * 814,130,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 1371, scaleFactorHeight * 650,130,130), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 600, scaleFactorHeight * 650,130,130), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 257, scaleFactorHeight * 470,70,50), 0)
    #pygame.draw.rect(surface, (255,0,0), (scaleFactorWidth * 925, scaleFactorHeight * 470,70,50), 0)


    if LeftSide.colliderect(playerRect):
        COLLIDED_RIGHT = True
    else:
        COLLIDED_RIGHT = False

    if TopSide.colliderect(playerRect):
        COLLIDED_DOWN = True
    else:
        COLLIDED_DOWN = False

    if RightSide.colliderect(playerRect) or DownLeftSide.colliderect(playerRect):
        COLLIDED_LEFT = True
    else:
        COLLIDED_LEFT = False

    if DownTopSide.colliderect(playerRect):
        COLLIDED_UP = True
    else:
        COLLIDED_UP = False
    
    if UsingVendingMachine == True:
        textBox("Do you want to buy a soda for $1?","1 = Yes", "2 = No", False)
        
    if UsingToilet == True:
        textBox("1 = The company now pays $1 each time you take a piss. Take a piss.","2 = Put all of your money in toilet.", "3 = Do nothing.", False)

    if UsingWaterCooler == True:
        textBox("The cooler's empty, but there is 5 dollars at the bottom!","It's just out of my reach.", "1 = Continue", False)

    if UsingBossDoor == True:
        textBox("Cheap bastard.", "1 = Continue", "", False)
        
    if UsingPC == True:
        textBox("You turn on the computer to find a steam sale is on.", "You lose all your money. I hope the games are worth it!", "1 = Continue", False)

    if UsingWaterCoolerSoda == True:
        textBox("You pour in the soda", " and the 5 dollar bill rises enough for you to grab it!", "1 = Continue", False)

    if UsingEmptyCooler == True:
        textBox("The cooler has a small soda puddle at the bottom.", "1 = Continue", "", False)

    if UsingLottery == True:
        textBox("Enter Lottery? If you don't win, you can't feed your family!", "1 = Yes", "2 = No", False)

    if UsingPurse == True:
        textBox("This purse has $5 in it.", "I'm sure no one will miss it.", "1 = Continue", False)

    if UsingEmptyPurse == True:
        textBox("An empty purse.", "1 = Continue", "", False)

    if UsingCarpet == True:
        textBox("You found $10 under the rug!", "What a stupid place to put money.", "1 = Continue", False)

    if UsingBoard == True:
        if HasHammer == True:
            if GotBoardMoney == True:
                textBox("A pin board filled with shit routines and deathly deadlines.", "1 = Continue", "", False)
            else:
                textBox("You use the hammer to take the nail out.", "You get the $30 from the board.", "1 = Continue", False)
        else:
            textBox("There is money nailed to this board", "with a note saying \"life saivings plees do not steel\"", "1 = Continue", False)

    if UsingToolBox == True:
        if KnowsAboutNail == True:
            textBox("Theres a hammer in the toolbox.", "You take the hammer with you.", "1 = Continue", False)
        else:
            textBox("It's a toolbox.", "1 = Continue", "", False)

    if UsingPoster == True:
        if Money >= 55:
            textBox("Hey wait a minute... Theres a safe behind this poster!", "It's marked \"Game Budget\" and it has $45 in it!", "1 = Continue", False)
        else:
            textBox("A poster that the companys put up to \"Boost Morale\".", "1 = Continue", "", False)

def main(): #Main code. Needs clearing up.
    
    global clock
    clock = pygame.time.Clock()
    
    random.seed()
    
    while True:
        if not get_input(): break
        
        draw()
        
        if devmode is True:
            framecounter()
        
        overlay()
        
        pygame.display.flip()
        
        clock.tick(60)
        
    if devmode is True:
        print('Cache cleared.')
    pygame.quit()

        
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
