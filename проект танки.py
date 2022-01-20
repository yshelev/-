import random, pygame, sys
from math import cos, acos, sin

pygame.init()

FPS = 50

number_of_tracks = 4
current_track = 0
tracks = ["C418_-_Minecraft_30921694.mp3",
          "C418_-_Haggstrom_30921643.mp3",
          "C418_-_Living_Mice_30921638.mp3",
          "C418_-_Subwoofer_Lullaby_30921632.mp3"]
random.shuffle(tracks)


def music_player():
    global number_of_tracks
    global current_track
    if pygame.mixer.music.get_busy():
        return
    else:
        current_track += 1
        if current_track >= number_of_tracks:
            current_track = 0

        pygame.mixer.music.load("data/" + tracks[current_track])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
def finish_screen():
    result = defeated_tanks * 3 - all_shots - lose * 6 - losed_hp
    with open('info.txt', 'w') as f:
        f.write('number of deaths: ' + str(lose) + "\n")
        f.write('number of destroyed tanks: ' + str(defeated_tanks) + "\n")
        f.write('total shots fired: ' + str(all_shots) + "\n")
        f.write('result: ' + str(result))
    if result < 0:
        intro_text = ["к сожалению, вы проиграли, но достойно сражались!",
                      "спасибо за игру",
                      'ваш результат: ' + str(result)]
    else:
        intro_text = ['вы победили!',
                      'спасибо за игру!!',
                      'ваш результат: ' + str(result)]

    fon = pygame.image.load('data/end_fon.jpg')
    fon1 = pygame.transform.scale(fon, (WIDTH, HEIGHT))
    screen.blit(fon1, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def draw_location(lvl):
    for i in vertical_borders:
        i.kill()
    for j in horizontal_borders:
        j.kill()
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    if lvl == 1:
        Border(300, 5, 300, 600)
        Border(320, 5, 320, 285)
        Border(320, 305, 600, 305)
        Border(320, 305, 320, 600)
        Border(320, 285, 620, 325)
        Border(600, 305, 600, 600)
        Border(620, 285, 620, 600)
        Border(300, 600, 320, 600)
        Border(600, 600, 620, 600)
    if lvl == 2:
        Border(5, 390, 450, 390)
        Border(5, 410, 450, 410)
        Border(450, 390, 450, 410)
        Border(550, 390, 550, 410)
        Border(550, 390, 995, 390)
        Border(550, 410, 995, 410)
    if lvl == 3:
        pass


def blitRotate(surf, image, pos, originPos, angle):
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (pos[0] + min_box[0], pos[1] - max_box[1])

    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image


def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    x, y = rect.center
    rot_rect = rot_image.get_rect(center=(x, y))
    return rot_image, rot_rect


def terminate():
    pygame.quit()
    sys.exit()


def draw_normal_name(scr):
    normal_name = {0: 'normal weapon',
                       1: 'normal weapon with a ricochet',
                       2: 'shotgun'}
    font = pygame.font.Font(None, 25)
    text = font.render(f"weapon type = {normal_name[our_tank[1].weapon_type]}", True, (0, 0, 0))
    text_x = 10
    text_y = 775
    scr.blit(text, (text_x, text_y))

def draw_hp(scr):
    font = pygame.font.Font(None, 25)
    text = font.render(f"hp = {our_tank[0].hp}", True, (0, 0, 0))
    text_x = 10
    text_y = 755
    scr.blit(text, (text_x, text_y))

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "вы стреляете, убиваете с 1,",
                  "в вас надо попасть трижды"]

    fon = pygame.image.load('data/start_fon.jpg')
    fon1 = pygame.transform.scale(fon, (WIDTH, HEIGHT))
    screen.blit(fon1, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
            pygame.display.flip()
        clock.tick(FPS)

class AnimatedSmoke(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, bool, number_of_tank, flag):
        super().__init__(all_sprite)
        self.frames = []
        self.sheet = sprites['smoke']
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.count = 0
        self.rect = self.rect.move(x, y)
        self.speed = 5
        self.bool = bool
        self.number = number_of_tank
        self.flag = flag

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // columns,
                                self.sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x, y, event_type):
        if event_type == 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.count += 1
            if self.count == 30:
                self.kill()

