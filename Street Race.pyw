import pygame as pg
import sys
import random
import math

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

W = 800
H = 600
BG = (100, 100, 100)
WHITE = (255, 255, 255)
car_accident = 0
drove_cars = 0
speed = 2
acceleration = 0.05
f_screen = [1, 2]
level = 40
R, G, B = 0, 255, 0
radius = 140
stop = 1
stop_tick = 0
start = True
game = True
pause = [False, True]
level_game = 1
play, out = None, None

home_images = []
path = 'img/home'
for file_name in os.listdir(path):
    home_image = pg.image.load(path + os.sep + file_name)
    home_images.append(home_image)
image_btn1 = pg.image.load('img/btn_play.png')
image_btn2 = pg.image.load('img/btn_exit.png')
player_image = pg.image.load('img/Car.png')
fuel_image = pg.image.load('img/fuel.png')
canister_image = pg.image.load('img/canister.png')
tree_image = pg.image.load('img/d.png')
flower_image = pg.image.load('img/c.png')
water_image = pg.image.load('img/water.png')
image_3 = pg.image.load('img/3.png')
CARS = [pg.image.load('img/car1.png'), pg.image.load('img/car2.png'),
        pg.image.load('img/car3.png')]
n = len(CARS)
COLOR = ['red3', 'dark green', 'navy', 'orange']
imgColor = pg.image.load('img/car4.png')
originalColor = imgColor.get_at((imgColor.get_width() // 2, imgColor.get_height() // 2))
ar = pg.PixelArray(imgColor)
ar.replace(originalColor, pg.Color(random.choice(COLOR)), 0.1)
del ar
CARS.append(imgColor)

FPS = 120
clock = pg.time.Clock()

# pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()
u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, 350)
u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, random.randrange(7000, 27001, 5000))

