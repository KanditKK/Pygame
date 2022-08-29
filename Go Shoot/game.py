import pygame as pg

pg.init()

display_width = 800
display_height = 600

gameDisplay = pg.display.set_mode((display_width,display_height))
pg.display.set_caption('Go Shoot!')
font = pg.font.Font('Exo-Regular.otf', 54)
font2 = pg.font.Font('Exo-Regular.otf', 32)
text = font.render("0", True, (255,255,255))
textRect = text.get_rect()
textRect.center = (display_width // 2, (display_height // 2)+400)
clock = pg.time.Clock()
isCrashed = False
score = 0
tankposx =  (display_width * 0.45)
tankposy = (display_height * 0.8)
tankposx_change = 0
tankposy_change = 0
tankFacing = 0 #tankImg indetankposx
n = 0
bulletN = 6
bullet = []
reset = False

def createBullet(posx, posy, facing):
    age = 0
    if facing == 0: posy += -15; posx += 35
    if facing == 1: posy += 65; posx += 35
    if facing == 2: posx += -15; posy += 35
    if facing == 3: posx += 65; posy += 35
    ls = [posx,posy,facing,age]
    bullet.append(ls)

def updateBullet(bullet):
        for i in range(len(bullet)):
            bulletData = bullet[i]
            posx = bulletData[0]
            posy = bulletData[1]
            facing = bulletData[2]
            if posx >= display_width+200 or posy >= display_height+200 or posx <= -200 or posy <= -200:
                if facing == 0: posy = display_height + 100
                if facing == 1: posy = -100
                if facing == 2: posx = display_width + 100
                if facing == 3: posx = -100
            else:
                if facing == 0: posy += -15
                if facing == 1: posy += 15
                if facing == 2: posx += -15
                if facing == 3: posx += 15
            age = bulletData[3]+1
            overrideData = [posx, posy, facing, age]
            bullet[i] = overrideData
        for i in bullet:
            bulletData = i
            posx = bulletData[0]
            posy = bulletData[1]
            facing = bulletData[2]
            age = bulletData[3]
            gameDisplay.blit(bulletImg[facing], (posx, posy))
def checkBullet(bullet,f):
    dead = False
    for i in bullet:
        bulletData = i
        posx = bulletData[0]
        posy = bulletData[1]
        facing = bulletData[2]
        age = bulletData[3]
        if age > 5:
            for m in range(90):
                if posx+(-10-m) == tankposx:
                    for e in range(90):
                        if posy+(-10-e) == tankposy:
                            dead = True
    return dead

def renderBulletN(n):
    n -= 1
    if n == 5:
        gameDisplay.blit(bulletImg[0],(20,20))
        gameDisplay.blit(bulletImg[0],(40,20))
        gameDisplay.blit(bulletImg[0],(60,20))
        gameDisplay.blit(bulletImg[0],(80,20))
        gameDisplay.blit(bulletImg[0],(100,20))
    if n == 4:
        gameDisplay.blit(bulletImg[0],(20,20))
        gameDisplay.blit(bulletImg[0],(40,20))
        gameDisplay.blit(bulletImg[0],(60,20))
        gameDisplay.blit(bulletImg[0],(80,20))
    if n == 3:
        gameDisplay.blit(bulletImg[0],(20,20))
        gameDisplay.blit(bulletImg[0],(40,20))
        gameDisplay.blit(bulletImg[0],(60,20))
    if n == 2:
        gameDisplay.blit(bulletImg[0],(20,20))
        gameDisplay.blit(bulletImg[0],(40,20))
    if n == 1:
        gameDisplay.blit(bulletImg[0],(20,20))

tankImg = [pg.image.load('tank_up.png'), pg.image.load('tank_down.png'), pg.image.load('tank_left.png'), pg.image.load('tank_right.png')]
bulletImg = [pg.image.load('bullet_up.png'), pg.image.load('bullet_down.png'), pg.image.load('bullet_left.png'), pg.image.load('bullet_right.png')]
mapImg = pg.image.load('map.png')
diedImg = pg.image.load('died.jpg')
expImg = pg.image.load('exp.png')
while not isCrashed:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isCrashed = True

        ############################
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                tankposx_change = 5
                tankFacing = 3
            elif event.key == pg.K_a:
                tankposx_change = -5
                tankFacing = 2
            elif event.key == pg.K_s:
                tankposy_change = 5
                tankFacing = 1
            elif event.key == pg.K_w:
                tankposy_change = -5
                tankFacing = 0
            elif event.key == pg.K_SPACE:
                if bulletN > 1:
                    createBullet(tankposx, tankposy, tankFacing)
                    score += 1
                    bulletN -= 1
            elif event.key == pg.K_r:
                bulletN = 6;
        if event.type == pg.KEYUP and (event.key == pg.K_w or event.key == pg.K_a or event.key == pg.K_s or event.key == pg.K_d): tankposx_change = 0; tankposy_change = 0
        ######################
    if tankposx <= 137 and tankFacing == 2:
        tankposx = 130
    elif tankposx >= 612 and tankFacing == 3:
        tankposx = 619
    else :
        tankposx+= tankposx_change

    tankposy += tankposy_change
    if tankposx >= display_width+200: tankposx = -100
    if tankposy >= display_width+200: tankposy = -100
    if tankposx <= -200 : tankposx = display_width+100
    if tankposy <= -200 : tankposy = display_height+100
    gameDisplay.blit(mapImg, (0,0))
    updateBullet(bullet);
    renderBulletN(bulletN);
    gameDisplay.blit(tankImg[tankFacing], (tankposx,tankposy))
    if checkBullet(bullet,tankFacing):
        gameDisplay.blit(expImg, (tankposx+25, tankposy+25))
        pg.display.update()
        pg.time.delay(500)
        maxtxt = open('score.txt', 'r')
        max = int(str(maxtxt.readline()))
        maxtxt.close()
        if score > max:
            maxtxt = open('score.txt', 'w')
            maxtxt.write(str(score))
            maxtxt.close()
            max = score
        gameDisplay.blit(diedImg, (0,0))
        text = font.render("Score: "+str(score), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)-250)
        gameDisplay.blit(text, textRect)
        text = font2.render("Max Score: "+str(max), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (display_width // 2, (display_height // 2)-200)
        gameDisplay.blit(text, textRect)
        pg.display.update()
        pg.time.delay(2000)
        tankposx =  (display_width * 0.45)
        tankposy = (display_height * 0.8)
        tankFacing = 0
        bullet = []
        bulletN = 6
        while not reset:
            for ev in pg.event.get():
                if ev.type == pg.KEYDOWN: reset = True
        reset = False
        score = 0
        tankposx_change = 0
        tankposy_change = 0
    pg.display.update()
    clock.tick(50)
    if n == 50:
        n = 0;
        if bulletN <= 5:
            bulletN += 1
    n+= 1
pg.quit()
quit()