class AnimatedFire(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y):
        super().__init__(all_sprite)
        self.sheet = sprites['fire']
        self.frames = []
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.count = 0
        self.rect = self.rect.move(x, y)
        self.speed = 5

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // columns,
                                self.sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x, y, event_type):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.count += 1
        if self.count == 20:
            self.kill()


class VS_tank_gun(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type, number_of_tank):
        super().__init__(all_sprite)
        self.image = pygame.image.load('data/new_tank_gun.jpg')
        self.image_start_gun = pygame.image.load('data/new_tank_gun.jpg')
        self.image_start_gun = pygame.transform.scale(self.image_start_gun
                                                      , (50, 100))
        self.image_start_gun = pygame.transform.rotate(self.image_start_gun, 180)
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_start_gun.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.die = False
        self.weapon_type = weapon_type
        self.number = number_of_tank
        all_sprite.add(self)
        all_vs_tanks_sprites.add(self)

    def update(self, x, y, event_type):
        global defeated_tanks
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 2:
                defeated_tanks += 1
                pygame.sprite.spritecollide(self, all_shot, True)
                self.die = True
                pygame.sprite.spritecollide(self, all_vs_tanks_sprites, False)[0].kill()
                self.kill()
                all_vs_tanks[self.number][0].kill()

        if event_type == 3 + self.number:
            pred_rect = self.rect.move(0, 0)
            self.rect = self.rect.move(x * self.speed, y * self.speed)
            if not all_vs_tanks[self.number][0].can_move:
                self.rect = pred_rect

        if event_type == 6:
            coord = [self.rect.x, self.rect.y]
            target = [x, y]
            delta_x = coord[0] + 13 - target[0]
            delta_y = coord[1] + 40 - target[1]
            long = (delta_x ** 2 + delta_y ** 2) ** 0.5
            try:
                angle = acos(delta_x / long) * (1 if delta_y > 0 else -1)
            except ZeroDivisionError:
                angle = acos(delta_x / 1) * (1 if delta_y > 0 else -1)
            self.image, self.rect = rot_center(self.image_start_gun, self.rect, -angle * 57 - 90)


class VS_tank_gus(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__(all_sprite)
        self.image = pygame.image.load('data/tank_gus.jpg')
        self.image_start_gus = pygame.image.load('data/tank_gus.jpg')
        self.image_start_gus = pygame.transform.scale(self.image_start_gus
                                                      , (75, 75))
        self.image = pygame.transform.scale(self.image, (75, 75))

        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.start_pos_x = x
        self.start_pos_y = y
        self.rect.x = x
        self.rect.y = y
        self.die = False
        self.can_move = True
        self.move_to_coord = True
        self.number = number
        self.speed = 5
        all_sprite.add(self)
        all_vs_tanks_sprites.add(self)

    def update(self, x, y, event_type):
        global defeated_tanks
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 2:
                defeated_tanks += 1
                pygame.sprite.spritecollide(self, all_shot, True)
                pygame.sprite.spritecollide(self, all_vs_tanks_sprites, False)[1].kill()
                self.die = True
                self.kill()
                all_vs_tanks[self.number][1].kill()

        if event_type == 3 + self.number:
            self.move(x, y)
            self.rotate(x, y)


    def move(self, x, y):
        pred_rect = self.rect.move(0, 0)
        self.rect = self.rect.move(x * self.speed, y * self.speed)

        if pygame.sprite.spritecollide(self, horizontal_borders, False) or \
                pygame.sprite.spritecollide(self, vertical_borders, False) or \
                pygame.sprite.spritecollide(self, all_our_tanks_sprite, False):
            self.rect = pred_rect
            self.can_move = False
        else:
            self.can_move = True

    def rotate(self, x, y):
            pos = (screen.get_width() / 2, screen.get_height() / 2)
            pos = (200, 200)
            w, h = self.image.get_size()
            if x == 0:
                if y == -1:
                    self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 180)
                elif y == 1:
                    self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 0)
            elif x == 1:
                if y == 0:
                    self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 90)
            else:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 270)



