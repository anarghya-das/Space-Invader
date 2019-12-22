import pygame
import random
import math
from enemy import EnemyClass


def show_score(score):
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    scoreX, scoreY = 10, 10
    s, rect = text_objects(f"Score : {str(score)}", font, WHITE)
    screen.blit(s, (scoreX, scoreY))


def show_over(score):
    over = pygame.font.Font('freesansbold.ttf', 82)
    mediumText = pygame.font.Font('freesansbold.ttf', 42)
    s, end = text_objects("Game Over!", over, WHITE)
    end.center = (math.floor(SCREEN_WIDTH/2),
                  math.floor(SCREEN_HEIGHT/2))
    score, srect = text_objects(f"Final Score: {score}", mediumText, WHITE)
    srect.center = (math.floor(SCREEN_WIDTH/2),
                    math.floor(SCREEN_HEIGHT/2)+70)
    enter, rect = text_objects(
        "Press Enter to Restart", mediumText, WHITE)
    rect.center = (math.floor(SCREEN_WIDTH/2),
                   math.floor(SCREEN_HEIGHT/2)+120)
    screen.blit(s, end)
    screen.blit(score, srect)
    screen.blit(enter, rect)


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


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, gameDisplay, x, y, w, h, ic, ac, textColor, action=None, *params):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if len(params) == 0:
                action()
            else:
                action(*params)
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText, textColor)
    textRect.center = (math.floor(x+(w/2)), math.floor(y+(h/2)))
    gameDisplay.blit(textSurf, textRect)


def end_game():
    pygame.quit()
    quit()

# The game function in which the game actually runs, the parameters are passed to alter the difficulty of the game
def game(playerX_change_value, enemyX_change_value, enemyY_change, enemy_count, bullet_speed, difficulty_step):
    pygame.mixer.music.play(-1)

    playerImg = pygame.image.load("assests/player.png")
    playerX = 370
    playerY = 500
    playerX_change = 0

    enemies = []
    enemyImg = pygame.image.load("assests/enemy.png")

    for _ in range(enemy_count):
        enemies.append(create_enemy(enemyX_change_value, enemyY_change))

    bullet = pygame.image.load("assests/bullet.png")
    bulletX = 0
    bulletY = 0

    pressed_left = False
    pressed_right = False
    running = True
    pause = False
    bullet_fired = False
    game_over = False
    score = 0

    while running:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        if game_over:
            pygame.mixer.music.stop()
            show_over(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    end_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        pygame.mixer.music.play(-1)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    end_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pressed_left = True
                    if event.key == pygame.K_RIGHT:
                        pressed_right = True
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                    if event.key == pygame.K_RETURN:
                        pause = False
                    if event.key == pygame.K_SPACE:
                        if not bullet_fired and not pause:
                            bulletX, bulletY = fire_bullet(
                                playerX, playerY, bullet)
                            bullet_fired = True
                            laser.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pressed_left = False
                    if event.key == pygame.K_RIGHT:
                        pressed_right = False

            if pause:
                largeText = pygame.font.Font('freesansbold.ttf', 82)
                mediumText = pygame.font.Font('freesansbold.ttf', 42)
                TextSurf, TextRect = text_objects(
                    "Game Paused", largeText, WHITE)
                TextRect.center = (math.floor(SCREEN_WIDTH/2),
                                   math.floor(SCREEN_HEIGHT/2))
                enter, rect = text_objects(
                    "Press Enter to Continue", mediumText, WHITE)
                rect.center = (math.floor(SCREEN_WIDTH/2),
                               math.floor(SCREEN_HEIGHT/2)+70)
                screen.blit(TextSurf, TextRect)
                screen.blit(enter, rect)
            else:
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
                            if score > 0:
                                score -= 1
                        else:
                            bulletY -= bullet_speed
                            update_bullet(bulletX, bulletY, bullet)

                    if collision(bulletX, bulletY, e.x, e.y):
                        bullet_fired = False
                        destroy.play()
                        bulletX = 0
                        bulletY = 0
                        score += 1
                        e.set_x(random.randint(0, 800-IMAGE_SIZE))
                        e.set_y(random.randint(50, 150))

                    Enemy(e, enemyImg)
                show_score(score)
                if score > 0 and score % difficulty_step == 0:
                    if (score // difficulty_step) + enemy_count != len(enemies):
                        enemyX_change_value += 5
                        enemyY_change += 5
                        enemies.append(create_enemy(
                            enemyX_change_value, enemyY_change))
                Player(playerX, playerY, playerImg)
        pygame.display.update()
        clock.tick(FPS)

# The main menu function which displays the title and has the buttons to start the game or exit
def main():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                intro = False
                end_game()
        screen.blit(background, (0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 82)
        TextSurf, TextRect = text_objects(
            "Space Invader", largeText, WHITE)
        TextRect.center = (math.floor(SCREEN_WIDTH/2),
                           math.floor(SCREEN_HEIGHT/2))
        screen.blit(TextSurf, TextRect)
        button("Play", screen, 150, 450, 100, 50,
               (200, 200, 200), WHITE, BLACK, game, playerX_change_value, enemyX_change_value, enemyY_change, ENEMY_COUNT, bullet_speed, difficulty_step)
        button("Quit", screen, 550, 450, 100, 50,
               (170, 1, 20), RED, WHITE, end_game)
        pygame.display.update()
        clock.tick(FPS)


# This is where the program starts, pygame is initialized, game window created and assests are loaded
if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    IMAGE_SIZE = 64
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Loading Assets
    background = pygame.image.load("assests/back.jpg")
    gameIcon = pygame.image.load("assests/player.png")
    destroy = pygame.mixer.Sound("assests/destroy.wav")
    laser = pygame.mixer.Sound("assests/laser.wav")
    music = pygame.mixer.music.load("assests/music.wav")

    # Creating the window with the resolution and setting the title
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("Space Invader")

    # Difficulty Values which can be modified to increase or decrease the game difficulty
    difficulty_step = 10  # After every 10 points scored the difficulty increases
    bullet_speed = 5
    playerX_change_value = 5
    enemyX_change_value = 5
    enemyY_change = 30
    ENEMY_COUNT = 6

    main()
