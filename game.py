import pygame
import os
import sys
from classes import Hero, Boss, BossBullet, Bunker, Camera, Bullet

size = width, height = 896, 896
tile_width = tile_height = 56
screen = pygame.display.set_mode(size)
scene = False  # для вызова боса назначить True
lives = 25  # жизни базы
collidable_object = [] # изменятся в generate_level и при создании врагов и пуль


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = 'data/' + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                collidable_object.append(Tile('wall', x, y))
                bunk.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Hero(x, y, player_group, all_sprites)
            elif level[y][x] == 'b':
                collidable_object.append(Bunker(x, y, all_sprites))
            elif level[y][x] == 's':
                collidable_object.append(Tile('sand', x, y))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        image1 = pygame.transform.scale(tile_images[tile_type], (56, 56))
        self.image = image1
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


if __name__ == '__main__':
    running = True
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bunk = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('crateWood.png'),
        'empty': load_image('tileGrass1.png'),
        'sand': load_image('tileSand1.png')
    }
    screen.fill(pygame.Color('white'))
    FPS = 60
    clock = pygame.time.Clock()
    player, level_x, level_y = generate_level(load_level('lvl1.txt'))
    camera = Camera()
    if scene:  # проверка начата ли сцена с босом
        Boss(all_sprites)
        BossBullet(all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                new = Bullet(*event.pos, player, all_sprites)
                bullets.add(new)

        screen.fill(pygame.Color('white'))
        hits = pygame.sprite.groupcollide(bunk, bullets, False, True)
        # for sprite in all_sprites:
        #     hasCollide = False
        #
        #     for collide in collidable_object:
        #         hasCollide = collide.rect.colliderect(player)
        #         pygame.sprite.spritecollide()
        #         if hasCollide:
        #             print(collide, hasCollide)
        #             break
        #
        #     if hasCollide:
        #
        #         player.rect.x -= 5
        #         break
        #
        #     camera.apply(sprite)
        #     sprite.update()

        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)

        player.collide(collidable_object)

        all_sprites.update()
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        player_group.draw(screen)

        clock.tick(FPS)

        pygame.display.flip()



    pygame.quit()