text1 = pg.font.SysFont('Arial', 24, True, True)
text2 = pg.font.SysFont('Arial', 16, True, False)
text3 = pg.font.SysFont('Arial', 50, True, True)
txt = text3.render('GAME OVER', True, pg.Color('red'), None)
txt_w, txt_h = text3.size('GAME OVER')
txt_pos = ((W - txt_w) // 2, (H - txt_h) // 2)
txt2 = text3.render('MOTORWAY', True, pg.Color('blue'), None)
txt2_w, txt2_h = text3.size('MOTORWAY')
txt2_pos = ((W - txt2_w) // 2, (H - txt2_h) // 2)
txt3 = text1.render("key 'p' - pause", True, WHITE, None)
txt3_w = text1.size("key 'p' - pause")[0]
txt3_pos = ((W - txt3_w) // 2, 480)
txt_km = text2.render('km/h', True, WHITE, None)
txt_km_pos = (745, 550)

pg.display.set_icon(pg.image.load('img/car.png'))
pg.display.set_caption('Motorway')
pg.mouse.set_visible(True)
screen = pg.display.set_mode((W, H))

tick = pg.mixer.Sound('sound/ticking.wav')
sound_three = pg.mixer.Sound('sound/three.wav')
sound_car_accident = pg.mixer.Sound('sound/accident.wav')
sound_canister = pg.mixer.Sound('sound/canister.wav')
sound_length = sound_canister.get_length() * 1000
sound_start = pg.mixer.Sound('sound/Car Vroom.wav')
if os.name == 'nt':
    pg.mixer.music.load('sound/fon.mp3')
else:
    pg.mixer.music.load('sound/motorway.wav')


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.orig_image = self.image
        self.angle = angle
        self.speed = speed
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.position += self.velocity
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, image, dy, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.flip(image, False, dy)
        self.x = x
        self.y = y
        self.h = image.get_height()
        self.w = image.get_width() // 2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        group.add(self)
        self.speed = random.randint(3, 5)
        self.car_x, self.car_y, self.car_dy = False, False, False

    def create_car(self):
        block = 0
        direction = random.randint(0, 1)
        if direction == 0:
            self.car_y = - self.h
            self.car_dy = True
            self.car_x = random.randrange(80, W // 2, 80)
        elif direction == 1:
            self.car_y = H + self.h
            self.car_dy = False
            self.car_x = random.randrange(W // 2 + 80, W, 80)
        for img in cars:
            if self.car_x == img.rect.x + img.rect.w // 2:
                block = 1
        if block == 0:
            num = random.randint(0, n)
            if num == 3:
                original_color = CARS[num].get_at((self.w, self.h // 2))
                arr = pg.PixelArray(CARS[num])
                arr.replace(original_color, pg.Color(random.choice(COLOR)), 0.1)
                del arr
            new_car = Car(self.car_x, self.car_y, CARS[num], self.car_dy, cars)
            all_sprites.add(new_car, layer=2)

    def update(self):
        global drove_cars
        if self.x < W // 2:
            self.rect.y += self.speed
            if self.rect.y > H + self.h:
                self.kill()
                drove_cars += 1
        if self.x > W // 2:
            self.rect.y -= self.speed - 1
            if self.rect.y < 0 - self.h:
                self.kill()
                drove_cars += 1


class Background(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((W, H))
        self.image.fill(BG)
        pg.draw.line(self.image, (0, 128, 0), [20, 0], [20, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [780, 0], [780, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [400, 0], [400, 600], 80)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, (200, 200, 200),
                    [40 + xx * 80, 0 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 10 + yy * 60],
                    [40 + xx * 80, 600 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 50 + yy * 60], 5)
        self.speed = speed
        group.add(self)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = - H


class Other(pg.sprite.Sprite):
    def __init__(self, x, y, image, h):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        if image is canister_image or image is image_3 or image is water_image:
            self.image = image
        else:
            self.image = pg.transform.scale(image, (image.get_width() // 2, h // 2))
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            if self is canister or self is three or self is water:
                self.kill()
            if self in trees and level_game == 2:
                index = random.randint(0, 5)
                home = Other(x=self.rect.x, y=self.rect.y, image=home_images[index], h=home_images[index].get_height())
                self.kill()
                homes.add(home)
                all_sprites.add(home, layer=4)
            elif self in homes and level_game == 3:
                flower = Other(x=self.rect.x, y=self.rect.y, image=flower_image, h=flower_image.get_height())
                self.kill()
                flowers.add(flower)
                all_sprites.add(flower, layer=4)
            self.rect.y = - H


cars = pg.sprite.Group()
roads = pg.sprite.Group()
trees = pg.sprite.Group()
homes = pg.sprite.Group()
flowers = pg.sprite.Group()
all_sprites = pg.sprite.LayeredUpdates()

player = Player(x=W // 2 + 80, y=H // 2, angle=0, image=player_image)
car = Car(random.randrange(80, W // 2, 80), 0, CARS[random.randint(0, n)], True, cars)
for i in range(2):
    bg = Background(x=0, y=0 if i == 0 else -H, group=roads)
canister = Other(x=random.randrange(W // 2 + 80, W, 80) - canister_image.get_width() // 2,
                 y=-canister_image.get_height(), image=canister_image,
                 h=canister_image.get_height())
three = Other(x=random.randrange(80, W // 2, 80) - image_3.get_width() // 2,
              y=-image_3.get_height(), image=image_3, h=image_3.get_height())
water = Other(x=random.randrange(80, W // 2, 80) - water_image.get_width() // 2,
              y=-water_image.get_height(), image=water_image, h=water_image.get_height())

canisters = pg.sprite.Group(canister)
threes = pg.sprite.Group(three)
waters = pg.sprite.Group(water)
all_sprites.add(car, layer=2)


def speedometer():
    value = 0
    for deg in range(5, 84, 6):
        length = 20 if deg == 5 or deg == 23 or deg == 41 or deg == 59 or deg == 77 else 10
        cos = math.cos(math.radians(deg))
        sin = math.sin(math.radians(deg))
        pg.draw.line(
            screen, WHITE,
            [W - radius * cos, H - radius * sin],
            [W - (radius - length) * cos, H - (radius - length) * sin], 2)
    for deg in range(9, 78, 17):
        cos = math.cos(math.radians(deg))
        sin = math.sin(math.radians(deg))
        screen.blit(
            text2.render(str(value), True, WHITE, None),
            (W - (radius - 30) * cos, H - (radius - 30) * sin))
        value += 100
    screen.blit(txt_km, txt_km_pos)
    s = abs(30 - player.velocity.y * 14 if player.velocity.y <= 0 else 24 - player.velocity.y * 14)
    cos = math.cos(math.radians(s))
    sin = math.sin(math.radians(s))
    pg.draw.line(
        screen, (255, 0, 0), [W, H],
        [W - (radius - 10) * cos, H - (radius - 10) * sin], 4)
    pg.draw.circle(screen, WHITE, [W, H], 25, 0)


def game_over():
    screen.fill(BG)
    screen.blit(bg.image, (0, 0))
    pg.draw.ellipse(screen, pg.Color('lime green'), (100, 50, 600, 500), 0)
    if start:
        screen.blit(txt2, txt2_pos)
    else:
        screen.blit(txt, txt_pos)
    screen.blit(image_3, (80 - image_3.get_width() // 2, 20))
    screen.blit(canister_image, (W - 80 - canister_image.get_width() // 2, 20))
    screen.blit(text1.render('-3 car accident', True, pg.Color('lime green'), BG), (115, 25))
    screen.blit(text1.render('+40 liters', True, pg.Color('lime green'), BG), (580, 25))
    screen.blit(txt3, txt3_pos)
    play_btn = screen.blit(
        image_btn1, ((W - image_btn1.get_width()) // 2, (H - image_btn1.get_height()) // 2 - 100))
    out_btn = screen.blit(
        image_btn2, ((W - image_btn2.get_width()) // 2, (H - image_btn2.get_height()) // 2 + 100))
    return play_btn, out_btn


while game:
    clock.tick(FPS)
    if pg.event.get(pg.QUIT):
        break
    for e in pg.event.get():
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
        elif e.type == u1_event and stop == 0:
            car.create_car()
        elif e.type == u2_event and stop == 0:
            canisters.add(canister)
            all_sprites.add(canister, layer=1)
            canister.rect.center = random.randrange(W // 2 + 80, W, 80), - canister.h
            timer = random.randrange(7000, 27001, 5000)
            pg.time.set_timer(u2_event, timer)
            if timer >= 17000:
                threes.add(three)
                all_sprites.add(three, layer=1)
                three.rect.center = random.randrange(80, W // 2, 80), - three.h * random.randint(20, 30)
            if timer <= 7000 + 5000 * (level_game - 1):
                waters.add(water)
                all_sprites.add(water, layer=1)
                water.rect.center = random.randrange(W // 2 + 80, W, 80), - water.h * random.randint(15, 20)
        elif e.type == pg.KEYDOWN and e.key == pg.K_f:
            f_screen.reverse()
            if f_screen[0] == 1:
                screen = pg.display.set_mode((W, H))
            elif f_screen[0] == 2:
                screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if play.collidepoint(e.pos):
                    sound_start.play()
                    pg.mouse.set_visible(False)
                    for nx in range(3):
                        for ny in range(6):
                            tree = Other(x=nx * 380, y=-H + ny * 200, image=tree_image, h=tree_image.get_height())
                            trees.add(tree)
                            all_sprites.add(tree, layer=4)
                    all_sprites.add(*roads, layer=0)
                    all_sprites.add(player, layer=3)
                    player.position.x, player.position.y = W // 2 + 80, H // 2
                    player.angle = 0
                    player.update()
                    car_accident = 0
                    drove_cars = 0
                    level = 40
                    level_game = 1
                    stop = 0
                    start = False
                    pause = [False, True]
                    pg.mixer.music.play(loops=-1)
                elif out.collidepoint(e.pos):
                    game = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_p:
            if start is False:
                pause.reverse()
                if pause[0] is False:
                    stop = 0
                    pg.mixer.music.unpause()
                else:
                    stop = 1
                    pg.mixer.music.pause()
                    sound_car_accident.stop()
                    sound_canister.stop()
                    tick.stop()

    if stop == 0:
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            player.velocity.x = speed
            player.angle -= 1
            if player.angle < -20:
                player.angle = -20
        elif keys[pg.K_LEFT]:
            player.velocity.x = -speed
            player.angle += 1
            if player.angle > 20:
                player.angle = 20
        else:
            player.velocity.x = 0
            if player.angle < 0:
                player.angle += 1
            elif player.angle > 0:
                player.angle -= 1
        if keys[pg.K_UP]:
            player.velocity.y -= acceleration
            if player.velocity.y < -speed * 2:
                player.velocity.y = -speed * 2
        elif keys[pg.K_DOWN]:
            player.velocity.y += acceleration
            if player.velocity.y > speed + 1:
                player.velocity.y = speed + 1
        else:
            if player.velocity.y < 0:
                player.velocity.y += acceleration
                if player.velocity.y > 0:
                    player.velocity.y = 0
            elif player.velocity.y > 0:
                player.velocity.y -= acceleration
                if player.velocity.y < 0:
                    player.velocity.y = 0

        if player.position.x > W - 40:
            player.position.x = W - 40
        elif player.position.x < 40:
            player.position.x = 40
        elif player.position.y > H:
            player.position.y = H
        elif player.position.y < 0:
            player.position.y = 0

        if pg.sprite.spritecollide(player, cars, True):
            sound_car_accident.play()
            player.angle = random.randrange(-65, 65, 25)
            car_accident += 1
        if pg.sprite.spritecollideany(player, trees) or pg.sprite.spritecollideany(player, homes)\
           or pg.sprite.spritecollideany(player, flowers):
            player.angle = -60
            player.velocity.y = speed
        if pg.sprite.spritecollide(player, canisters, True):
            sound_canister.play(maxtime=int(sound_length - level * 40))
            level = 40
        if pg.sprite.spritecollide(player, threes, True, pg.sprite.collide_circle_ratio(1.0)):
            if car_accident >= 3:
                sound_three.play()
                car_accident -= 3
        if pg.sprite.spritecollideany(player, waters, pg.sprite.collide_circle_ratio(0.8)):
            sound_car_accident.play()
            sound_car_accident.fadeout(500)
            player.angle = random.randint(60, 181)
            player.position.y -= 4
            player.position.x += random.randrange(-20, 23, 6)

        if 100 <= drove_cars < 300:
            if int((str(drove_cars))[0]) == level_game:
                level_game += 1

        if level <= 0 or car_accident >= 10:
            all_sprites.empty()
            cars.empty()
            trees.empty()
            homes.empty()
            flowers.empty()
            canister.kill()
            three.kill()
            water.kill()
            pg.mouse.set_visible(True)
            tick.stop()
            pg.mixer.music.stop()
            stop = 1
        elif level == 40:
            R, G = 0, 255
            tick.stop()
            stop_tick = 0
        elif 10 < level <= 15:
            R, G = 255, 255
        elif 0 < level <= 10:
            R, G = 255, 0
            if stop == 0:
                if stop_tick == 0:
                    tick.play(-1)
                    stop_tick = 1

        if player.position.x > W // 2:
            level -= round(0.01 + abs(player.velocity.y) / 1000.0, 3)
        else:
            level -= 0.02

        all_sprites.update()
        all_sprites.draw(screen)
        pg.draw.rect(screen, (R, G, B), (710, 55 - level, 20, level))
        speedometer()
        screen.blit(fuel_image, (700, 5))
        screen.blit(text2.render(f'FPS: {int(clock.get_fps())}', True, WHITE, None), (367, 10))
    else:
        if pause[0] is False:
            play, out = game_over()
            d = open('Record/record.dat', 'r')
            record = int(d.read())
            d.close()
            if record < drove_cars:
                record = drove_cars
                d = open('Record/record.dat', 'w')
                d.write(str(record))
                d.close()
            screen.blit(text1.render(f'RECORD: {record}', True, WHITE, None),
                                    ((W - text1.size(f'RECORD: {record}')[0]) // 2, 90))
    screen.blit(text1.render(f'Car accident: {car_accident}  Drove cars: {drove_cars}',
                             True, pg.Color('lime green'), None if stop == 1 else BG), (50, 570))
    screen.blit(text1.render(str(level_game), True, WHITE, None), (W - 25, 10))
    pg.display.update()

print(f'car accident: {car_accident}\ndrove cars: {drove_cars}')
sys.exit(0)
