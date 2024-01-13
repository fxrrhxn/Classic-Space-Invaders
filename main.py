import pygame ,random ,math
from pygame import mixer

# initialise pygame before using it:
pygame.init()

# creating a screen:
screen = pygame.display.set_mode((800, 600))

# Creating a title and icon for the window:
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#background image:
background = pygame.image.load("background.jpg")

# background sound:
mixer.music.load('background.wav')
mixer.music.play(-1)

# player spaceship:
playerImg = pygame.image.load('player_ship.png')
playerX = 370
playerY = 500
playerX_change = 0

# enemy:
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(0.26)
    enemyY_change.append(37)

# score:
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 20)
textX = 10
textY = 10

# Game Over:
over = pygame.font.Font("freesansbold.ttf", 55)

# bullet:
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletY_change = 1

# Ready - you cant see the bullet on the screen
# Fire - bullet is ready to be fires
bullet_state = "ready"

def showScore(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    # render the text:
    over_text = over.render('GAME OVER!', True,  (255, 255, 255))
    screen.blit(over_text, (221, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bulet(x, y):

    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+20, y+8))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX[i]-bulletX,2)+ math.pow(enemyY[i]-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False
    
# Main Game Loop:
running = True
while running:

    # Colors for the screen:
    screen.fill((2, 17, 34, 1))
    # background input
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking keystrokes:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.3
            if event.key == pygame.K_RIGHT:
                playerX_change += 0.3
            
            # firing bullet:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # get the current x co-ordinate of the spaceship:
                    bullet_sound =mixer.Sound('laser.wav')
                    bulletX = playerX
                    fire_bulet(bulletX, bulletY)
                    bullet_sound.play()
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0   

# Considering boundaries for player spaceship and enemy:
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # bullet movement:
    if bullet_state == "fire":
        fire_bulet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    # enemy movement:
    for i in range(num_of_enemies):

        #Game Over:
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] += 0.26
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 0.26
            enemyY[i] += enemyY_change[i]
        
        # Collision:
        collision = isCollision(enemyX, enemyY, bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()