import pygame as pg
import random

TITLE = "Slime Passing"


WIDTH = 800
HEIGHT = 1000
CENTER = (WIDTH/2,HEIGHT/2)

tile_size = HEIGHT/20

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (30,30,30)

fps = 30

#Player
START_POSITIONX = WIDTH/2-25
START_POSITIONY = HEIGHT-115
player_speed = 5
sprint_mod = 1.8

#Enemy
enemy_min_speed = 5
enemy_max_speed = 10
random_enemy_speed = random.randrange(enemy_min_speed,enemy_max_speed)

startDifMod = 1

#Images
bgimg_location = "sprites/background.png"
tcimg_location = "sprites/treasure.png"
pimg_location = "sprites/player.png"
eimg_location = "sprites/enemy.png"
e2img_location = "sprites/enemy2.png"
heart_location = "sprites/lifeHeart.png"
pfimg_location = "sprites/playerForward.png"
