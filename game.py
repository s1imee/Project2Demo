import pygame
import math
from random import choice

pygame.init()
tile_width = tile_height = 56
width, height = 896, 896


class Boss(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/tank_huge.png")
    image = pygame.transform.scale(image1, (62, 76))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Boss.image
        self.rect = self.image.get_rect()
        self.rect.x = 800 + self.rect[2]
        self.rect.y = 175

    def update(self):
        self.rect.x -= 0.5


class BossBullet(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/bulletRed2.png")
    image = pygame.transform.scale(image1, (16, 24))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BossBullet.image
        self.rect = self.image.get_rect()
        self.rect.x = Boss().rect.x
        self.rect.y = Boss().rect.y

    def update(self):
        self.rect.x -= 10
        if self.rect.x == 6:
            self.rect.x = Boss().rect.x

        elif self.rect.x < 6:
            self.rect.x = Boss().rect.x


class Bunker(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/crateMetal.png")
    image = pygame.transform.scale(image1, (56, 56))

    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = Bunker.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/1111.png")
    original_image = pygame.transform.rotate(pygame.transform.scale(image1, (42, 46)), 90)
    image = pygame.transform.rotate(pygame.transform.scale(image1, (42, 46)), 90)

    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.original_image = Hero.original_image
        self.original_image = pygame.transform.rotate(self.original_image, 180)
        self.key_is_up = True
        self.rect = self.original_image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.position = [tile_width * pos_x, tile_height * pos_y]
        self.last_move_x = 0
        self.last_move_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.position[0] -= 5
            self.last_move_x = -5
        if keys[pygame.K_d]:
            self.rect.x += 5
            self.position[0] += 5
            self.last_move_x = 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
            self.position[1] -= 5
            self.last_move_y = -5
        if keys[pygame.K_s]:
            self.rect.y += 5
            self.position[1] += 5
            self.last_move_y = 5
        self.rotate()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle + 4))
        # self.rect = self.image.get_rect(center=self.position)

    def collide(self, collidable_object):
        hits = pygame.sprite.spritecollide(self, collidable_object, False)
        if len(hits) != 0:
            for block in hits:
                if block.rect.x + (block.rect.width - 10) < self.rect.x:  # left
                    self.rect.x += 5
                    # self.rect.x = self.rect.x - self.last_move_x
                if block.rect.x > self.rect.x + (self.rect.width - 18):  # right
                    self.rect.x -= 5
                    # self.rect.y = self.rect.y - self.last_move_y
                if block.rect.y > self.rect.y + (self.rect.height - 32):  # up
                    self.rect.y -= 5
                if block.rect.y + (block.rect.height - 40) < self.rect.y:  # down
                    self.rect.y += 5

        self.last_move_x = self.last_move_y = 0


class Bullet(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/bulletRed2.png")
    image = pygame.transform.scale(image1, (10, 14))

    def __init__(self, pos_x, pos_y, player, *group):
        super().__init__(*group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 15
        self.rect.y = player.rect.y + 15

        # x, y = pygame.mouse.get_pos()# нажатие мыши
        dx, dy = pos_x - self.rect.x, pos_y - self.rect.y
        len = math.hypot(dx, dy)
        self.dx = dx / len
        self.dy = dy / len
        self.speed = 20
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        x, y = target.rect.center
        self.dx = -(x + target.rect.w / 2 - width / 2)
        self.dy = -(y + target.rect.h / 2 - height / 2)


class Enemy(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/creature.png")
    image = pygame.transform.scale(image1, (72, 84))
    image_damage = pygame.image.load("data/creature_damge.png")

    def __init__(self, x, y, collidable_object, *group):
        super().__init__(*group)

        self.collidable_object = []
        for i in collidable_object:
            if type(i) == Bunker:
                self.bunker = i
                self.collidable_object.append(i)
            if type(i) == Tile:
                if i.type == 'wall':
                    self.collidable_object.append(i)

        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hp = 100
        self.speed = 1
        self.up_or_down = choice(['up', 'down'])
        self.lef_or_rig = choice(['left', 'rig'])
        self.last_move_x = 0
        self.last_move_y = 0
        len_for_bunker_x = self.bunker.rect.x - self.rect.x
        len_for_bunker_y = self.bunker.rect.y - self.rect.y

        if abs(len_for_bunker_x) > abs(len_for_bunker_y):
            if len_for_bunker_x > 0:
                self.bypass_speed_x = 2
            else:
                self.bypass_speed_x = -2
            self.bypass_speed_y = choice([2, -2])
        else:
            if len_for_bunker_y > 0:
                self.bypass_speed_y = 2
            else:
                self.bypass_speed_y = -2
            self.bypass_speed_x = choice([2, -2])


    def update(self):
        x = self.bunker.rect.x
        y = self.bunker.rect.y
        self.last_move_x = 0
        self.last_move_y = 0

        if self.rect.x > x:
            self.rect.x -= self.speed
            self.last_move_x = -self.speed
        elif self.rect.x < x:
            self.rect.x += self.speed
            self.last_move_x = self.speed

        check_collide = self.collide(self.collidable_object, 'x')
        if check_collide[0]:
            self.rect.x -= self.last_move_x
            if check_collide[1]:  # подошли к бункеру или нет
                self.attack_the_bunker()
            else:
                self.rect.y += self.bypass_speed_x

        if self.rect.y > y:
            self.rect.y -= self.speed
            self.last_move_y = -self.speed
        elif self.rect.y < y:
            self.rect.y += self.speed
            self.last_move_y = self.speed

        check_collide = self.collide(self.collidable_object, 'y')
        if check_collide[0]:
            self.rect.y -= self.last_move_y
            if check_collide[1]:  # подошли к бункеру или нет
                self.attack_the_bunker()
            else:
                self.rect.x += self.bypass_speed_x


    def took_damage(self, damage):
        self.hp -= damage

    def collide(self, collidable_object, x_or_y):
        hits = pygame.sprite.spritecollide(self, collidable_object, False)
        collide_x = False
        collide_y = False
        attack = False
        if len(hits) != 0:
            if x_or_y == 'x':
                for block in hits:
                    if block.rect.x + (block.rect.width - 10) < self.rect.x:  # left
                        collide_x = True
                    if block.rect.x > self.rect.x + (self.rect.width - 10):  # right
                        collide_x = True
                    if type(block) == Bunker:
                        attack = True
                if attack:
                    self.attack_the_bunker()
                return [collide_x, attack]
            else:
                for block in hits:
                    if block.rect.y > self.rect.y + (self.rect.height - 10):  # up
                        collide_y = True
                    if block.rect.y + (block.rect.height - 10) < self.rect.y:  # down
                        collide_y = True
                    if type(block) == Bunker:
                        attack = True
                if attack:
                    self.attack_the_bunker()
                return [collide_y, attack]

        return [False, attack]

    def attack_the_bunker(self):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_images, *group):
        super().__init__(*group)
        self.type = tile_type
        image1 = pygame.transform.scale(tile_images[tile_type], (56, 56))
        self.image = image1
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
