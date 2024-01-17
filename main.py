from typing import Any
import pygame, sys ,random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
ENEMY_COUNT = 10
PLAYER_SPEED = 4
ENEMY_SPEED = 2
BULLET_SPEED = 6
SHOOT_COOLDOWN = 500  # in milliseconds

# Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('game_resources/spaceship.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')

# Loading resources
background_image = pygame.image.load('game_resources/background.jpg')
mixer.music.load('game_resources/background.wav')
mixer.music.play(-1)
bullet_sound = mixer.Sound('game_resources/laser.wav')
explosion_sound = mixer.Sound('game_resources/explosion.wav')
over = pygame.font.Font("freesansbold.ttf", 55)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('game_resources/player_ship.png')
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.change_x = 0
        self.last_shoot_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > SHOOT_COOLDOWN:
            bullet_sound.play()
            bullet = Bullet(self.rect)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shoot_time = current_time

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('game_resources/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(30, SCREEN_HEIGHT - 200)
        self.change_x = ENEMY_SPEED
        self.change_y = 40

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.change_x = -self.change_x
            self.rect.y += self.change_y

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.image.load('game_resources/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + player_rect.width // 2 - self.rect.width // 2
        self.rect.y = player_rect.y
        self.change_y = -BULLET_SPEED

    def update(self):
        self.rect.y += self.change_y
        if self.rect.y < 0:
            self.kill()

# Game Over function
def game_over():
    over_text = over.render('GAME OVER!', True, (255, 255, 255))
    screen.blit(over_text, (SCREEN_WIDTH/2 - 190, SCREEN_HEIGHT/2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Create sprite groups
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player and add to sprite groups
player = Player()
all_sprites.add(player)
player_group.add(player)

# Create enemies and add to sprite groups
for _ in range(ENEMY_COUNT):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Scoring
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 20)
textX = 10
textY = 10

# Level
level = 1

# fullscreen flag:
fullscreen = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    player.rect.x = SCREEN_WIDTH // 2 + 90 - player.rect.width // 2 + 90
                    player.rect.y = SCREEN_HEIGHT - player.rect.height + 130
                else:
                    player.rect.x = SCREEN_WIDTH // 2 - player.rect.width // 2
                    player.rect.y = SCREEN_HEIGHT - player.rect.height - 10
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            if event.key == pygame.K_RIGHT:
                player.change_x += PLAYER_SPEED

            if event.key == pygame.K_LEFT:
                player.change_x -= PLAYER_SPEED

            if event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change_x = 0

    # Update sprites
    all_sprites.update()

    # Collision detections
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        explosion_sound.play()
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score_value += 1

    hits = pygame.sprite.groupcollide(player_group, enemies, False, False)
    if hits:
        game_over()

    # Draw everything on the screen
    screen.fill((2, 17, 34, 1))
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Draw score
    score = font.render(f"Score: {score_value} Level: {level}", True, (255, 255, 255))
    screen.blit(score, (textX, textY))

    # Level progression
    if score_value >= level * 10:
        level += 1
        ENEMY_COUNT += 5  # Increase the number of enemies with each level 
        for _ in range(5): # new-update: enemies now increase by 5 instead of 2
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Update the display
    pygame.display.flip()
    clock.tick(120) # updates the frames to 120 from 60