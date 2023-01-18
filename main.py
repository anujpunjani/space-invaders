import pygame
import random
import math
from pyfiglet import figlet_format
from termcolor import colored

header = figlet_format("Space Invaders!")
header = colored(header, color="green")
# color not showing in some computers
print(header)

# Initializing the pygame
pygame.init()

# create a screen
# (x, y) -> top left is (0, 0) -> 800 width - 600 height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("playership.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    # blit means to draw - so drawing an image of player on screen
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)


def enemy(x, y, i):
    # blit means to draw - so drawing an image of player on screen
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"
bullet_fire = False


def fire_bullet(x, y):
    global bullet_fire, bullet_state
    bullet_fire = True
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Score

score_value = 0
font = pygame.font.Font("Merriweather-Regular.ttf", 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


# Game Over Text
over_font = pygame.font.Font("Merriweather-Regular.ttf", 70)


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))


# Collision Detection
def isCollision(eX, eY, bX, bY):
    distance = math.sqrt(((eX - bX) ** 2) + ((eY - bY) ** 2))

    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # screen fill in RGB color
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))  # image start from (0, 0)

    # looping through every event happening inside that window and check if any one is QUIT
    for event in pygame.event.get():
        # QUIT equal to cross of window
        if event.type == pygame.QUIT:
            running = False

        # When a keystroke is pressed on the keyboard
        # keydown is when a keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # if keystroke is pressed check whether its left or right
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready" or bullet_fire is False:
                    # Get the current x, y coordinate of the spaceship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        # Keyup is when a keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Checking for boundaries so that player doesn't go out of bounds
    # X coordinate
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    # Y coordinate
    if playerY >= 536:
        playerY = 536
    elif playerY <= 0:
        playerY = 0

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        # Movement
        enemyX[i] += enemyX_change[i]

        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # bulletX = playerX
            bulletY = playerY
            bullet_fire = False
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        # bulletY = playerY
        bullet_fire = False
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # this is going to be there for updating whatever changes happened to screen
    # display is always updating
    pygame.display.update()
