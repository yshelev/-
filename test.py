import random, pygame, sys
from math import cos, acos, sin

pygame.init()

FPS = 50


def blitRotate(surf, image, pos, originPos, angle):
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
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

class Tank_gus(pygame.sprite.Sprite):
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
        all_sprite.add(self)

    def update(self, x, y, event_type):
        if event_type == 0:
            self.move(x, y)
            self.rotate(x, y)

    def move(self, x, y):
        speed = 10
        self.rect = self.rect.move(x * speed, y * speed)


    def rotate(self, x, y):
        pos = (screen.get_width() / 2, screen.get_height() / 2)
        pos = (200, 200)
        w, h = self.image.get_size()
        if x == 0:
            if y == -1:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w/2, h/2), 180)
            elif y == 1:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w/2, h/2), 0)
        elif x == 1:
            if y == 0:
                self.image = blitRotate(screen, self.image_start_gus, pos, (w/2, h/2), 90)
        else:
            self.image = blitRotate(screen, self.image_start_gus, pos, (w/2, h/2), 270)

    def retx_y(self):
        return self.rect.x, self.rect.y

class Tank_gun(pygame.sprite.Sprite):
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
        all_sprite.add(self)

    def update(self, x, y, event_type):
        if event_type == 0:
            speed = 10
            self.rect = self.rect.move(x * speed, y * speed)
            return self.rect.x, self.rect.y
        if event_type == 2:
            coord = [self.rect.x, self.rect.y]
            target = [x, y]
            delta_x = coord[0] - target[0]
            delta_y = coord[1] - target[1]
            long = (delta_x ** 2 + delta_y ** 2) ** 0.5
            try:
                angle = acos(delta_x / long) * (1 if delta_y > 0 else -1)
            except ZeroDivisionError:
                angle = acos(delta_x / 1) * (1 if delta_y > 0 else -1)
            self.image, self.rect = rot_center(self.image_start_gun, self.rect, -angle * 57 + 90)

class Shot(pygame.sprite.Sprite):
    def __init__(self, coord, target):
        super().__init__(all_sprite)
        self.image = self.image = pygame.image.load('data/пуля.jpg')
        self.image = pygame.transform.scale(self.image
                                                      , (20, 20))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        coord = list(coord)
        self.x_y = list((coord[0] + 15, coord[1]))
        delta_x = coord[0] - target[0]
        delta_y = coord[1] - target[1]
        long = (delta_x ** 2 + delta_y ** 2) ** 0.5
        try:
            angle = acos(delta_x / long) * (1 if delta_y > 0 else -1)
        except ZeroDivisionError:
            angle = acos(delta_x / 1) * (1 if delta_y > 0 else -1)
        speed = 20
        self.speed_x = -cos(angle) * speed
        self.speed_y = -sin(angle) * speed
        self.rect = pygame.Rect(int(self.x_y[0]), int(self.x_y[1]), 20, 20)
        all_sprite.add(self)

    def update(self, x, y, event_type):
        if event_type == 1:
            self.rect = self.rect.move(self.speed_x, self.speed_y)

pygame.display.set_caption('Pull up on the tank, и я еду в бой')
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sprite = pygame.sprite.Sprite()
all_sprite = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True

start_pos_x, start_pos_y = 500, 500

our_tank = (Tank_gus(start_pos_x, start_pos_y), Tank_gun(start_pos_x + 12, start_pos_y - 15, 0))

start_screen()
flag = 0
flag_1 = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            shot = Shot([our_tank[1].rect.x, our_tank[1].rect.y], [x, y])
            flag = 1
            flag_1 = 1

    if flag:
        all_sprite.update(x, y, 1)
    if flag_1:
        all_sprite.update(x, y, 2)
        flag_1 = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        all_sprite.update(0, -1, 0)
    elif keys[pygame.K_a]:
        all_sprite.update(-1, 0, 0)
    elif keys[pygame.K_s]:
        all_sprite.update(0, 1, 0)
    elif keys[pygame.K_d]:
        all_sprite.update(1, 0, 0)
    screen.fill((255, 255, 255))
    all_sprite.draw(screen)
    clock.tick(10)
    pygame.display.flip()
pygame.quit()
print()