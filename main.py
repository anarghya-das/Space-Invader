import pygame
import random
import math
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMAGE_SIZE = 64
score = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("back.jpg")
bullet = pygame.image.load("bullet.png")
bullet_fired = False
bulletX = 0
bulletY = 0
bullet_speed = 10
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerX_change_value = 3

enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 800-IMAGE_SIZE)
enemyY = random.randint(50, 150)
enemyX_change_value = 4
enemyY_change = 20
enemyX_change = enemyX_change_value


def Enemy(x, y):
    screen.blit(enemyImg, (x, y))


def Player(x, y):
    screen.blit(playerImg, (x, y))


def boundary_check(x_cord):
    offset = SCREEN_WIDTH-IMAGE_SIZE
    if x_cord <= 0:
        return 0
    elif x_cord >= offset:
        return offset
    else:
        return x_cord


def enemy_update(x, change, y):
    x += change
    offset = SCREEN_WIDTH-IMAGE_SIZE
    if x <= 0:
        change = enemyX_change_value
        x = 0
        y += enemyY_change
    elif x >= offset:
        change = -enemyX_change_value
        x = offset
        y += enemyY_change
    return x, change, y


def fire_bullet(x, y):
    global bullet_fired
    bx = x
    by = y-IMAGE_SIZE
    screen.blit(bullet, (bx, by))
    bullet_fired = True
    return bx, by


def update_bullet(x, y):
    screen.blit(bullet, (x, y))


def collision(b_x, b_y, e_x, e_y):
    d = math.sqrt(math.pow((b_x-e_x), 2)+math.pow((b_y-e_y), 2))
    if d <= IMAGE_SIZE:
        return True
    else:
        return False


running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerX_change_value
            if event.key == pygame.K_RIGHT:
                playerX_change = playerX_change_value
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if not bullet_fired:
                    bulletX, bulletY = fire_bullet(playerX, playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    playerX = boundary_check(playerX)
    enemyX, enemyX_change, enemyY = enemy_update(enemyX, enemyX_change, enemyY)
    if bullet_fired:
        if bulletY <= 0 or collision(bulletX, bulletY, enemyX, enemyY):
            bullet_fired = False
        else:
            bulletY -= bullet_speed
            update_bullet(bulletX, bulletY)
    if collision(bulletX, bulletY, enemyX, enemyY):
        score += 1
        enemyX = random.randint(0, 800-IMAGE_SIZE)
        enemyY = random.randint(50, 150)
        print(score)
    Enemy(enemyX, enemyY)
    Player(playerX, playerY)

    pygame.display.update()
