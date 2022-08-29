import pygame
import random

pygame.init()

displayHeight = 600
displayWidth = 800

font = pygame.font.Font('Exo-Regular.otf', 24)
bigger_font = pygame.font.Font('Exo-Regular.otf', 54)
smaller_font = pygame.font.Font('Exo-Regular.otf', 18)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('PIF - Physics is fun!')
clock = pygame.time.Clock()

fps = 50 #frame per sec.
acceleration = 400 #px/s
firstacc = 400
crashed = False
posy = 0
yc = 0
score = 0
time = 0
latestMax = 600
obstacle = [] #[py, sx, sy]

def generateObstacle():
    obstacle.append([800, random.randint(10,200), random.randint(10,100), random.randint(0,1)])

def updateObstacle(obls):
    global score
    newls = []
    for dat in obls:
        newy = dat[0] - (acceleration/fps)
        if newy > -100: newls.append([newy, dat[1], dat[2], dat[3]])
        else: score+= 1
    return newls

generateObstacle()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: crashed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: yc = 600; time =- (900-latestMax)
    if yc > 0: posy -= int(yc/20); yc -= int(yc/20)
    posy += (firstacc/fps)

    if posy < latestMax: latestMax = posy

    if posy <= 0 : posy = 0; yc = 0
    if posy + 60 >= displayHeight : posy =  displayHeight - 60; yc = 0 - time; time += 50; latestMax = 500
    print(time)
    if time > 0 and pygame.time.get_ticks() % 50 == 0: time += 50
    gameDisplay.fill((255,255,255))
    pygame.draw.rect(gameDisplay, (50,50,50), pygame.Rect(100, posy, 60, 60))
    acceleration = firstacc + (score*10)
    text = font.render('Score: '+str(score), True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (60, 20)
    gameDisplay.blit(text, textRect)
    if pygame.time.get_ticks() % random.randint(30,60) == 0: generateObstacle()
    obstacle = updateObstacle(obstacle)
    for dat in obstacle:
        if dat[3] == 0: pygame.draw.rect(gameDisplay, (150,150,150), pygame.Rect(dat[0], displayHeight - dat[1], dat[2], dat[1]))
        else: pygame.draw.rect(gameDisplay, (150,150,150), pygame.Rect(dat[0], 0, dat[2], dat[1]))
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
quit()
