import pygame
import random
import math
from pygame import mixer

pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Wars\BY:- ANKUR")

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.SysFont('freesansbold', 20)

# Game over
game_over_font = pygame.font.SysFont('freesansbold', 64)

# Show score
def show_score(x, y):
    score = font.render("Points: " + str(score_val),
                        True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game over text
def game_over():
    game_over_text = game_over_font.render("GAME OVER",
                                           True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))

# Background sound
mixer.music.load('C:/Users/ankur/Desktop/project/data/background.wav')
mixer.music.play(-1)

# Battle ship
playerImage = pygame.image.load('C:/Users/ankur/Desktop/project/data/spaceship.png')
playerImage = pygame.transform.scale(playerImage, (64, 64))
player_X = 370
player_Y = 523
player_Xchange = 0

# Invaders
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8
for num in range(no_of_invaders):
    invader_image = pygame.image.load('C:/Users/ankur/Desktop/project/data/alien.png')
    invader_image = pygame.transform.scale(invader_image, (64, 64))
    invaderImage.append(invader_image)
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2 * 0.5)  # Reduce the speed by 50%
    invader_Ychange.append(50)

# Bullet
bulletImage = pygame.image.load('C:/Users/ankur/Desktop/project/data/bullet.png')
bulletSize = (24, 24)  # Set the desired bullet size
bulletImage = pygame.transform.scale(bulletImage, bulletSize)
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"

# Collision
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False

# Player
def player(x, y):
    screen.blit(playerImage, (x, y))

# Invader
def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))

# Bullet
def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -1.7
            if event.key == pygame.K_RIGHT:
                player_Xchange = 1.7
            if event.key == pygame.K_SPACE:
                if bullet_state == "rest":
                    bullet_X = player_X + 16
                    bullet_Y = player_Y - 32
                    bullet_state = "fire"
                    bullet_sound = mixer.Sound('C:/Users/ankur/Desktop/project/data/bullet.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    player_X += player_Xchange

    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

        if bullet_Y <= 0:
            bullet_Y = 500
            bullet_state = "rest"

        if bullet_state == "fire":
            bullet(bullet_X, bullet_Y)
            bullet_Y -= bullet_Ychange

        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('C:/Users/ankur/Desktop/project/data/explosion.wav')
                    explosion_sound.play()
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        collision = isCollision(invader_X[i], bullet_X, invader_Y[i], bullet_Y)
        if collision:
            score_val += 1
            bullet_Y = 500
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    if player_X <= 0:
        player_X = 0
    elif player_X >= screen_width - 64:
        player_X = screen_width - 64

    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()

# Quit pygame
pygame.quit()