class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprite)
        if x1 == x2:
            vertical_borders.add(self)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            horizontal_borders.add(self)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Our_tank_gus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprite)
        self.image = pygame.image.load('data/tank_gus.jpg')
        self.image_start_gus = pygame.image.load('data/tank_gus.jpg')
        self.image_start_gus = pygame.transform.scale(self.image_start_gus
                                                      , (75, 75))
        self.image = pygame.transform.scale(self.image, (75, 75))

        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 3
        self.die = False
        self.can_move = True
        self.speed = 5
        all_sprite.add(self)
        all_our_tanks_sprite.add(self)

    def update(self, x, y, event_type):
        global losed_hp
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 0:
                rect = pygame.sprite.spritecollide(self, all_shot, False)[0].rect
                x, y = rect.x, rect.y
                AnimatedFire(5, 4, x, y)
                self.hp -= 1
                losed_hp += 1
                pygame.sprite.spritecollide(self, all_shot, True)
                if not self.hp:
                    self.die = True
                    our_tank[1].kill()
                    self.kill()
        if event_type == 0:
            self.move(x, y)
            self.rotate(x, y)

    def move(self, x, y):
        pred_rect = self.rect.move(0, 0)
        self.rect = self.rect.move(x * self.speed, y * self.speed)

        if pygame.sprite.spritecollide(self, horizontal_borders, False) or \
            pygame.sprite.spritecollide(self, vertical_borders, False) or \
            pygame.sprite.spritecollide(self, all_vs_tanks_sprites, False):
            self.rect = pred_rect
            self.can_move = False
        else:
            self.can_move = True



    def rotate(self, x, y):
        pos = (screen.get_width() / 2, screen.get_height() / 2)
        pos = (200, 200)
        w, h = self.image.get_size()
        if x == 0:
            if y == -1:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 180)
            elif y == 1:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 0)
        elif x == 1:
            if y == 0:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 90)
        else:
            self.image = blitRotate(screen, self.image_start_gus, pos, (w / 2, h / 2), 270)


class Our_tank_gun(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type):
        super().__init__(all_sprite)
        self.image = pygame.image.load('data/new_tank_gun.jpg')
        self.image_start_gun = pygame.image.load('data/new_tank_gun.jpg')
        self.image_start_gun = pygame.transform.scale(self.image_start_gun
                                                      , (50, 100))
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_start_gun.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.can_move = True
        self.weapon_type = weapon_type
        self.die = False
        all_sprite.add(self)
        all_our_tanks_sprite.add(self)

    def update(self, x, y, event_type):
        global losed_hp
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 0:
                pygame.sprite.spritecollide(self, all_shot, True)
                our_tank[0].hp -= 1
                losed_hp += 1
                if not our_tank[0].hp:
                    self.die = True
                    our_tank[0].kill()
                    self.kill()

        if event_type == 0:
            pred_rect = self.rect.move(0, 0)
            self.rect = self.rect.move(x * self.speed, y * self.speed)
            if not our_tank[0].can_move:
                self.rect = pred_rect

        if event_type == 2:
            coord = [self.rect.x, self.rect.y]
            target = [x, y]
            delta_x = coord[0] + 13 - target[0]
            delta_y = coord[1] + 40 - target[1]
            long = (delta_x ** 2 + delta_y ** 2) ** 0.5
            try:
                angle = acos(delta_x / long) * (1 if delta_y > 0 else -1)
            except ZeroDivisionError:
                angle = acos(delta_x / 1) * (1 if delta_y > 0 else -1)
            self.image, self.rect = rot_center(self.image_start_gun, self.rect, -angle * 57 + 90)

