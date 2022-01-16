import pygame
import os
import sys

pygame.init()
size = width, height = 1300, 750
screen = pygame.display.set_mode(size)
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
    filename = "data/" + filename
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
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.flag = True

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.flag:
            self.rect.x -= tile_width
            self.flag = False
            if pygame.sprite.spritecollide(self, tiles_group, False):
                env = pygame.sprite.spritecollide(self, tiles_group, False)
                for tile in env:
                    if tile.type == 'wall':
                        self.rect.x += tile_width
        if keys[pygame.K_RIGHT] and self.flag:
            self.rect.x += tile_width
            self.flag = False
            if pygame.sprite.spritecollide(self, tiles_group, False):
                env = pygame.sprite.spritecollide(self, tiles_group, False)
                for tile in env:
                    if tile.type == 'wall':
                        self.rect.x -= tile_width
        if keys[pygame.K_UP] and self.flag:
            self.rect.y -= tile_height
            self.flag = False
            if pygame.sprite.spritecollide(self, tiles_group, False):
                env = pygame.sprite.spritecollide(self, tiles_group, False)
                for tile in env:
                    if tile.type == 'wall':
                        self.rect.y += tile_height
        if keys[pygame.K_DOWN] and self.flag:
            self.rect.y += tile_height
            self.flag = False
            if pygame.sprite.spritecollide(self, tiles_group, False):
                env = pygame.sprite.spritecollide(self, tiles_group, False)
                for tile in env:
                    if tile.type == 'wall':
                        self.rect.y -= tile_height
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
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

if __name__ == '__main__':
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')
    tile_width = tile_height = 50
    running = True
    player = None
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level('level.txt'))
    clock = pygame.time.Clock()
    start_screen()
    FPS = 60
    screen.fill(pygame.Color('white'))
    pygame.mouse.set_visible(False)
    camera = Camera()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_group.update()
            if event.type == pygame.KEYUP:
                player.flag = True
        all_sprites.update()
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


# new_x, new_y = target.real_xy()
#         self.dx = self.old_x - new_x
#         self.dy = self.old_y - new_y
#         self.old_x = new_x
#         self.old_y = new_y
#         if self.dx < 0:
#             self.dx -= 10
#         elif self.dx > 0:
#             self.dx += 10
#
#         print('разница', self.dx, self.dy)