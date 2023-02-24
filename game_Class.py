import pygame.sprite
from game_Objects import *
from settings import *
import sys
import random
import math
from xbox_controller import *

def draw_Text(screen,text,size,x,y,color):
    font_name = pg.font.match_font("comic_sans")
    font = pg.font.Font(font_name,size)
    text_sprite = font.render(text,True,color)
    text_rect = text_sprite.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_sprite,text_rect)


class Game():

    def __init__(self):
        self.playing = True
        self.game_window = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        joystick_count = pg.joystick.get_count()

        #setup controller
        if joystick_count > 0:
            self.xbox_controller = Controller()
        else:
            self.xbox_controller = None
        self.controller = Controller()

        #background making
        self.background = GameObject(0,0,WIDTH,HEIGHT,bgimg_location)
        #goal making
        self.treasure_chest  = GameObject(WIDTH/2-tile_size/2,tile_size/3.33,tile_size,tile_size,tcimg_location)
        #player making
        self.player = Player(START_POSITIONX, START_POSITIONY,tile_size,tile_size,pimg_location,player_speed)
        self.hasOneUp = False
        self.extraLife = GameObject(-100, -100, tile_size, tile_size, heart_location)

        self.level = 1
        #enemy starting
        self.enemies_list = []
        self.spawn_enemies(self.level)
        self.restartLevel()




    def spawn_enemies(self,number):
        startx = 100
        starty = 100
        timesSpawned = 0
        for i in range(number):
            speed = random.randint(5, 10)
            enemy_x = random.randint(115, WIDTH - tile_size)
            if startx <= WIDTH - tile_size:
                startx += 115
            else:
                startx = 100 + timesSpawned
                timesSpawned += 1
            enemy_y = startx

            flip = random.choice(("h","t"))
            if flip == "t":
                enemy = Up_Enemy(enemy_y, enemy_x, tile_size, tile_size, e2img_location, speed)
                self.enemies_list.append(enemy)

            else:
                enemy = Side_Enemy(enemy_x, enemy_y, tile_size, tile_size, eimg_location, speed)
                self.enemies_list.append(enemy)

    def check_collision(self, obj1, obj2):
        # check if colliding in the x dir
        if obj1.x > (obj2.x + obj2.width):
            return False
        elif (obj1.x + obj1.width) < obj2.x:
            return False

        if obj1.y > (obj2.y + obj2.height):
            return False
        elif (obj1.y + obj1.width) < obj2.y:
            return False
        return True

    def start_game_loop(self):
        while self.playing:

            # tick Clock
            self.clock.tick(fps)

            # get inputs
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.playing = False
            self.get_player_inputs(events)

            # if (pg.K_w or pg.K_UP or pg.K_DOWN or pg.K_s) not in keys:
            #     self.player.set_move_dir(0, "y")
            # if (pg.K_a or pg.K_LEFT or pg.K_d or pg.K_RIGH) not in keys:
            #     self.player.set_move_dir(0, "x")

                # elif event.type == pg.KEYDOWN:
                #     if event.key == pg.K_w or event.key == pg.K_UP: #move up
                #         self.player.set_move_dir(-1,"y")
                #     if event.key == pg.K_s or event.key == pg.K_DOWN: #move down
                #         self.player.set_move_dir(1,"y")
                #     if event.key == pg.K_a or event.key == pg.K_LEFT: #move left
                #         self.player.set_move_dir(-1,"x")
                #     if event.key == pg.K_d or event.key == pg.K_RIGHT: #move right
                #         self.player.set_move_dir(1,"x")
                # if event.type == pg.KEYUP:
                #     if event.key == pg.K_w or pg.K_UP or pg.K_DOWN or pg.K_s:
                #         self.player.set_move_dir(0,"y")
                #     if event.key == pg.K_a or pg.K_LEFT or pg.K_d or pg.K_RIGHT:
                #         self.player.set_move_dir(0,"x")

            self.update()
            self.draw()


    # def load_imgs(self):
        # self.background_img = pg.image.load(bgimg_location)
        # self.background_img = pg.transform.scale(self.background_img,(WIDTH,HEIGHT))
        #
        # self.treasure_chest_img = pg.image.load(tcimg_location)
        # self.treasure_chest_img = pg.transform.scale(self.treasure_chest_img,(50,50))
        #
        # self.player_img = pg.image.load(pimg_location)
        # self.player_img = pg.transform.scale(self.player_img,(50,50))

    def update(self):
        self.player.move()
        for enemy in self.enemies_list:
            enemy.path((WIDTH/8)*7,WIDTH/8,(HEIGHT/8)*6.93,(HEIGHT/6.6)) #MAX, min, max, min

        if self.check_collision(self.treasure_chest,self.player):
            print("Player Has the Chest")
            self.treasure_chest.collect()
            # self.increase_difficulty()
            # self.spawn_enemies(self.difMod)

        if self.check_collision(self.extraLife,self.player):
            self.extraLife.collect()
            self.player.lives += 1

        for enemy in self.enemies_list:
            if self.check_collision(enemy,self.player):
                if self.invincible == False:
                    if self.player.lives > 0:
                        self.player.lives -= 1
                        self.death_screen()
                        self.restartLevel()
                    else:
                        self.playing = False



        if self.treasure_chest.collected and self.player.y >HEIGHT-75:
            print("You Win")
            self.nextLevel()


    def draw(self):
        self.game_window.fill(GRAY)
        self.game_window.blit(self.background.image,(self.background.x,self.background.y))
        self.game_window.blit(self.treasure_chest.image,(self.treasure_chest.x,self.treasure_chest.y))
        self.game_window.blit(self.player.image, (self.player.x,self.player.y))
        self.game_window.blit(self.extraLife.image,(self.extraLife.x,self.extraLife.y))
        for enemy in self.enemies_list:
            self.game_window.blit(enemy.image, (enemy.x,enemy.y))
            enemy.showHitbox(self.game_window)
        self.player.showHitbox(self.game_window)
        self.treasure_chest.showHitbox((self.game_window))

        pg.display.update()

    def get_player_inputs(self,events):
        if self.xbox_controller:
            hat = self.xbox_controller.get_hat()
            self.player.set_move_dir(hat.get("H_X"),hat.get("H_Y"))
            axis = self.xbox_controller.get_axis()
            self.player.set_move_dir(axis.get("A_LX"),axis.get("A_LY"))
            button = self.xbox_controller.get_buttons()
            if button.get("B_S") == 0:
                self.player.walk()
            elif button.get("B_S") == 1:
                self.player.sprint()
            if button.get("B_W") == 0 or button.get("B_S")== 0 or button.get("B_O") == 0:
                self.invincible = False
            elif button.get("B_W") == 1 and button.get("B_S")== 1 and button.get("B_O") == 1:
                self.invincible = True
                self.player.speed = 25


        for event in events:
            if event.type == pg.KEYUP:  # looks for unpressing a key and stops movement
                if event.key == pg.K_w or pg.K_UP or pg.K_DOWN or pg.K_s:
                    self.player.set_move_dir(0, 0)
                if event.key == pg.K_a or pg.K_LEFT or pg.K_d or pg.K_RIGHT:
                    self.player.set_move_dir(0, 0)
                if event.key == pg.K_LSHIFT or pg.K_RSHIFT:
                    self.player.sprint()







        keys = pygame.key.get_pressed()  # checks if a key is pressed
        if keys[pg.K_w or pg.K_UP]:  # if key is being pressed, move up
            self.player.set_move_dir(-0,-1)
            self.player.image_path = pimg_location
        if keys[pg.K_s or pg.K_DOWN]:  # if key is being pressed, move down
            self.player.set_move_dir(0,1)
            self.player.image_path = pfimg_location
        if keys[pg.K_a or pg.K_LEFT]:  # if key is being pressed, move left
            self.player.set_move_dir(-1,0)
        if keys[pg.K_d or pg.K_RIGHT]:  # if key is being pressed, move right
            self.player.set_move_dir(1, 0)
        if keys[pg.K_LSHIFT or pg.K_RSHIFT]:
            self.player.walk()

    def show_start_screen(self):
        self.game_window.fill(GRAY)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        enemy = Side_Enemy(WIDTH/2-tile_size/2, HEIGHT/2, tile_size, tile_size, eimg_location,0)
        self.player = Player(START_POSITIONX, START_POSITIONY,tile_size,tile_size,pimg_location,player_speed)
        draw_Text(self.game_window,"Welcome To Slime Passing",55,WIDTH/2,HEIGHT/2-250,WHITE)
        draw_Text(self.game_window,"press Enter or B to start",40,WIDTH/2,HEIGHT/2+200,WHITE)
        self.game_window.blit(self.player.image, (self.player.x,self.player.y))
        self.game_window.blit(enemy.image, (enemy.x,enemy.y))
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False
            button_inputs = self.xbox_controller.get_buttons()
            b = button_inputs.get("B_E")
            if b > 0:
                waiting = False

    def show_game_over_screen(self):
        self.game_window.fill(BLACK)
        draw_Text(self.game_window,"Game Over",80,WIDTH/2,HEIGHT/2-200,RED)
        draw_Text(self.game_window,"Press enter or B to replay",30,WIDTH/2,HEIGHT/2+200,RED)
        draw_Text(self.game_window,"Press escape or start to quit",30,WIDTH/2,HEIGHT/2+250,RED)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False
                    if event.key == pg.K_ESCAPE:
                        return "end"
            button_inputs = self.xbox_controller.get_buttons()
            b = button_inputs.get("B_E")
            start = button_inputs.get("B_ST")
            if b >0:
                waiting = False
            if start >0:
                return "end"

    def death_screen(self):
        self.game_window.fill(BLACK)
        draw_Text(self.game_window, "You Died", 60, WIDTH / 2, HEIGHT / 2 - 250, WHITE)
        if self.player.lives == 1:
            draw_Text(self.game_window, ("You Have "+str(self.player.lives+1)+" Life Left"),40, WIDTH/2,HEIGHT/2,WHITE)
        else:
            draw_Text(self.game_window, ("You Have "+str(self.player.lives+1)+" Lives Left"),40, WIDTH/2,HEIGHT/2,WHITE)
        draw_Text(self.game_window, "press Enter or B to start", 40, WIDTH / 2, HEIGHT / 2 + 200, WHITE)

        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False
            button_inputs = self.xbox_controller.get_buttons()
            b = button_inputs.get("B_E")
            if b > 0:
                waiting = False

    def nextLevel(self):
        self.level +=1
        self.player.collected = False
        self.restartLevel()
        self.enemies_list = []
        self.spawn_enemies(self.level)
        self.hasOneUp = random.choice([True,True,False,False,False,False])
        if self.hasOneUp:
            self.extraLife = GameObject(random.randint(0+tile_size,WIDTH-tile_size),random.randint(0+tile_size,HEIGHT-tile_size),tile_size,tile_size,heart_location)
        else:
            self.extraLife_x = 1000
            self.extraLife_y = 0

    def restartLevel(self):
        self.enemies_list = []
        self.spawn_enemies(self.level)
        self.treasure_chest = GameObject(WIDTH / 2 - tile_size / 2, tile_size / 3.33, tile_size, tile_size,tcimg_location)
        self.player.reset()