class Shot(pygame.sprite.Sprite):
    def __init__(self, coord, target, type, bool, number):
        super().__init__(all_sprite)
        self.image = sprites['shot']
        self.image_start_patr = self.image
        self.image = pygame.transform.scale(self.image
                                            , (15, 15))
        self.image_start_patr = pygame.transform.scale(self.image
                                            , (15, 15))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_start_patr.set_colorkey(self.image.get_at((0, 0)))
        self.type = type
        self.whose_shot = bool
        self.number = number
        coord = list(coord)
        self.x_y = list((coord[0], coord[1]))
        delta_x = coord[0] - target[0]
        delta_y = coord[1] - target[1]
        long = (delta_x ** 2 + delta_y ** 2) ** 0.5
        try:
            angle = acos(delta_x / long) * (1 if delta_y > 0 else -1)
        except ZeroDivisionError:
            angle = acos(delta_x / 1) * (1 if delta_y > 0 else -1)
        speed = 10
        self.speed_x = -cos(angle) * speed
        self.speed_y = -sin(angle) * speed
        self.angle = -angle * 57 + 90
        self.rect = pygame.Rect(int(self.x_y[0]), int(self.x_y[1]), 20, 20)
        self.image, self.rect = rot_center(self.image_start_patr, self.rect, self.angle)
        self.rect = self.rect.move(self.speed_x * 5, self.speed_y * 5)
        if self.type == 1:
            self.count = 0
        all_sprite.add(self)
        all_shot.add(self)
        smoke = AnimatedSmoke(6, 5, self.rect.x, self.rect.y, self.whose_shot, self.number, True)

    def update(self, x, y, event_type):
        if event_type == 1:
            if self.type == 1:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    self.whose_shot = 1
                    self.speed_y = -self.speed_y
                    if self.speed_y <= 0:
                        self.angle = 180 - self.angle
                    else:
                        self.angle = -180 - self.angle
                    self.image, self.rect = rot_center(self.image_start_patr, self.rect, self.angle)
                    self.count += 1
                    if self.count == 3:
                        self.kill()
                        fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    self.speed_x = -self.speed_x
                    self.angle = -self.angle
                    self.image, self.rect = rot_center(self.image_start_patr, self.rect, self.angle)
                    self.count += 1
                    self.whose_shot = 1
                    if self.count == 3:
                        self.kill()
                        fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)
            elif self.type == 0:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    self.kill()
                    fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    self.kill()
                    fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)
            elif self.type == 2:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    self.kill()
                    fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    self.kill()
                    fire = AnimatedFire(5, 4, self.rect.x, self.rect.y)


pygame.display.set_caption('Pull up on the tank, и я еду в бой')
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sprite = pygame.sprite.Sprite()
all_sprite = pygame.sprite.Group()
all_shot = pygame.sprite.Group()
all_vs_tanks_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_our_tanks_sprite = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True

image = pygame.image.load('data/пуля.jpg')
fire_sheet = pygame.image.load('data/animated_fire.png')
smoke_sheet = pygame.image.load('data/animated_smoke.png')
sprites = {"smoke": smoke_sheet, "fire":  fire_sheet, 'shot': image}

size = 10
y = 0
lvl = 1
start_pos_x, start_pos_y = 500, 500

our_tank = (Our_tank_gus(start_pos_x, start_pos_y), Our_tank_gun(start_pos_x + 12, start_pos_y - 15, 0))
vs_tank_0 = (VS_tank_gus(10, 20, 0), VS_tank_gun(17, 5, 2, 0))
vs_tank_1 = (VS_tank_gus(450, 20, 1), VS_tank_gun(462, 5, 2, 1))
vs_tank_2 = (VS_tank_gus(800, 20, 2), VS_tank_gun(812, 5, 2, 2))
all_vs_tanks = [vs_tank_0, vs_tank_1, vs_tank_2]

Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)


start_screen()
music_player()

flag_gun = 0

flag_shot = True
count_shot = 0

