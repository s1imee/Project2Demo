import pygame
import math

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
    image1 = pygame.image.load("data/tank_sand.png")
    original_image = pygame.transform.rotate(pygame.transform.scale(image1, (42, 46)), 90)
    image = pygame.transform.rotate(pygame.transform.scale(image1, (42, 46)), 90)

    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.original_image = Hero.original_image
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
    image = pygame.transform.scale(image1, (16, 24))

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
        self.speed = 10
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
