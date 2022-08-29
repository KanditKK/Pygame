import pygame
import random
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Sky Shooter!')

font = pygame.font.Font('Exo-Regular.otf', 24)
bigger_font = pygame.font.Font('Exo-Regular.otf', 54)
smaller_font = pygame.font.Font('Exo-Regular.otf', 18)
black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
start = False
gameSpeed = 1
score = 0
battleplaneImg = pygame.image.load('battleplane.png')
battleplanespeedImg = pygame.image.load('battleplane_speed.png')
backgroundImg = pygame.image.load('background.jpg')
overlay1Img = pygame.image.load('red.jpg')
overlay2Img = pygame.image.load('green.jpg')
meteorImg = [pygame.image.load('meteor1.png'), pygame.image.load('meteor2.png'), pygame.image.load('meteor3.png')]
bulletImg = pygame.image.load('bullet_up.png')
overlay1Img.set_alpha(75)
overlay2Img.set_alpha(75)
entities = []; bullet = [] #[px, py ,type, xc, yc, subtype]
bullet = [] #[px, py]
x =  (display_width * 0.45)
x_change = 0

def getMessage(type, key):
    if type == 'dead':
        deadType = {'border':'You have experienced kinetic energy.',
                    'hit-by-meteor':'You were hit by some meteoroids.'}
        return deadType[key]

def renderPauseScreen(type, key):
    crashed = False
    if type == 'dead':

        text = font.render(str(key), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)+25)
        gameDisplay.blit(overlay1Img, (0, 0))
        gameDisplay.blit(text, textRect)

        text = font.render('Your Score: '+str(score), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, 50)
        gameDisplay.blit(text, textRect)

        text = bigger_font.render('You died!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)-25)
        gameDisplay.blit(text, textRect)

        text = smaller_font.render('Press Q to quit.', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)+75)
        gameDisplay.blit(text, textRect)

        text = smaller_font.render('Press any key to Restart.', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)+100)
        gameDisplay.blit(text, textRect)

        maxtxt = open('score.txt', 'r')
        max = int(str(maxtxt.readline()))
        maxtxt.close()
        if score > max:
            maxtxt = open('score.txt', 'w')
            maxtxt.write(str(score))
            maxtxt.close()

        pygame.display.update()
        reset = False
        pygame.time.delay(1000)
        while not reset:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_q: crashed = True
                    reset = True

    if type == 'pause':
        gameDisplay.blit(overlay2Img, (0, 0))

        text = bigger_font.render('Paused!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)-25)
        gameDisplay.blit(text, textRect)

        text = smaller_font.render('Press Q to quit.', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)+25)
        gameDisplay.blit(text, textRect)

        text = smaller_font.render('Press any key to Resume.', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)+50)
        gameDisplay.blit(text, textRect)

        pygame.display.update()
        reset = False
        while not reset:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_q: crashed = True
                    reset = True
    return crashed

def generateMeteor(list):
    #new entity [px, py ,type, xc, yc, subtype]
    rdpos = random.randint(10,790)
    rdtype = random.randint(0,2)
    meteorData = [rdpos, -300, 'meteor', 0, 3, rdtype]
    list.append(meteorData)
    return list

def renderEntities(list):
    for edata in list:
        px = edata[0]
        py = edata[1]
        type = edata[2]
        subtype = edata[5]
        gameDisplay.blit(meteorImg[subtype], (px, py))

def updateEntities(list):
    ls = []
    for edata in list:
        px = edata[0]
        py = edata[1]
        if edata[0] <= 800: px += (edata[3]*gameSpeed)
        if edata[1] <= 600: py += (edata[4]*gameSpeed)
        xc = edata[3]
        yc = edata[4] + score/1000
        type = edata[2]
        subtype = edata[5]
        ls.append([px, py, type, xc, yc, subtype])
    return ls

def checkEHitbox(x, list):
    entityHeight = 0
    entityWidth = 0
    for edata in list:
        px = int(edata[0])
        py = int(edata[1])
        type = edata[2]
        subtype = edata[5]
        if type == 'meteor':
            if subtype == 0: entityWidth = 25; entityHeight = 64
            if subtype == 1: entityWidth = 50; entityHeight = 128
            if subtype == 2: entityWidth = 10; entityHeight = 26
            for h in range(58):
                if py + entityHeight == 500 + h:
                    for bw in range(100):
                        for ew in range(entityWidth):
                            if px + ew == x + bw:
                                return True

