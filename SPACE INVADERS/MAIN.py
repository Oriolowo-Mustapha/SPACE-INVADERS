import pygame
import random
import math
from pygame import mixer

#   INITIALIZE PYGAME FOR USE
pygame.init()

# CREATING THE SCREEN
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load("Background img.jpg")
background = pygame.transform.scale(background, (800, 600))

# BACKGROUND SONG
mixer.music.load("background.wav")
mixer.music.play(-1)

# TITLE AND ICON
pygame.display.set_caption("Space Invaders ")
icon = pygame.image.load("space invaders ucon.png")
pygame.display.set_icon(icon)

# PLAYER
player_img = pygame.image.load("Player.png")
# TO RESIZE THE PLAYER CHARACTER
player_img = pygame.transform.scale(player_img, (64, 64))
player_x = 370
player_y = 480
player_x_change = 0

# ENEMY
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy_img.append(pygame.image.load("Enemy.png"))
    enemy_x.append(random.randint(0, 737))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.2)
    enemy_y_change.append(40)

# BULLET
bullet_img = pygame.image.load("bullet.png")
# RESIZE THE BULLET  TO 32X32
bullet_img = pygame.transform.scale(bullet_img, (64, 64))
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1.5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font .render("GAME OVER.", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def Player(x, y):
    screen.blit(player_img, (x, y))


def Enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def Fire_Bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 0, y + 0))


def is_Collision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:
    # RGB: RED- BLUE-GREEN
    screen.fill((0, 0, 0))
    # BACKGROUND
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # CHECK FOR KEY WHICH HAS BEING PRESSED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    Fire_Bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_x_change = 0

    # CHECKING FOR SPACESHIP BOUNDARIES
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # CHECKING FOR ENEMY BOUNDARIES
    for i in range(num_enemies):
        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]
            # COLLISION SYNTAX
        collision = is_Collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        Enemy(enemy_x[i], enemy_y[i], i)

    # CHECKING FOR BULLET MOVEMENT
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        Fire_Bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    Player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
