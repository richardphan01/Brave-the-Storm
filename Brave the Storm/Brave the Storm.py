#Importing Libraries required for Game
import pygame
import random
import sys
import math
from pygame import mixer
import time

#Initializers for pygame and mixer libraries
mixer.init()
pygame.init()

#Visuals for game window
icon = pygame.image.load(".\\assets\\download.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Brave the Storm")

#Background music for the game
mixer.music.load(".\\assets\\a.mp3")
mixer.music.play(-1)

#Sets the size of the game window
length = 800
width = 600
t_end = time.time() + 10

text_color = (0,255,0)
player_color = (0,255,255)
player_rad = 15
player_pos = [400,575]
player_speed = 7
background_color = (0,0,0)
pygame.key.set_repeat(10,10)


num_enemies = 10
enemy_color = [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
enemy_rad = 50
enemy_pos = [random.randint(0,length), 0]
enemy_list = [enemy_pos]

num_powerups = 1
power_pos = [random.randint(0,length), 0]
power_list = [power_pos]
power_rad = 10
power_color = [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
speed_powerup = 10


speed = 10
screen = pygame.display.set_mode((length,width))
collision_rad = player_rad + enemy_rad
powercollision_rad = player_rad + power_rad

game_over = False
score = 0
level = 1

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("Comic Sans MS",35)

#Functions for game entity movement
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < num_enemies and delay < 0.075:
        x_pos = random.randint(0,length-enemy_rad)
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def drop_powerups(power_list, player_color):
    delay = random.random()
    if len(power_list) < num_powerups and delay < 0.001 and player_color == (0,255,255):
        x_pos = random.randint(0,length-power_rad)
        y_pos = 0
        power_list.append([x_pos,y_pos])

#Functions for main game functions
def display_level(score, level):
    if score < 50:
        level = 1
    elif score < 150:
        level = 2
    elif score < 300:
        level = 3
    elif score < 500:
        level = 4
    else:
        level = 5
    return level

def set_level(score, speed):

    speed = score/5 + 5

    return speed

def number_enemies(level,num_enemies):
    if level == 1:
        num_enemies = 10
    elif level == 2:
        num_enemies = 12
    elif level == 3:
        num_enemies = 14
    elif level == 4:
        num_enemies = 16
    else:
        num_enemies = 18

    return num_enemies


###Functions to draw in game entities###

#This function draws the enemy by taking in the: surface drawn on, color, position(x,y), and the radius and draws a circle until the maximum number of enemies are drawn
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(screen, enemy_color, enemy_pos, enemy_rad)

#This function draws the enemy by taking in the: surface drawn on, color, position(x,y), and the radius and draws a circle until the maximum number of enemies are drawn
def draw_powerups(power_list):
    for power_pos in power_list:
        power_color = [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
        pygame.draw.circle(screen, power_color, power_pos, power_rad)



###Functions to update game entity positions###

#This function checks to see if power up are on the screen.  If the power up is on screen its position is updated. Otherwise, it is removed from the list
def update_powerups(power_list):
    for idx, power_pos in enumerate(power_list):
        if power_pos[1] >= 0 and (power_pos[1]+power_rad) < length:
            power_pos[1] += int(speed/2)
        else:
            power_list.pop(idx)

#This function checks to see if enemies are on the screen.  If the enemy is on screen its position is updated. Otherwise, it is removed from the list
def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and (enemy_pos[1]+enemy_rad) < length:
            enemy_pos[1] += int(speed/2)
        else:
            enemy_list.pop(idx)
            score += 1
    return score


###Functions to evaluate collision checks between player and game entities###

#The position of all the enemies on the screen is taken. For each enemy, checks whether any enemy collided with the player.
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detectCollision(player_pos, enemy_pos):
            return True
    return False


def power_collision_check(power_list, player_pos):
    for power_pos in power_list:
        if powerup_collision(player_pos, power_pos):
            return True
    return False

#The position of the enemies and player are calculated relative to each other to check whether they have collided
def detectCollision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (math.sqrt((e_x-p_x)**2+(e_y-p_y)**2)+int(score/30) <=collision_rad):
        return True
    return False

def powerup_collision(player_pos, power_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    pu_x = power_pos[0]
    pu_y = power_pos[1]

    if (math.sqrt((pu_x-p_x)**2+(pu_y-p_y)**2) <=powercollision_rad):
        power_pos[1] = 1000
        return True
    return False

#Main Loop that runs the game
while not game_over:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_UP:
                if player_pos[1] > (player_rad):
                    y -= player_speed
            elif event.key == pygame.K_DOWN:
                if player_pos[1] < (width-player_rad):
                    y += player_speed
            elif event.key == pygame.K_RIGHT:
                if player_pos[0] < (length-player_rad):
                    x += player_speed
            elif event.key == pygame.K_LEFT:
                if player_pos[0] > (player_rad):
                    x -= player_speed

            player_pos = [x,y]

    screen.fill(background_color)

    clock.tick(30)


    drop_enemies(enemy_list)
    draw_enemies(enemy_list)


    drop_powerups(power_list, player_color)
    draw_powerups(power_list)
    update_powerups(power_list)

    num_enemies = number_enemies(level,num_enemies)

    score = update_enemy_positions(enemy_list, score)



    speed = set_level(score, speed)
    level = display_level(score, level)



    text_level = "Level: " + str(level)
    text = "Score: " + str(score)

    label = myFont.render(text, 1, text_color)
    label_level = myFont.render(text_level, 1, text_color)

    screen.blit(label, (length-200,width-40))
    screen.blit(label_level, (length-200,(width - 80)))



    if powerup_collision(player_pos, power_pos):
        print(player_pos)
        print(power_pos)
        power_num = random.randint(1, 2)
        if power_num == 1:
            if not player_color == (255,255,0):
                player_color = (255,0,0)

        if power_num == 2:
            if not player_color == (255,0,0):
                player_color = (255,255,0)
                if player_color == (255,255,0):
                    player_speed = int(speed*2)



    if player_color == (255,0,0):
         if collision_check(enemy_list, player_pos):
            game_over = False
    else:
        if collision_check(enemy_list, player_pos):
            game_over = True

    powerup_time = random.random()
    if powerup_time < 0.004:
        player_color = (0,255,255)
        player_speed = 7


    player = pygame.draw.circle(screen, player_color , (player_pos[0],player_pos[1]) , player_rad)
    pygame.display.update()
