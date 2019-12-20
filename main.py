import pygame
import random
import math
from enemy import EnemyClass


def show_score(score):
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    scoreX, scoreY = 10, 10
    s = font.render(f"Score : {str(score)}", True, (255, 255, 255))
    screen.blit(s, (scoreX, scoreY))


def show_over():
    over = pygame.font.Font(pygame.font.get_default_font(), 64)
    overX, overY = 250, 250
    s = over.render("Game Over!", True, (255, 255, 255))
    screen.blit(s, (overX, overY))


def create_enemy(enemyX_change_value, enemyY_change):
    enemyX = random.randint(0, 800-IMAGE_SIZE)
    enemyY = random.randint(50, 150)
    enemyX_change = enemyX_change_value
    e = EnemyClass(enemyX, enemyY, enemyX_change, enemyY_change)
    return e


def Enemy(e, enemyImg):
    screen.blit(enemyImg, (e.x, e.y))


def Player(x, y, playerImg):
    screen.blit(playerImg, (x, y))


def boundary_check(x_cord):
    offset = SCREEN_WIDTH-IMAGE_SIZE
    if x_cord <= 0:
        return 0
    elif x_cord >= offset:
        return offset
    else:
        return x_cord


def enemy_update(e):
    x = e.x
    change = e.x_change
    y = e.y
    x += change
    offset = SCREEN_WIDTH-IMAGE_SIZE
    if x <= 0:
        change = enemyX_change_value
        x = 0
        y += e.y_change
    elif x >= offset:
        change = -enemyX_change_value
        x = offset
        y += e.y_change
    e.set_x(x)
    e.set_y(y)
    e.set_x_change(change)


def fire_bullet(x, y, bullet):
    bx = x
    by = y-IMAGE_SIZE
    screen.blit(bullet, (bx, by))
    return bx, by


def update_bullet(x, y, bullet):
    screen.blit(bullet, (x, y))


def collision(b_x, b_y, e_x, e_y):
    d = math.sqrt(math.pow(b_x-e_x, 2)+math.pow(b_y-e_y, 2))
    if d < 27:
        return True
    else:
        return False


def game(playerX_change_value, enemyX_change_value, enemyY_change, enemy_count, bullet_speed):
    playerImg = pygame.image.load("player.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemies = []
    enemyImg = pygame.image.load("enemy.png")

    for _ in range(enemy_count):
        enemies.append(create_enemy(enemyX_change_value, enemyY_change))

    background = pygame.image.load("back.jpg")
    bullet = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = 0

    pressed_left = False
    pressed_right = False
    running = True
    bullet_fired = False
    game_over = False
    score = 0

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
                        pressed_left = True
                    if event.key == pygame.K_RIGHT:
                        pressed_right = True
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if not bullet_fired:
                            bulletX, bulletY = fire_bullet(
                                playerX, playerY, bullet)
                            bullet_fired = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pressed_left = False
                    if event.key == pygame.K_RIGHT:
                        pressed_right = False

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
                enemy_update(e)
                if bullet_fired:
                    if bulletY <= 0:
                        bullet_fired = False
                    else:
                        bulletY -= bullet_speed
                        update_bullet(bulletX, bulletY, bullet)

                if collision(bulletX, bulletY, e.x, e.y):
                    bullet_fired = False
                    bulletX = 0
                    bulletY = 0
                    score += 1
                    e.set_x(random.randint(0, 800-IMAGE_SIZE))
                    e.set_y(random.randint(50, 150))

                Enemy(e,enemyImg)
            show_score(score)
            Player(playerX, playerY, playerImg)
        pygame.display.update()
        clock.tick(FPS)


pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMAGE_SIZE = 64

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Difficulty Values
bullet_speed = 3
playerX_change_value = 4
enemyX_change_value = 4
enemyY_change = 20
ENEMY_COUNT = 6

game(playerX_change_value,enemyX_change_value,enemyY_change,ENEMY_COUNT,bullet_speed)
pygame.quit()
quit()