lose, defeated_tanks, all_shots, losed_hp = 0, 0, 0, 0
coord_to_move = {0: [random.randint(all_vs_tanks[0][0].start_pos_x - 100, all_vs_tanks[0][0].start_pos_x + 100),
                     random.randint(all_vs_tanks[0][0].start_pos_y - 100, all_vs_tanks[0][0].start_pos_y + 100)],
                 1: [random.randint(all_vs_tanks[1][0].start_pos_x - 100, all_vs_tanks[1][0].start_pos_x + 100),
                     random.randint(all_vs_tanks[1][0].start_pos_y - 100, all_vs_tanks[1][0].start_pos_y + 100)],
                 2: [random.randint(all_vs_tanks[2][0].start_pos_x - 100, all_vs_tanks[2][0].start_pos_x + 100),
                     random.randint(all_vs_tanks[2][0].start_pos_y - 100, all_vs_tanks[2][0].start_pos_y + 100)]}

flag_change = 0
count_change = 0

vs_tank_count_shot = 0
vs_tank_flag_shot = True

count_move_vs_tank = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if flag_shot:
                if not our_tank[1].die:
                    all_shots += 1
                    if our_tank[1].weapon_type == 2:
                        shotgun_shot_0 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x, y], 2, 0, -1)
                        shotgun_shot_1 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x + 50, y + 50], 2, 0, -1)
                        shotgun_shot_2 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x - 50, y - 50], 2, 0, -1)
                    else:
                        shot = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25], [x, y],
                                    our_tank[1].weapon_type, 0, -1)
                    flag_gun = 1
                    flag_shot = False

    if not flag_shot:
        if count_shot == 30:
            flag_shot = True
            count_shot = 0
        else:
            count_shot += 1
    if flag_gun:
        all_sprite.update(x, y, 2)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not flag_change:
            flag_change = 1
            if our_tank[1].weapon_type == 2:
                our_tank[1].weapon_type = 0
            else:
                our_tank[1].weapon_type += 1
    if flag_change:
        if count_change == 3:
            flag_change = 0
            count_change = 0
        else:
            count_change += 1
    if keys[pygame.K_w]:
        all_sprite.update(0, -1, 0)
    elif keys[pygame.K_a]:
        all_sprite.update(-1, 0, 0)
    elif keys[pygame.K_s]:
        all_sprite.update(0, 1, 0)
    elif keys[pygame.K_d]:
        all_sprite.update(1, 0, 0)


    for i in range(3):
        if not all_vs_tanks[i][0].move_to_coord:
            if all_vs_tanks[i][0].start_pos_x - 20 <= all_vs_tanks[i][0].rect.x <= all_vs_tanks[i][0].start_pos_x + 20 \
                    and \
            all_vs_tanks[i][0].start_pos_y - 20 <= all_vs_tanks[i][0].rect.y <= all_vs_tanks[i][0].start_pos_y + 20:
                all_vs_tanks[i][0].move_to_coord = True
                coord_to_move[i] = [random.randint(all_vs_tanks[i][0].start_pos_x - 100,
                                                   all_vs_tanks[i][0].start_pos_x + 100),
                                    random.randint(all_vs_tanks[i][0].start_pos_y - 100,
                                                   all_vs_tanks[i][0].start_pos_y + 100)]
            else:
                if all_vs_tanks[i][0].start_pos_x - 20 <= all_vs_tanks[i][0].rect.x <= all_vs_tanks[i][0].start_pos_x + 20:
                    if all_vs_tanks[i][0].start_pos_y < all_vs_tanks[i][0].rect.y:
                        move_x, move_y = 0, -1
                    elif all_vs_tanks[i][0].start_pos_y > all_vs_tanks[i][0].rect.y:
                        move_x, move_y = 0, 1
                else:
                    if all_vs_tanks[i][0].start_pos_x < all_vs_tanks[i][0].rect.x:
                        move_x, move_y = -1, 0
                    if all_vs_tanks[i][0].start_pos_x > all_vs_tanks[i][0].rect.x:
                        move_x, move_y = 1, 0

        else:
            if coord_to_move[i][0] - 20 <= all_vs_tanks[i][0].rect.x <= coord_to_move[i][0] + 20 and\
                coord_to_move[i][1] - 20 <= all_vs_tanks[i][0].rect.y <= coord_to_move[i][1] + 20:
                all_vs_tanks[i][0].move_to_coord = False
                coord_to_move[i] = [random.randint(all_vs_tanks[i][0].start_pos_x - 100,
                                                   all_vs_tanks[i][0].start_pos_x + 100),
                                    random.randint(all_vs_tanks[i][0].start_pos_y - 100,
                                                   all_vs_tanks[i][0].start_pos_y + 100)]
            else:
                if not all_vs_tanks[i][0].can_move:
                    coord_to_move[i] = [random.randint(all_vs_tanks[i][0].start_pos_x - 100,
                                                       all_vs_tanks[i][0].start_pos_x + 100),
                                        random.randint(all_vs_tanks[i][0].start_pos_y - 100,
                                                       all_vs_tanks[i][0].start_pos_y + 100)]
                if coord_to_move[i][0] - 20 <= all_vs_tanks[i][0].rect.x <= coord_to_move[i][0] + 20:
                    if coord_to_move[i][1] < all_vs_tanks[i][0].rect.y:
                        move_x, move_y = 0, -1
                    elif coord_to_move[i][1] > all_vs_tanks[i][0].rect.y:
                        move_x, move_y = 0, 1
                else:
                    if coord_to_move[i][0] < all_vs_tanks[i][0].rect.x:
                        move_x, move_y = -1, 0
                    if coord_to_move[i][0] > all_vs_tanks[i][0].rect.x:
                        move_x, move_y = 1, 0
        if i == 0:
            move_x_0, move_y_0 = move_x, move_y
        elif i == 1:
            move_x_1, move_y_1 = move_x, move_y
        else:
            move_x_2, move_y_2 = move_x, move_y

    all_sprite.update(move_x_0, move_y_0, 3)
    all_sprite.update(move_x_1, move_y_1, 4)
    all_sprite.update(move_x_2, move_y_2, 5)

    if vs_tank_flag_shot:
        if not (our_tank[1].die or our_tank[0].die):
            if not (all_vs_tanks[0][0].die or all_vs_tanks[0][1].die):
                if all_vs_tanks[0][1].weapon_type == 2:
                    shotgun_shot_0 = Shot([all_vs_tanks[0][0].rect.x + 25,all_vs_tanks[0][0].rect.y + 25],
                                          [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25], 2, 2, 0)
                    shotgun_shot_1 = Shot([all_vs_tanks[0][0].rect.x + 25, all_vs_tanks[0][0].rect.y + 25],
                                          [our_tank[0].rect.x + 75, our_tank[0].rect.y + 75], 2, 2, 0)
                    shotgun_shot_2 = Shot([all_vs_tanks[0][0].rect.x + 25, all_vs_tanks[0][0].rect.y + 25],
                                          [our_tank[0].rect.x - 25, our_tank[0].rect.y - 25], 2, 2, 0)
                else:
                    shot = Shot([all_vs_tanks[0][0].rect.x + 25, all_vs_tanks[0][0].rect.y + 25],
                                [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                all_vs_tanks[0][1].weapon_type, 2, 0)

            if not (all_vs_tanks[1][0].die or all_vs_tanks[1][1].die):
                if all_vs_tanks[1][1].weapon_type == 2:
                    shotgun_shot_0 = Shot([all_vs_tanks[1][0].rect.x + 25,all_vs_tanks[1][0].rect.y + 25],
                                          [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                          2, 2, 1)
                    shotgun_shot_1 = Shot([all_vs_tanks[1][0].rect.x + 25, all_vs_tanks[1][0].rect.y + 25],
                                          [our_tank[0].rect.x + 75, our_tank[0].rect.y + 75],
                                          all_vs_tanks[0][1].weapon_type, 2, 1)
                    shotgun_shot_2 = Shot([all_vs_tanks[1][0].rect.x + 25, all_vs_tanks[1][0].rect.y + 25],
                                          [our_tank[0].rect.x - 25, our_tank[0].rect.y - 25],
                                          all_vs_tanks[0][1].weapon_type, 2, 1)
                else:
                    shot = Shot([all_vs_tanks[1][0].rect.x + 25, all_vs_tanks[1][0].rect.y + 25],
                                [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                all_vs_tanks[1][1].weapon_type, 2, 1)

            if not (all_vs_tanks[2][0].die or all_vs_tanks[2][1].die):
                if all_vs_tanks[2][1].weapon_type == 2:
                    shotgun_shot_0 = Shot([all_vs_tanks[2][0].rect.x + 25, all_vs_tanks[2][0].rect.y + 25],
                                          [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25], 2, 2, 2)
                    shotgun_shot_1 = Shot([all_vs_tanks[2][0].rect.x + 25, all_vs_tanks[2][0].rect.y + 25],
                                          [our_tank[0].rect.x + 75, our_tank[0].rect.y + 75], 2, 2, 2)
                    shotgun_shot_2 = Shot([all_vs_tanks[2][0].rect.x + 25, all_vs_tanks[2][0].rect.y + 25],
                                          [our_tank[0].rect.x - 25, our_tank[0].rect.y - 25], 2, 2, 2)
                else:
                    shot = Shot([all_vs_tanks[2][0].rect.x + 25, all_vs_tanks[2][0].rect.y + 25],
                                [our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                all_vs_tanks[2][1].weapon_type, 2, 2)
            vs_tank_flag_shot = False

    if not vs_tank_flag_shot:
        if vs_tank_count_shot == 40:
            vs_tank_flag_shot = True
            vs_tank_count_shot = 0
        else:
            vs_tank_count_shot += 1
    if not all_vs_tanks_sprites:
        if all_sprite:
            for i in all_sprite:
                i.kill()
        if lvl == 3:
            finish_screen()
            pygame.quit()
        lvl += 1
        our_tank = (Our_tank_gus(start_pos_x, start_pos_y), Our_tank_gun(start_pos_x + 12, start_pos_y - 15, 0))
        vs_tank_0 = (VS_tank_gus(10, 5, 0), VS_tank_gun(17, -10, 2, 0))
        vs_tank_1 = (VS_tank_gus(450, 5, 1), VS_tank_gun(462, -10, 2, 1))
        vs_tank_2 = (VS_tank_gus(800, 5, 2), VS_tank_gun(812, -10, 2, 2))
        all_vs_tanks = [vs_tank_0, vs_tank_1, vs_tank_2]
    if not all_our_tanks_sprite:
        lose += 1
        if all_sprite:
            for i in all_sprite:
                i.kill()
        if lvl == 3:
            finish_screen()

            pygame.quit()
        lvl += 1
        our_tank = (Our_tank_gus(start_pos_x, start_pos_y), Our_tank_gun(start_pos_x + 12, start_pos_y - 15, 0))
        vs_tank_0 = (VS_tank_gus(10, 5, 0), VS_tank_gun(17, -10, 2, 0))
        vs_tank_1 = (VS_tank_gus(450, 5, 1), VS_tank_gun(462, -10, 2, 1))
        vs_tank_2 = (VS_tank_gus(800, 5, 2), VS_tank_gun(812, -10, 2, 2))
        all_vs_tanks = [vs_tank_0, vs_tank_1, vs_tank_2]
    all_sprite.update(1, 0, 1)
    all_sprite.update(our_tank[0].rect.x, our_tank[0].rect.y, 6)
    screen.fill((255, 255, 255))
    draw_location(lvl)
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

    count_for_tanks = 0
    draw_normal_name(screen)
    draw_hp(screen)
    all_sprite.draw(screen)
    clock.tick(20)
    pygame.display.flip()

pygame.quit()
