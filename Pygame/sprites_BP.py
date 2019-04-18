import pygame as pg
from settings import *
import time
import random

global p_spread_pos, p_spread_bool, c_spread_pos, c_spread_bool
p_spread_pos = []
p_spread_bool = False
c_spread_pos = []
c_spread_bool = False

# 추가
char_image_up = ['image/BP1_UP.png', 'image/BP2_UP.png']
char_image_down = ['image/BP1_Down.png', 'image/BP2_Down.png']
char_image_right = ['image/BP1_Right.png', 'image/BP2_Right.png']
char_image_left = ['image/BP1_Left.png', 'image/BP2_Left.png']
weapon_name = ["SHOTGUN", "BIG", "RIFLE"]
bubble = ['image/bubblebubble1.png', 'image/bubblebubble2.png']


class Player_Create(pg.sprite.Sprite):
    """Super Class"""
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0
        self.image = ""
    def get_keys(self): pass

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def draw_health(self): pass

    def update(self): pass

    def attack(self): pass


class Player(Player_Create):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.health_bar = None

        if self.game.p1_bubble_status == 'bubble':
            self.image = pg.image.load(bubble[0])
        else:
            if self.game.name == 'bazzi':
                self.image = pg.image.load(char_image_down[0])
            elif self.game.name == 'dao':
                self.image = pg.image.load(char_image_down[1])

        self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.dir = 0
        # player 1,2 받아옴
        print(self.game.name, self.game.name_2)

        # Player 설정 init
        self.health = PLAYER_HEALTH
        self.weapon = None
        self.speed = PLAYER_SPEED
        self.shot_delay = 0             # 총 발사 간격
        self.last_shot = 0              # 마지막 총알 발사 시간

        # Player1 무기 Setting
        if self.game.name == 'bazzi':
            self.weapon = weapon_name[0]
        elif self.game.name == 'dao':
            self.weapon = weapon_name[1]

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            if self.game.p1_bubble_status == 'bubble':
                pass
            else:
                self.attack()
        if keys[pg.K_a]:
            if self.game.p1_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[0])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = -BUBBLE_SPEED
                self.dir = 3
            else:
                if self.game.name == 'bazzi':
                    self.image = pg.image.load(char_image_left[0])
                elif self.game.name == 'dao':
                    self.image = pg.image.load(char_image_left[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = -PLAYER_SPEED
                self.dir = 3
        if keys[pg.K_d]:
            if self.game.p1_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[0])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = BUBBLE_SPEED
                self.dir = 1
            else:
                if self.game.name == 'bazzi':
                    self.image = pg.image.load(char_image_right[0])
                elif self.game.name == 'dao':
                    self.image = pg.image.load(char_image_right[1])
            self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
            self.vx = PLAYER_SPEED
            self.dir = 1
        if keys[pg.K_w]:
            if self.game.p1_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[0])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = -BUBBLE_SPEED
                self.dir = 0
            else:
                if self.game.name == 'bazzi':
                    self.image = pg.image.load(char_image_up[0])
                elif self.game.name == 'dao':
                    self.image = pg.image.load(char_image_up[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = -PLAYER_SPEED
                self.dir = 0
        if keys[pg.K_s]:
            if self.game.p1_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[0])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = BUBBLE_SPEED
                self.dir = 2
            else:
                if self.game.name == 'bazzi':
                    self.image = pg.image.load(char_image_down[0])
                elif self.game.name == 'dao':
                    self.image = pg.image.load(char_image_down[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = PLAYER_SPEED
                self.dir = 2
        # 대각선
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7
            self.vy *= 0.7

        if keys[pg.K_r]:    # 총 교체
            pg.mixer.Channel(1).play(pg.mixer.Sound("sound/button-09.wav"))
            if self.weapon == weapon_name[0]:       # SHOTGUN
                self.weapon = weapon_name[1]        # to BIG
                self.shot_delay = 2.5
                self.speed = 110
            elif self.weapon == weapon_name[1]:     # BIG
                self.weapon = weapon_name[2]        # to RIFLE
                self.shot_delay = 0.2
                self.speed = 130
            else:                                   # RIFLE
                self.weapon = weapon_name[0]        # to SHOTGUN
                self.shot_delay = 1
                self.speed = 150

    def draw_health(self):
        if self.health < 40:
            self.health -= 0.1
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PLAYER_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 3)
        if self.health <= PLAYER_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.health <= 0:
            self.game.p1_killed = True  # Player1의 사망을 Game 클래스에 알림

    def attack(self):
        if self.weapon == weapon_name[2]:   # RIFLE
            if time.time() - self.last_shot > self.shot_delay:
                player_bullet = Bullet_Rifle()
                player_bullet.rect.x = self.rect.x
                player_bullet.rect.y = self.rect.y
                player_bullet.dir = self.game.player.dir
                self.game.all_sprites.add(player_bullet)
                self.game.player_bullets.add(player_bullet)
                pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Rifle.wav"))
                self.last_shot = time.time()

        elif self.weapon == weapon_name[0]:     # SHOTGUN
            if time.time() - self.last_shot > self.shot_delay:
                bullet_list = []
                global c_spread_bool, c_spread_pos
                spread_num1 = -0.1
                if not c_spread_bool:
                    for i in range(10):
                        player_bullet = Bullet_Shotgun()
                        bullet_list.append(player_bullet)
                    for b in bullet_list:
                        spread_num2 = random.randint(-10, 10)
                        b.rect.x = self.rect.x + spread_num2
                        b.rect.y = self.rect.y + spread_num2
                        c_spread_pos.append(spread_num2)
                        b.dir = self.dir
                        b.bullet_spread = spread_num1
                        self.game.all_sprites.add(b)
                        self.game.player_bullets.add(b)
                        self.shot_delay = b.delay
                        spread_num1 += 0.2
                    pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Shotgun.wav"))
                else:
                    for i in range(10):
                        player_bullet = Bullet_Shotgun()
                        bullet_list.append(player_bullet)
                    i = 0
                    for b in bullet_list:
                        b.rect.x = self.rect.x + c_spread_pos[i]
                        b.rect.y = self.rect.y + c_spread_pos[i]
                        b.dir = self.dir
                        b.bullet_spread = spread_num1
                        self.game.all_sprites.add(b)
                        self.game.player_bullets.add(b)
                        spread_num1 += 0.2
                        i += 1
                        self.shot_delay = b.delay
                    pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Shotgun.wav"))
                self.last_shot = time.time()
                c_spread_bool = True

        elif self.weapon == weapon_name[1]:     # BIG
            if time.time() - self.last_shot > self.shot_delay:
                player_bullet = Bullet_Big()
                player_bullet.rect.x = self.rect.x
                player_bullet.rect.y = self.rect.y
                player_bullet.dir = self.game.player.dir
                self.shot_delay = player_bullet.delay
                self.game.all_sprites.add(player_bullet)
                self.game.player_bullets.add(player_bullet)
                pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Bazooka.wav"))
                self.last_shot = time.time()

    def touch_challenger(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.challenger, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.challenger, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


class Challenger(Player_Create):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.challengers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.health_bar = None
        if self.game.p2_bubble_status == 'bubble':
            self.image = pg.image.load(bubble[1])
        else:
            if self.game.name_2 == 'bazzi':
                self.image = pg.image.load(char_image_down[0])
            elif self.game.name_2 == 'dao':
                self.image = pg.image.load(char_image_down[1])

        self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.dir = 0
        # Challenger 설정 init
        self.health = CHALLENGER_HEALTH
        self.weapon = None
        self.speed = PLAYER_SPEED
        self.shot_delay = 0
        self.last_shot = 0

        # Player2 무기 Setting
        if self.game.name_2 == 'bazzi':
            self.weapon = weapon_name[0]    # SHOTGUN
        elif self.game.name_2 == 'dao':
            self.weapon = weapon_name[1]    # BIG

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_SLASH]:
            if self.game.p2_bubble_status == 'bubble':
                pass
            else:
                self.attack()
        if keys[pg.K_LEFT]:
            if self.game.p2_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = -BUBBLE_SPEED
                self.dir = 3
            else:
                if self.game.name_2 == 'bazzi':
                    self.image = pg.image.load(char_image_left[0])
                elif self.game.name_2 == 'dao':
                    self.image = pg.image.load(char_image_left[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = -PLAYER_SPEED
                self.dir = 3
        if keys[pg.K_RIGHT]:
            if self.game.p2_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = BUBBLE_SPEED
                self.dir = 1
            else:
                if self.game.name_2 == 'bazzi':
                    self.image = pg.image.load(char_image_right[0])
                elif self.game.name_2 == 'dao':
                    self.image = pg.image.load(char_image_right[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vx = PLAYER_SPEED
                self.dir = 1
        if keys[pg.K_UP]:
            if self.game.p2_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = -BUBBLE_SPEED
                self.dir = 0
            else:
                if self.game.name_2 == 'bazzi':
                    self.image = pg.image.load(char_image_up[0])
                elif self.game.name_2 == 'dao':
                    self.image = pg.image.load(char_image_up[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = -PLAYER_SPEED
                self.dir = 0
        if keys[pg.K_DOWN]:
            if self.game.p2_bubble_status == 'bubble':
                self.image = pg.image.load(bubble[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = BUBBLE_SPEED
                self.dir = 2
            else:
                if self.game.name_2 == 'bazzi':
                    self.image = pg.image.load(char_image_down[0])
                elif self.game.name_2 == 'dao':
                    self.image = pg.image.load(char_image_down[1])
                self.image = pg.transform.scale(self.image, (TILESIZE * 2, TILESIZE * 2))
                self.vy = PLAYER_SPEED
                self.dir = 2
        if keys[pg.K_COMMA]:
            pg.mixer.Channel(1).play(pg.mixer.Sound("sound/button-09.wav"))
            if self.weapon == weapon_name[0]:       # SHOTGUN
                self.weapon = weapon_name[1]        # to BIG
                self.shot_delay = 2.5
                self.speed = 110
            elif self.weapon == weapon_name[1]:     # BIG
                self.weapon = weapon_name[2]        # to RIFLE
                self.shot_delay = 0.2
                self.speed = 130
            else:                                   # RIFLE
                self.weapon = weapon_name[0]        # to SHOTGUN
                self.shot_delay = 1
                self.speed = 150

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7
            self.vy *= 0.7

    def draw_health(self):
        if self.health < 40:
            self.health -= 0.1
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / CHALLENGER_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 3)
        if self.health <= CHALLENGER_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.health <= 0:
            self.game.p2_killed = True  # Player2의 사망을 Game 클래스에 알림

    def attack(self):
        if self.weapon == weapon_name[2]:   # RIFLE
            if time.time() - self.last_shot > self.shot_delay:
                challenger_bullet = Bullet_Rifle()
                challenger_bullet.rect.x = self.rect.x
                challenger_bullet.rect.y = self.rect.y
                challenger_bullet.dir = self.game.challenger.dir
                self.game.all_sprites.add(challenger_bullet)
                self.game.challenger_bullets.add(challenger_bullet)
                pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Rifle.wav"))
                self.last_shot = time.time()

        elif self.weapon == weapon_name[0]:     # SHOTGUN
            if time.time() - self.last_shot > self.shot_delay:
                bullet_list = []
                global c_spread_bool, c_spread_pos
                spread_num1 = -0.1
                if not c_spread_bool:
                    for i in range(10):
                        challenger_bullet = Bullet_Shotgun()
                        bullet_list.append(challenger_bullet)
                    for b in bullet_list:
                        spread_num2 = random.randint(-20, 20)
                        b.rect.x = self.rect.x + spread_num2
                        b.rect.y = self.rect.y + spread_num2
                        c_spread_pos.append(spread_num2)
                        b.dir = self.dir
                        b.bullet_spread = spread_num1
                        self.game.all_sprites.add(b)
                        self.game.challenger_bullets.add(b)
                        self.shot_delay = b.delay
                        spread_num1 += 0.2
                    pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Shotgun.wav"))
                else:
                    for i in range(10):
                        challenger_bullet = Bullet_Shotgun()
                        bullet_list.append(challenger_bullet)
                    i = 0
                    for b in bullet_list:
                        b.rect.x = self.rect.x + c_spread_pos[i]
                        b.rect.y = self.rect.y + c_spread_pos[i]
                        b.dir = self.dir
                        b.bullet_spread = spread_num1
                        self.game.all_sprites.add(b)
                        self.game.challenger_bullets.add(b)
                        spread_num1 += 0.2
                        i += 1
                        self.shot_delay = b.delay
                    pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Shotgun.wav"))
                self.last_shot = time.time()
                c_spread_bool = True

        elif self.weapon == weapon_name[1]:
            if time.time() - self.last_shot > self.shot_delay:
                challenger_bullet = Bullet_Big()
                challenger_bullet.rect.x = self.rect.x
                challenger_bullet.rect.y = self.rect.y
                challenger_bullet.dir = self.game.challenger.dir
                self.shot_delay = challenger_bullet.delay
                self.game.all_sprites.add(challenger_bullet)
                self.game.challenger_bullets.add(challenger_bullet)
                pg.mixer.Channel(1).play(pg.mixer.Sound("sound/Bazooka.wav"))
                self.last_shot = time.time()

    def touch_player(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.player, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.player, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        image_path = "image/" + image + ".png"
        self.image = pg.image.load(image_path)
        # size transform
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        image_path = "image/" + image + ".png"
        self.image = pg.image.load(image_path)
        # size transform
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Bullet(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.dir = 0
        self.bullet_speed = 0
        self.delay = 0
        self.damage = 0

    def update(self): pass


class Bullet_Shotgun(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = pg.image.load('image/WaterBall.png')
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.dir = 0
        self.bullet_speed = 17
        self.bullet_spread = 0
        self.delay = 1
        self.damage = 7.5

    def update(self):
        if self.dir == 0:
            self.rect.y -= self.bullet_speed
            self.rect.x += self.bullet_spread
        elif self.dir == 1:
            self.rect.x += self.bullet_speed
            self.rect.y += self.bullet_spread
        elif self.dir == 2:
            self.rect.y += self.bullet_speed
            self.rect.x += self.bullet_spread
        elif self.dir == 3:
            self.rect.x -= self.bullet_speed
            self.rect.y += self.bullet_spread


class Bullet_Rifle(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = pg.image.load('image/WaterBall.png')
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.dir = 0
        self.bullet_speed = 30
        self.delay = 0.2
        self.damage = 15

    def update(self):
        if self.dir == 0:
            self.rect.y -= self.bullet_speed
        elif self.dir == 1:
            self.rect.x += self.bullet_speed
        elif self.dir == 2:
            self.rect.y += self.bullet_speed
        elif self.dir == 3:
            self.rect.x -= self.bullet_speed


class Bullet_Big(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = pg.image.load('image/WaterBall.png')
        self.image = pg.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.dir = 0
        self.bullet_speed = 20
        self.delay = 2.5
        self.damage = 100

    def update(self):
        if self.dir == 0:
            self.rect.y -= self.bullet_speed
        elif self.dir == 1:
            self.rect.x += self.bullet_speed
        elif self.dir == 2:
            self.rect.y += self.bullet_speed
        elif self.dir == 3:
            self.rect.x -= self.bullet_speed

