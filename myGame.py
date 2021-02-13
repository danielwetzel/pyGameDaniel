import pygame
import player
import enemy
import attackParticles
import sys
import random
import menus
import enemyList
import time

#load font
font = pygame.font.SysFont(None, 30)

#Textures
background = pygame.image.load("textures/background.png")
backPanel = pygame.image.load("textures/panel.png")
lostImg = pygame.image.load("textures/lost.png")
wonImg = pygame.image.load("textures/win.png")
lvlUp = pygame.image.load("textures/lvlUp.png")
skipImg = pygame.image.load("textures/skip.png")
evolveImg = pygame.image.load("textures/evolveMessage.png")
startImg = pygame.image.load("textures/start.png")
selectGreyImg = pygame.image.load("textures/selectGrey.png")
selectYellowImg = pygame.image.load("textures/selectYellow.png")
startGreyImg = pygame.image.load("textures/startGrey.png")
resetImg = pygame.image.load("textures/reset.png")
lockImg = pygame.image.load("textures/locked.png")
num1img = pygame.image.load("textures/1.png")
num2img = pygame.image.load("textures/2.png")
num3img = pygame.image.load("textures/3.png")
pwrUp = pygame.image.load("textures/pwrUp.png")
tradeImg = pygame.image.load("textures/trade.png")
exitButton = pygame.image.load("textures/exit.png")
tradeInMessage = pygame.image.load("textures/tradeInMsg.png")
powerUpMsg = pygame.image.load("textures/powerUpMsg.png")

#Screen Size
screen_width = 1200
screen_backImg = 600
screen_panel = 225
screen_height = screen_backImg + screen_panel

#Sounds
winningSound = pygame.mixer.Sound("sounds/victory.wav")
losingSound = pygame.mixer.Sound("sounds/losing.wav")

#Variables
fps = 60
selectionTime = 30

#Player's Monster Selection
firstMonstNr = 0
secondMonstNr = 0
lastMonstNr = 0

difficulty = 0

#Enemy's monster selection
eFirstMonstNr = 0
eSecondMonstNr = 0
eLastMonstNr = 0

#Set the amount of time the game idles after every action
waitingAmount = 120

rounds = 1

gameStage = 0

screen = pygame.display.set_mode([screen_width, screen_height])

turnOrder = []


def new():
    global won
    global lost
    global gameStage
    global firstMonstNr, secondMonstNr, lastMonstNr

    global eFirstMonstNr, eSecondMonstNr, eLastMonstNr

    won = False
    lost = False

    player.setMonsters(firstMonstNr, secondMonstNr, lastMonstNr)
    enemy.setMonsters(eFirstMonstNr, eSecondMonstNr, eLastMonstNr)

    gameStage = 1

    run()


def printScreen():
    screen.blit(background, (0, 0))
    screen.blit(backPanel, (0, screen_backImg))

    if gameStage == 0:
        screen.blit(evolveImg, (200, 100))
        screen.blit(skipImg, (screen_width - 220, 20))

    if gameStage == 1:
        screen.blit(powerUpMsg, (200, 100))

    if gameStage == 3:
        screen.blit(tradeInMessage, (200, 100))
        screen.blit(skipImg, (screen_width - 220, 20))

    player.printPlayerMonsters()
    enemy.printEnemyMonsters()
    for a in attackParticles.currentParticles:
        a.printAttack()


