# Main Game Loop Code.

import pygame
import math
import os
import random

pygame.font.init()
FONT = pygame.font.SysFont('agencyfb', 40)
COLOUR = (255, 255, 255)

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 40
FPS = 60
VEL = 5
START_ENEMY_VEL = 3
EXPLODE_RADIUS = 200
SUPERNOVA_WIDTH = 500
START_SPAWN_RATE = 200
NUM_LIVES = 3
HITBOX = 20
STAR_WIDTH = 80
SUPERNOVA_SPAN = 15

MY_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images', 'user_ship.png'))
MY_SPACESHIP = pygame.transform.scale(MY_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
ENEMY_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images', 'enemy_ship.png'))
ENEMY_SPACESHIP = pygame.transform.scale(ENEMY_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('images', 'space.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
STAR_IMAGE = pygame.image.load(os.path.join('images', 'star.png'))
STAR = pygame.transform.scale(STAR_IMAGE, (STAR_WIDTH, STAR_WIDTH))
SUPERNOVA_IMAGE = pygame.image.load(os.path.join('images', 'supernova.png'))
SUPERNOVA = pygame.transform.scale(SUPERNOVA_IMAGE, (SUPERNOVA_WIDTH, SUPERNOVA_WIDTH))
MENU_IMAGE = pygame.image.load(os.path.join('images', 'menu.jpg'))
MENU = pygame.transform.scale(MENU_IMAGE, (WIDTH, HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supernova Dodgeball")

class Ship:
    
    def __init__(self, x, y, speed): # Note x and y refer to the middle.
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x - (SPACESHIP_WIDTH/2), self.y - (SPACESHIP_HEIGHT/2), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    def move(self, aim_x, aim_y):
        # Input position moving toward (e.g. mouse coords for Player, player coords for Enemy)
        # Execute the change in direction.
        # Note that we actually don't need to check/enforce player doesn't go off the map.
        rel_x, rel_y = aim_x - self.x, aim_y - self.y
        mag = ((rel_x**2)+(rel_y**2))**0.5
        if mag > 5:
            self.x += math.floor((rel_x / mag) * self.speed)
            self.y += math.floor((rel_y / mag) * self.speed)
            self.angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x)) - 90

class Player(Ship):
    
    def draw(self):
        MY_ROTATED_SPACESHIP = pygame.transform.rotate(MY_SPACESHIP, self.angle)
        WIN.blit(MY_ROTATED_SPACESHIP, (self.x - (SPACESHIP_WIDTH/2), self.y - (SPACESHIP_HEIGHT/2)))

class Enemy(Ship):
    
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.is_collision = False
    
    def draw(self):
        ROTATED_ENEMY_SPACESHIP = pygame.transform.rotate(ENEMY_SPACESHIP, self.angle)
        WIN.blit(ROTATED_ENEMY_SPACESHIP, (self.x - (SPACESHIP_WIDTH/2), self.y - (SPACESHIP_HEIGHT/2)))

    def check_collision(self, other):
        # Check if there is a collison.
        dx = self.x - other.x
        dy = self.y - other.y
        if dx**2 + dy**2 < HITBOX**2:
            self.is_collision = True
            pygame.time.delay(2000)

class Star:
    
    def __init__(self):
        # Spawn a star in the middle.
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.is_collision = False
    
    def draw(self):
        # Code to draw the star.
        WIN.blit(STAR, (self.x - (STAR_WIDTH/2), self.y - (STAR_WIDTH/2)))
    
    def check_collision(self, other, supernova):
        # Check for collision with the player.
        # If so, move the star elsewhere.
        dx = self.x - other.x
        dy = self.y - other.y
        if dx**2 + dy**2 < HITBOX**2:
            # Save the (maybe) old star's coordinates in the supernova object.
            for a in [self.x]:
                supernova.x = a
            for b in [self.y]:
                supernova.y = b
            self.is_collision = True
            self.x = random.randint(100, WIDTH)
            self.y = random.randint(100, HEIGHT)


class Supernova:
    
    def __init__(self):
        self.exists = False
    
    def draw(self):
        WIN.blit(SUPERNOVA, (self.x - (SUPERNOVA_WIDTH/2), self.y - (SUPERNOVA_WIDTH/2)))

def title():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            main()
        # Drawing
        WIN.blit(MENU, (0, 0))
        central_text = FONT.render("Press the Space key to start", 1, COLOUR)
        WIN.blit(central_text, ((WIDTH-central_text.get_width())/2, HEIGHT-200))
        pygame.display.update()

def main():
    # Instantiate Player and Star classes.
    player = Player(300, 100, VEL) # Fill in data here.
    star = Star()
    supernova = Supernova()
    score = 0
    lives = NUM_LIVES
    enemies = []
    SPAWN_RATE = START_SPAWN_RATE
    spawn_counter = SPAWN_RATE
    ENEMY_VEL = START_ENEMY_VEL
    supernova_counter = SUPERNOVA_SPAN
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
        # Increase difficulty
        if score < 20 and score > 10:
            SPAWN_RATE = 150
        elif score < 30 and score > 20:
            ENEMY_VEL = 4
        elif score < 40 and score > 30:
            SPAWN_RATE = 100
        elif score < 50 and score > 40:
            ENEMY_VEL = 5
        elif score < 60 and score > 50:
            SPAWN_RATE = 50
        elif score < 70 and score > 60:
            ENEMY_VEL = 6
        elif score < 80 and score > 70:
            SPAWN_RATE = 25
        
        # Make new enemies.
        if spawn_counter > 0:
            spawn_counter -= 1
        else:
            spawn_counter = SPAWN_RATE
            rand_var = random.randint(1, 4)
            if rand_var == 1:
                # Top left spawn.
                enemies.append(Enemy(0, 0, ENEMY_VEL))
            elif rand_var == 2:
                # Top right spawn.
                enemies.append(Enemy(WIDTH, 0, ENEMY_VEL))
            elif rand_var == 3:
                # Bottom left spawn.
                enemies.append(Enemy(0, HEIGHT, ENEMY_VEL))
            else:
                # Bottom right spawn.
                enemies.append(Enemy(WIDTH, HEIGHT, ENEMY_VEL))
        
        # Do the movement.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player.move(mouse_x, mouse_y)
        for enemy in enemies:
            enemy.move(player.x, player.y)
        
        # Check for enemy ship collisions.
        for enemy in enemies:
            enemy.check_collision(player)
            if enemy.is_collision:
                lives -= 1
                enemies = []
        
        # Check for player/star collisons.
        star.check_collision(player, supernova)
        if star.is_collision:
            star.is_collision = False
            new_enemies = []
            for enemy in enemies:
                dx = supernova.x - enemy.x
                dy = supernova.y - enemy.y
                if dx**2 + dy**2 < EXPLODE_RADIUS**2:
                    score += 1
                else:
                    new_enemies.append(enemy)
            enemies = new_enemies
            supernova.exists = True
        
        # Check lives
        if lives < 1:
            # Return difficutly parameters.
            ENEMY_VEL = START_ENEMY_VEL
            SPAWN_RATE = START_SPAWN_RATE
            # Title screen.
            title()
            run = False
        
        # Do the drawing.
        WIN.blit(BACKGROUND, (0, 0))
        if supernova.exists:
            if supernova_counter > 0:
                supernova_counter -= 1
                supernova.draw()
            else:
                supernova.exists = False
                supernova_counter = SUPERNOVA_SPAN
        score_text = FONT.render("Score: " + str(score), 1, COLOUR)
        WIN.blit(score_text, (20, 20))
        lives_text = FONT.render("Lives: " + str(lives), 1, COLOUR)
        WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 20, 20))
        star.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()

        pygame.display.update()


if __name__ == "__main__":
    title()