def checkEntities(list):
    score = 0
    ls = []
    for dat in list: ls.append(dat)
    for i in ls:
        if i[1] > 600:
            score+=1
            entities.remove(i)
    return score

def createBullet(x):
    ls = [x+50,450]
    bullet.append(ls)

def checkBHitbox(bulletlsls, entlsls):
    entityHeight = 0
    entityWidth = 0
    bulletls = []
    entls = []
    bl = 0
    en = 0
    for dat in bulletlsls: bulletls.append(dat)
    for dat in entlsls: entls.append(dat)

    for b in range(len(bulletls)):
        x = bulletls[b][0]
        y = bulletls[b][1]

        for i in range(len(entls)):
            px = int(entls[i][0])
            py = int(entls[i][1])
            type = entls[i][2]
            subtype = entls[i][5]
            if type == 'meteor':
                if subtype == 0: entityWidth = 25; entityHeight = 64
                if subtype == 1: entityWidth = 50; entityHeight = 128
                if subtype == 2: entityWidth = 10; entityHeight = 26
                for h in range(5):
                    if py + entityHeight == y + h:
                        for bw in range(13):
                            for ew in range(entityWidth):
                                if px + ew == x + bw:
                                    print('ent:'+str(i)+', b:'+str(b))
                                    bl = b + 1
                                    en = i + 1
    if bl != 0: del bulletls[bl-1]
    if en != 0: del entls[en-1]

    return [entls, bulletls]

def renderBullet(list):
    for edata in list:
        px = edata[0]
        py = edata[1]
        gameDisplay.blit(bulletImg, (px, py))

def updateBullet(list):
    newls = []
    for dat in list:
        px = dat[0]
        py = dat[1] - 5
        newls.append([px, py])
    return newls














while not start:
    gameDisplay.blit(backgroundImg, (0, 0))
    text = bigger_font.render('Sky Shooter!', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (display_width // 2, (display_height // 2)-25)
    gameDisplay.blit(text, textRect)

    text = smaller_font.render('Press Q to quit.', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (display_width // 2, (display_height // 2)+25)
    gameDisplay.blit(text, textRect)

    text = smaller_font.render('Press any key to start.', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (display_width // 2, (display_height // 2)+50)
    gameDisplay.blit(text, textRect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: crashed = True
            start = True

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        ############################
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                crashed = renderPauseScreen('pause','')
            if event.key == pygame.K_a:
                x_change = -5
            if event.key == pygame.K_d:
                x_change = 5
            if event.key == pygame.K_w:
                gameSpeed = 3
            if event.key == pygame.K_SPACE:
                createBullet(x)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                gameSpeed = 1
        ######################
    ##
    x += x_change
    if x <= 0: crashed = renderPauseScreen('dead', getMessage('dead', 'border')); x = (display_width * 0.45); x_change = 0; entities = []; bullet = []; score = 0; gameSpeed = 1
    if x >= display_width - 100: crashed = renderPauseScreen('dead', getMessage('dead', 'border')); x = (display_width * 0.45); x_change = 0; entities = []; bullet = []; score = 0; gameSpeed = 1
    if score < 50:
        if pygame.time.get_ticks() % 50-score == 0: entities = generateMeteor(entities); score += checkEntities(entities)
    else:
        if pygame.time.get_ticks() % 20 == 0: entities = generateMeteor(entities); score += checkEntities(entities)
    entities = updateEntities(entities)
    bullet = updateBullet(bullet)
    print(bullet)
    gameDisplay.blit(backgroundImg, (0, 0))
    renderEntities(entities)
    renderBullet(bullet)

    if gameSpeed == 1: gameDisplay.blit(battleplaneImg, (x, 450))
    if gameSpeed == 3: gameDisplay.blit(battleplanespeedImg, (x, 450))

    if checkEHitbox(x, entities): crashed = renderPauseScreen('dead', getMessage('dead', 'hit-by-meteor')); x = (display_width * 0.45); x_change = 0; entities = []; bullet = []; score = 0; gameSpeed = 1

    check = checkBHitbox(bullet, entities)
    bullet = check[1]
    entities = check[0]

    maxtxt = open('score.txt', 'r')
    max = int(str(maxtxt.readline()))
    maxtxt.close()

    text = font.render('Score: '+str(score), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (60, 20)
    gameDisplay.blit(text, textRect)

    text = font.render('Max Score: '+str(max), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (680, 20)
    gameDisplay.blit(text, textRect)

    pygame.display.update()
    clock.tick(50)

pygame.quit()
quit()