def run():
    global waitingAmount
    global turnOrder
    global rounds
    global gameStage

    selTime = selectionTime
    frames = 0

    mbDown = False

    gameStage = 1

    waitingCounter = 0

    clock = pygame.time.Clock()

    player.setMonsters(firstMonstNr, secondMonstNr, lastMonstNr)
    enemy.setMonsters(eFirstMonstNr, eSecondMonstNr, eLastMonstNr)

    if random.randint(0,1) == 0:
        playerTurn = 0
    else:
        playerTurn = 1

    go = True

    while go:

        pygame.display.set_caption(f'WIP Project: pyGame by Daniel Wetzel - Battle Simulator - Round: {rounds}')

        for event in pygame.event.get():
            #Close the game
            if event.type == pygame.QUIT: sys.exit()

            #Player clicked Mouse Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbDown = True
            else:
                mbDown = False

        attackParticles.hanldeAttacks()
        printScreen()

        if playerTurn > 1:
            playerTurn = 0

        if player.isDead():
            #go = False
            screen.fill((100,100,100))
            screen.blit(lostImg, (350, 165))
            pygame.display.update()
            pygame.mixer.Sound.play(losingSound)
            time.sleep(3)
            menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])

        elif enemy.isDead():
            #go = False
            screen.fill((200,200,200))
            screen.blit(wonImg, (350, 165))
            pygame.display.update()
            pygame.mixer.Sound.play(winningSound)
            time.sleep(3)
            rounds += 1
            gameStage = 3
            frames = 0
            set_Enemy(difficulty)
            player.restore()
            enemy.restore()

        #Switch Monster (random)
        elif gameStage == 3:

            #Only alow trade in after round 5 and after that in every 2nd round
            if rounds >= 5 and rounds % 2 != 0:
                # Render the Seconds
                seconds = int(frames / fps)
                secondsRender = font.render(f'{(selTime - seconds)} Seconds left', True, (0, 0, 0))

                # Show Seconds
                screen.blit(secondsRender, (20, 20))

                sButton = pygame.Rect(screen_width - 220, 20, 200, 100)

                # show mouse
                pygame.mouse.set_visible(True)

                # get mouse position
                mousePos = pygame.mouse.get_pos()

                # if mouse is on one of the players monsters
                for pMonst in player.monsterList:

                    if pMonst.rect.collidepoint(mousePos):

                        # hide normal mouse
                        pygame.mouse.set_visible(False)

                        # Show LVL Up symbol
                        screen.blit(tradeImg, mousePos)

                        # Player clicked on the monster
                        if mbDown:

                            # Try to evolve the monster
                            selectedMonst = pMonst.switchRandom(rounds)

                            # Monster could be evolved
                            if selectedMonst:
                                gameStage = 1
                                menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])

                if sButton.collidepoint(mousePos):

                    # set cursor to a hand
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                    # Player clicked on the Button
                    if mbDown:
                        # Player wants to skip
                        gameStage = 1
                        menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])

                else:
                    # set normal cursor
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


                if seconds >= selTime:
                    # Players time runs up
                    gameStage = 1
                    menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])

            else:
                gameStage = 0


        #Battle Phase
        if gameStage == 2:

            # hide normal mouse
            pygame.mouse.set_visible(False)


            if  waitingCounter > waitingAmount:

                if player.isAttacking() == False:

                    if enemy.isAttacking() == False:

                        if playerTurn == 0:
                            target = enemy.getNextTarget()
                            player.attack(target)
                        elif playerTurn == 1:
                            target = player.getNextTarget()
                            enemy.attack(target)

                        playerTurn += 1
                        waitingCounter = 0

            waitingCounter += 1

        #Choose special Attacker
        elif gameStage == 1:
            # Render the Seconds
            seconds = int(frames / fps)
            secondsRender = font.render(f'{(selTime - seconds)} Seconds left', True, (0, 0, 0))

            #Show Seconds
            screen.blit(secondsRender,(20,20))

            #show mouse
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            #get mouse position
            mousePos = pygame.mouse.get_pos()

            #if mouse is on one of the players monsters
            for pMonst in player.monsterList:

                if pMonst.rect.collidepoint(mousePos):

                    #hide normal mouse
                    pygame.mouse.set_visible(False)

                    #Show LVL Up symbol
                    screen.blit(pwrUp, mousePos)

                    #Player clicked on the monster
                    if mbDown:

                        pMonst.turnSpecialAttacker()
                        enemy.monsterList[2].turnSpecialAttacker()
                        gameStage = 2

            if seconds >= selTime:
                #The player gets punished for not selecting in time.
                #Remove "#" to give him power up after the time is up

                #player.monsterList[2].turnSpecialAttacker()
                enemy.monsterList[2].turnSpecialAttacker()
                gameStage = 2

        #Evolve Monster
        elif gameStage == 0:
            # Render the Seconds
            seconds = int(frames / fps)
            secondsRender = font.render(f'{(selTime - seconds)} Seconds left', True, (0, 0, 0))

            #Show Seconds
            screen.blit(secondsRender,(20,20))

            skipButton = pygame.Rect(screen_width-220, 20, 200, 100)

            #show mouse
            pygame.mouse.set_visible(True)

            #get mouse position
            mousePos = pygame.mouse.get_pos()

            #if mouse is on one of the players monsters
            for pMonst in player.monsterList:

                if pMonst.evolvesTo != -1:

                    if pMonst.rect.collidepoint(mousePos):

                        #hide normal mouse
                        pygame.mouse.set_visible(False)

                        #Show LVL Up symbol
                        screen.blit(lvlUp, mousePos)


                        #Player clicked on the monster
                        if mbDown:

                            #Try to evolve the monster
                            selectedMonst = pMonst.evolve()

                            #Monster could be evolved
                            if selectedMonst:

                                gameStage = 1
                                menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])



            if skipButton.collidepoint(mousePos):

                #set cursor to a hand
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                # Player clicked on the Button
                if mbDown:
                    #Player wants to skip
                    gameStage = 1
                    menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])

            else:
                #set normal cursor
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if seconds >= selTime:
                # Players time runs up
                gameStage = 1
                menus.selectOrder([player.monsterList[0], player.monsterList[1], player.monsterList[2]])


        clock.tick(fps)
        pygame.display.update()
        frames += 1


def set_firstMon(monster, number):
    global firstMonstNr
    firstMonstNr = number

    #Delete obsolete Instance
    del monster


def set_secMon(monster, number):
    global secondMonstNr
    secondMonstNr = number

    #Delete obsolete Instance
    del monster


def set_lastMon(monster, number):
    global lastMonstNr
    lastMonstNr = number

    #Delet Obsolete Instance
    del monster


def set_Enemy(number):

    global eFirstMonstNr, eSecondMonstNr, eLastMonstNr
    global difficulty
    global rounds

    difficulty = number

    eRounds = rounds-1

    enemySelection = enemyList.loadEnemy(difficulty, eRounds)

    eFirstMonstNr= enemySelection[0]
    eSecondMonstNr = enemySelection[1]
    eLastMonstNr = enemySelection[2]
