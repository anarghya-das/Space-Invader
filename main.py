import pygame
import random
import math
from enemy import EnemyClass

pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMAGE_SIZE = 64
score = 0
font = pygame.font.Font(pygame.font.get_default_font(), 32)
over = pygame.font.Font(pygame.font.get_default_font(), 64)
scoreX, scoreY = 10, 10
overX, overY = 250, 250
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_over = False


def show_score():
    s = font.render(f"Score : {str(score)}", True, (255, 255, 255))
    screen.blit(s, (scoreX, scoreY))


def show_over():
    s = over.render(f"Game Over!", True, (255, 255, 255))
    screen.blit(s, (overX, overY))


pygame.display.set_caption("Space Invaders")
background = pygame.image.load("back.jpg")
bullet = pygame.image.load("bullet.png")
bullet_fired = False
bulletX = 0
bulletY = 0
bullet_speed = 4
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerX_change_value = 4

ENEMY_COUNT = 6
enemies = []
enemyImg = pygame.image.load("enemy.png")
enemyX_change_value = 4
enemyY_change = 20


def create_enemy():
    enemyX = random.randint(0, 800-IMAGE_SIZE)
    enemyY = random.randint(50, 150)
    enemyX_change = enemyX_change_value
    e = EnemyClass(enemyX, enemyY, enemyX_change, enemyY_change)
    return e


for _ in range(ENEMY_COUNT):
    enemies.append(create_enemy())


def Enemy(e):
    screen.blit(enemyImg, (e.x, e.y))


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
    e.set_x(x)
    e.set_y(y)
    e.set_x_change(change)


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
    d = math.sqrt(math.pow(b_x-e_x, 2)+math.pow(b_y-e_y, 2))
    if d < 27:
        return True
    else:
        return False

pressed_left=False
pressed_right=False
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    if game_over:
        show_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left=True
                if event.key == pygame.K_RIGHT:
                    pressed_right=True
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if not bullet_fired:
                        bulletX, bulletY = fire_bullet(playerX, playerY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_left=False
                if event.key == pygame.K_RIGHT:
                    pressed_right=False

        if pressed_left:
            playerX_change = -playerX_change_value
        elif pressed_right:
            playerX_change = playerX_change_value
        else:
            playerX_change = 0

        playerX += playerX_change
        playerX = boundary_check(playerX)
        for e in enemies:
            if collision(e.x, e.y, playerX, playerY):
                game_over = True
                show_over()
                break
            enemy_update(e.x, e.x_change, e.y)
            if bullet_fired:
                if bulletY <= 0:
                    bullet_fired = False
                else:
                    bulletY -= bullet_speed
                    update_bullet(bulletX, bulletY)

            if collision(bulletX, bulletY, e.x, e.y):
                bullet_fired = False
                bulletX = playerX
                bulletY = playerY
                score += 1
                e.set_x(random.randint(0, 800-IMAGE_SIZE))
                e.set_y(random.randint(50, 150))

            Enemy(e)
        show_score()
        Player(playerX, playerY)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
