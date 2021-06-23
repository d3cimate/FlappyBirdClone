#! /usr/bin/env python3
import pygame
import sys
import random

def drawFloor():
    window.blit(floor,(floorPos,900))
    window.blit(floor,(floorPos + 576,900))

def drawPipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            window.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            window.blit(flipPipe, pipe)

def createPipe():
    randPipe = random.choice(pipeHeight)
    botPipe = pipeSurface.get_rect(midtop = (600, randPipe))
    topPipe = pipeSurface.get_rect(midbottom = (600, randPipe - 300))
    return botPipe, topPipe 

def movePipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visiblePipes = [pipe for pipe in pipes if pipe.right > -50]
    return visiblePipes

def hasCollided(pipes):
    global canScore
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            canScore = True
            return False
    
    if birdRect.top <= -100 or birdRect.bottom >= 900:
        deathSound.play()
        canScore = True
        return False

    return True

def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMove * 3, 1)
    return newBird

def birdAnim():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (100,birdRect.centery))
    return newBird, newBirdRect

def displayScore(gameState):
    if gameState == "main_game":
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        window.blit(scoreSurface, scoreRect)

    if gameState == "game_over":
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        window.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center = (288, 850))
        window.blit(highScoreSurface, highScoreRect)

    if gameState == "starting":
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        window.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center = (288, 850))
        window.blit(highScoreSurface, highScoreRect)

def getHighscore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

def scoreCheck():
    global score, canScore
    if pipeList:
        for pipe in pipeList:
            if 95 < pipe.centerx < 105 and canScore:
                score += 1
                scoreSound.play()
                canScore = False
            if pipe.centerx < 0:
                canScore = True

# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
# ^ incase of sound issues through pygame version < 2.0
pygame.init()
window = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.TTF', 40)

flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
deathSound = pygame.mixer.Sound('sound/sfx_hit.wav')
scoreSound = pygame.mixer.Sound('sound/sfx_point.wav')

gravity = 0.2
birdMove = 0
inGame = False
hasStarted = False
canScore = True
score = 0
highScore = 0

getReady = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
getReadyRect = getReady.get_rect(center = (288, 512))

gameOver = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
gameOverRect = getReady.get_rect(center = (288, 512))

background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)

floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale2x(floor)
floorPos = 0

birdDownflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
birdMidflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
birdUpflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownflap, birdMidflap, birdUpflap]
birdIndex = 0
bird = birdFrames[birdIndex]
birdRect = bird.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 2000)

pipeSurface = pygame.image.load('assets/pipe-green.png').convert()
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipeHeight = [400, 600, 800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and inGame:
                birdMove = 0
                birdMove -= 8
                flapSound.play()
            if event.key == pygame.K_SPACE and inGame == False and hasStarted:
                inGame = True
                pipeList.clear()
                birdRect.center = (100, 512)
                birdMove = 0
                score = 0
            if event.key == pygame.K_SPACE and inGame == False and hasStarted == False:
                inGame = True
                pipeList.clear()
                birdRect.center = (100, 512)
                birdMove = 0
                score = 0
                hasStarted = True
        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())
        if event.type == BIRDFLAP:
            if birdIndex > 2:
                birdIndex += 1
            else:
                birdIndex = 0
            bird, birdRect = birdAnim()

    window.blit(background,(0,0))

    if inGame:
        birdMove += gravity
        rotatedBird = rotateBird(bird)
        birdRect.centery += birdMove

        window.blit(rotatedBird,birdRect)
        inGame = hasCollided(pipeList)

        pipeList = movePipe(pipeList)
        drawPipe(pipeList)
        scoreCheck()
        displayScore('main_game')
        # if (score - int(score)) == 0:
        #     scoreSound.play()
        # if score.is_integer:
        #     scoreSound.play()
        # scoreCount -= 1
        # if scoreCount <= 0:
        #     scoreSound.play()
        #     scoreCount = 100
    elif hasStarted == False:
        window.blit(getReady, getReadyRect)
        highScore = getHighscore(score,highScore)
        displayScore('starting')
    # elif inGame == False and hasStarted == False:
    #     window.blit(getReady, getReadyRect)
    #     highScore = getHighscore(score,highScore)
    #     displayScore('starting')
    elif inGame == False and hasStarted == True:
        window.blit(gameOver, gameOverRect)
        highScore = getHighscore(score,highScore)
        displayScore('starting')

    floorPos -= 1
    drawFloor()
    if floorPos <= -576:
        floorPos = 0

    pygame.display.update()
    clock.tick(120)