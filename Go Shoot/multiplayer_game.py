import pygame

pygame.init()

display_width = 800
display_height = 600

font = pygame.font.Font('Exo-Regular.otf', 54)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Multiplayer Go Shoot!')
clock = pygame.time.Clock()
crashed = False
reset = False

tankImg = [pygame.image.load('tank_up.png'), pygame.image.load('tank_down.png'), pygame.image.load('tank_left.png'), pygame.image.load('tank_right.png')]
bulletImg = [pygame.image.load('bullet_up.png'), pygame.image.load('bullet_down.png'), pygame.image.load('bullet_left.png'), pygame.image.load('bullet_right.png')]
mapImg = pygame.image.load('map.png')
diedImg = pygame.image.load('died.jpg')
expImg = pygame.image.load('exp.png')

tankls = [] #[x, y, xc, yc, facing, bulletN]
bulletls = [] #[uid, x, y, facing]

def createBullet(uid, tankls):
    tankData = tankls[uid]
    posx = tankData[0]
    posy = tankData[1]
    facing = tankData[4]
    if facing == 0: posy += -15; posx += 35
    if facing == 1: posy += 65; posx += 35
    if facing == 2: posx += -15; posy += 35
    if facing == 3: posx += 65; posy += 35
    ls = [uid, posx,posy,facing]
    bulletls.append(ls)
    return bulletls

def updateBullet(bullet):
        newBullet = []
        for i in range(len(bullet)):
            bulletData = bullet[i]
            uid = bulletData[0]
            posx = bulletData[1]
            posy = bulletData[2]
            facing = bulletData[3]
            if posx <= display_width+200 or posy <= display_height+200 and posx >= -200 or posy >= -200:
                if facing == 0: posy += -15
                if facing == 1: posy += 15
                if facing == 2: posx += -15
                if facing == 3: posx += 15
                overrideData = [uid, posx, posy, facing]
                newBullet.append(overrideData)
        bullet = []
        for i in newBullet: bullet.append(i)
        for i in bullet:
            bulletData = i
            posx = bulletData[1]
            posy = bulletData[2]
            facing = bulletData[3]
            gameDisplay.blit(bulletImg[facing], (posx, posy))
        return bullet

def checkBullet(bulletls):
    tank0 = []
    tank1 = []
    t0p = tankls[0]
    t1p = tankls[1]
    t0d = False
    t1d = False
    for dat in bulletls:
        if dat[0] == 0: tank0.append(dat)
        if dat[0] == 1: tank1.append(dat)

    for i in tank0:
        bulletData = i
        posx = bulletData[1]
        posy = bulletData[2]
        facing = bulletData[3]
        for m in range(90):
            if posx+(-10-m) == t1p[0]:
                for e in range(90):
                    if posy+(-10-e) == t1p[1]:
                        gameDisplay.blit(expImg, (t1p[0]+25, t1p[1]+25))
                        pygame.display.update()
                        t1d = True
    for i in tank1:
        bulletData = i
        posx = bulletData[1]
        posy = bulletData[2]
        facing = bulletData[3]
        for m in range(90):
            if posx+(-10-m) == t0p[0]:
                for e in range(90):
                    if posy+(-10-e) == t0p[1]:
                        gameDisplay.blit(expImg, (t0p[0]+25, t0p[1]+25))
                        pygame.display.update()
                        t0d = True
    dead = [t0d,t1d]
    return dead
def renderNBullet(n):
    for i in range(n-1): gameDisplay.blit(bulletImg[0],((i*20)+20,20))

def changePos(tank, uid, xc, yc, facing):
    tankData = tank[uid]
    if xc != 'p': tankData[2] = xc
    if yc != 'p': tankData[3] = yc
    if facing != 'p': tankData[4] = facing
    tank[uid] = tankData
    return tank

def updateTank(tankls):
    for uid in range(len(tankls)):
        tankData = tankls[uid]
        tankData[0] += tankData[2]
        tankData[1] += tankData[3]
        tankls[uid] = tankData
    for tankData in tankls: gameDisplay.blit(tankImg[tankData[4]], (tankData[0],tankData[1]))
    if tankls == []: tankls = [[360,500,0,0,0,5],[360,0,0,0,1,5]]
    return tankls

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                tankls = changePos(tankls, 0, 5, 'p', 3)
            if event.key == pygame.K_a:
                tankls = changePos(tankls, 0, -5, 'p', 2)
            if event.key == pygame.K_s:
                tankls = changePos(tankls, 0, 'p', 5, 1)
            if event.key == pygame.K_w:
                tankls = changePos(tankls, 0, 'p', -5, 0)
            if event.key == pygame.K_q:
                bulletls = createBullet(0, tankls)

            if event.key == pygame.K_l:
                tankls = changePos(tankls, 1, 5, 'p', 3)
            if event.key == pygame.K_j:
                tankls = changePos(tankls, 1, -5, 'p', 2)
            if event.key == pygame.K_k:
                tankls = changePos(tankls, 1, 'p', 5, 1)
            if event.key == pygame.K_i:
                tankls = changePos(tankls, 1, 'p', -5, 0)
            if event.key == pygame.K_u:
                bulletls = createBullet(1, tankls)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                tankls = changePos(tankls, 0, 0, 'p', 3)
            if event.key == pygame.K_a:
                tankls = changePos(tankls, 0, 0, 'p', 2)
            if event.key == pygame.K_s:
                tankls = changePos(tankls, 0, 'p', 0, 1)
            if event.key == pygame.K_w:
                tankls = changePos(tankls, 0, 'p', 0, 0)

            if event.key == pygame.K_l:
                tankls = changePos(tankls, 1, 0, 'p', 3)
            if event.key == pygame.K_j:
                tankls = changePos(tankls, 1, 0, 'p', 2)
            if event.key == pygame.K_k:
                tankls = changePos(tankls, 1, 'p', 0, 1)
            if event.key == pygame.K_i:
                tankls = changePos(tankls, 1, 'p', 0, 0)
        ######################

    gameDisplay.blit(mapImg, (0,0))
    bulletls = updateBullet(bulletls)
    tankls = updateTank(tankls)

    if checkBullet(bulletls)[0]:
        pygame.time.delay(500)
        gameDisplay.fill((0,0,0))
        text = font.render("IJKL Win!", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)-250)
        gameDisplay.blit(text, textRect)
        pygame.display.update()
        pygame.time.delay(2000)
        tankls = [[360,500,0,0,0,5],[360,0,0,0,1,5]]
        bulletls = []
        while not reset:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN: reset = True
        reset = False
    if checkBullet(bulletls)[1]:
        pygame.time.delay(500)
        gameDisplay.fill((0,0,0))
        text = font.render("WASD Win!", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, display_height // 2)
        gameDisplay.blit(text, textRect)
        pygame.display.update()
        pygame.time.delay(2000)
        tankls = [[360,500,0,0,0,5],[360,0,0,0,1,5]]
        bulletls = []
        while not reset:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN: reset = True
        reset = False
    pygame.display.update()
    clock.tick(50)
pygame.quit()
quit()
