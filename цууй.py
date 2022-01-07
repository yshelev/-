import random, pygame, sys
from math import cos, acos, sin

pygame.init()

FPS = 50


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
    text_y = 10
    scr.blit(text, (text_x, text_y))


def draw_hp(scr):
    font = pygame.font.Font(None, 25)
    text = font.render(f"hp = {our_tank[0].hp}", True, (0, 0, 0))
    text_x = 10
    text_y = 35
    scr.blit(text, (text_x, text_y))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если вы не будете уважать пуджа,",
                  "он вам накидает"]

    fon = pygame.image.load('data/fon.jpg')
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


class VS_tank_gun(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type):
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
        self.weapon_type = weapon_type
        all_sprite.add(self)
        all_vs_tanks_sprites.add(self)

    def update(self, x, y, event_type):
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 2:
                pygame.sprite.spritecollide(self, all_shot, True)
                all_sprite.remove(pygame.sprite.spritecollide(self, all_vs_tanks_sprites, False)[0])
                all_sprite.remove(self)
                self.die = True

        if event_type == 3:
            self.rect = self.rect.move(x * self.speed, y * self.speed)


class VS_tank_gus(pygame.sprite.Sprite):
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
        self.die = False
        self.speed = 5
        all_sprite.add(self)
        all_vs_tanks_sprites.add(self)

    def update(self, x, y, event_type):
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 2:
                pygame.sprite.spritecollide(self, all_shot, True)
                all_sprite.remove(pygame.sprite.spritecollide(self, all_vs_tanks_sprites, False)[1])
                all_sprite.remove(self)
                self.die = True
        if event_type == 3:
            self.move(x, y)
            self.rotate(x, y)

    def move(self, x, y):
        self.rect = self.rect.move(x * self.speed, y * self.speed)

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
        self.can_move = True
        all_sprite.add(self)

    def update(self, x, y, event_type):
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 0:
                pygame.sprite.spritecollide(self, all_shot, True)
                self.hp -= 1
                if not self.hp:
                    all_sprite.remove(our_tank[1])
                    all_sprite.remove(self)
        if event_type == 0:
            self.move(x, y)
            self.rotate(x, y)

    def move(self, x, y):
        speed = 5
        pred_rect = self.rect.move(0, 0)
        self.rect = self.rect.move(x * speed, y * speed)

        if pygame.sprite.spritecollide(self, horizontal_borders, False) or \
                pygame.sprite.spritecollide(self, vertical_borders, False):
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
        self.weapon_type = weapon_type
        self.die = False
        all_sprite.add(self)

    def update(self, x, y, event_type):
        if pygame.sprite.spritecollide(self, all_shot, False):
            if pygame.sprite.spritecollide(self, all_shot, False)[0].whose_shot != 0:
                pygame.sprite.spritecollide(self, all_shot, True)
                our_tank[0].hp -= 1
                if not our_tank[0].hp:
                    all_sprite.remove(our_tank[0])
                    all_sprite.remove(self)
                    self.die = True

        if event_type == 0:
            speed = 5
            pred_rect = self.rect.move(0, 0)
            self.rect = self.rect.move(x * speed, y * speed)
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
    def __init__(self, coord, target, type, bool):
        super().__init__(all_sprite)
        self.image = pygame.image.load('data/пуля.jpg')
        self.image_start_patr = pygame.image.load('data/пуля.jpg')
        self.image = pygame.transform.scale(self.image
                                            , (15, 15))
        self.image_start_patr = pygame.transform.scale(self.image
                                                       , (15, 15))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image_start_patr.set_colorkey(self.image.get_at((0, 0)))
        self.type = type
        self.whose_shot = 0
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
                        all_sprite.remove(self)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    self.speed_x = -self.speed_x
                    self.angle = -self.angle
                    self.image, self.rect = rot_center(self.image_start_patr, self.rect, self.angle)
                    self.count += 1
                    self.whose_shot = 1
                    if self.count == 3:
                        all_sprite.remove(self)
            elif self.type == 0:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    all_sprite.remove(self)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    all_sprite.remove(self)
            elif self.type == 2:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    all_sprite.remove(self)
                elif pygame.sprite.spritecollideany(self, vertical_borders):
                    all_sprite.remove(self)


pygame.display.set_caption('Pull up on the tank, и я еду в бой')
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sprite = pygame.sprite.Sprite()
all_sprite = pygame.sprite.Group()
all_shot = pygame.sprite.Group()
all_vs_tanks_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True

start_pos_x, start_pos_y = 500, 500

our_tank = (Our_tank_gus(start_pos_x, start_pos_y), Our_tank_gun(start_pos_x + 12, start_pos_y - 15, 0))
vs_tank_0 = (VS_tank_gus(500, 10), VS_tank_gun(515, 0, 0))
vs_tank_1 = (VS_tank_gus(600, 10), VS_tank_gun(615, 0, 0))
vs_tank_2 = (VS_tank_gus(700, 10), VS_tank_gun(715, 0, 0))
x_tunk, y_tunk = 500, 100 # x_tunk - это x танка(я так думаю); y_tunk - это перваночальная позиция пульки.
start_screen()

Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

flag = 0
flag_gun = 0
flag_shot = 0
count_shot = 0
flag_change = 0
count_change = 0

while running:
    y_tunk += 100  # Это скорость пули танка противника
    shot_gun_of_first_tunk = Shot([x_tunk + 25, y_tunk + 25],
                          [515, 0], 2, 0)
    shot_gun_of_second_tunk = Shot([600 + 25, y_tunk + 25],     # } Это выстрелы танков противника
                   [615, 0], 2, 0)
    shot_gun_of_third_tunk = Shot([700 + 25, y_tunk + 25],
                   [715, 0], 2, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not flag_shot:
                if not our_tank[1].die:
                    if our_tank[1].weapon_type == 2:

                        shotgun_shot_0 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x, y], 2, 0)
                        shotgun_shot_1 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x + 50, y + 50], 2, 0)
                        shotgun_shot_2 = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25],
                                              [x - 50, y - 50], 2, 0)
                    else:
                        shot = Shot([our_tank[0].rect.x + 25, our_tank[0].rect.y + 25], [x, y],
                                    our_tank[1].weapon_type, 0)


                    flag = 1
                    flag_gun = 1
                    flag_shot = 1

    if flag_shot:
        if count_shot == 10:
            flag_shot = 0
            count_shot = 0
        else:
            count_shot += 1
    if flag:
        all_sprite.update(x, y, 1)
    if flag_gun:
        all_sprite.update(x, y, 2)
        flag_gun = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not flag_change:
            flag_change = 1
            if our_tank[1].weapon_type == 2:
                our_tank[1].weapon_type = 0
            else:
                our_tank[1].weapon_type += 1
    if flag_change:
        if count_change == 10:
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
    all_sprite.update(0, 0.5, 3)
    all_sprite.update(0, 0.5, 4)
    screen.fill((255, 255, 255))
    draw_normal_name(screen)
    draw_hp(screen)
    all_sprite.draw(screen)
    clock.tick(20)
    pygame.display.flip()

pygame.quit()