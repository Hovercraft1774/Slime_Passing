from settings import *
import pygame as pg


class GameObject():
    def __init__(self,x,y,width, height, image_path):
        image = pg.image.load(image_path)
        self.image = pg.transform.scale(image,(width,height))
        self.width = width
        self.height = height
        self.startx = x
        self.starty = y
        self.x = self.startx
        self.y = self.starty
        self.player_dirY = 0
        self.player_dirX = 0
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.collected = False
    def showHitbox(self,win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pg.draw.rect(win,(255,0,0),self.hitbox,2)

    def reset(self):
        self.x = self.startx
        self.y = self.starty
        self.collected = False


    def collect(self):
        self.image = pg.transform.scale(self.image,(0,0))
        self.width = 0
        self.height = 0
        self.x = -100
        self.y = -100
        self.collected = True


class Player(GameObject):

    def __init__(self,x,y,width,height,image_path,speed):
        super(Player, self).__init__(x,y,width,height,image_path)
        self.speed = speed
        self.lives = 2
    def move(self):
        if (self.y > 0) or (self.y < HEIGHT) or (self.x > 0) or (self.x < WIDTH):
            pass
        self.y += (self.player_dirY * self.speed)
        self.x += (self.player_dirX * self.speed)
        if self.y > HEIGHT-tile_size:
            self.y = HEIGHT-tile_size
            return
        if self.y < 0:
            self.y = 0
            return
        if self.x > WIDTH- tile_size:
            self.x = WIDTH - tile_size
            return
        if self.x < 0:
            self.x = 0
            return
    def death(self):
        self.x = -200
        self.y = -200
        self.player_dirY = 0
        self.player_dirX = 0
        self.collected = False

    def walk(self):
        self.speed = player_speed
    def sprint(self):
        self.speed = player_speed*sprint_mod

    #setter method, dont reach in container
    def set_move_dir(self,x,y):
            self.player_dirX = x
            self.player_dirY = y




class Side_Enemy(GameObject):
    def __init__(self,x,y,width,height,image_path,speed):
        super(Side_Enemy,self).__init__(x,y,width,height,image_path)
        self.speed = speed
        self.enemy_dirX = 1
    def path(self,max_width,min_width,max_height,min_height):
        self.x +=(self.enemy_dirX * self.speed)
        if self.x >= max_width - self.width:
            self.enemy_dirX = -1
        elif self.x <= min_width:
            self.enemy_dirX = 1




class Up_Enemy(GameObject):
    def __init__(self, x, y, width, height, image_path, speed):
        super(Up_Enemy, self).__init__(x, y, width, height, image_path)
        self.speed = speed
        self.enemy_dirY = 1

    def path(self,max_width,min_width, max_height, min_height):
        self.y += (self.enemy_dirY * self.speed)
        if self.y >= max_height - self.height:
            self.enemy_dirY = -1
        elif self.y <= min_height:
            self.enemy_dirY = 1
            self.enemy_dirX = 0










