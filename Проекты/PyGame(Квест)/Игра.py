import pygame, sys, os

pygame.init()
size = WIDTH, HEIGHT = 800, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя: Камера')
FPS = 50


def load_img(name, colorkey=None):
    full_name = 'Data\\Sprites\\' + name
    if not os.path.isfile(full_name):
        print(f'Файл {full_name} не найден')
        sys.exit()
    img = pygame.image.load(full_name)
    if colorkey is not None:
        img = img.convert()
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey)
    else:
        img = img.convert_alpha()
    return img


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["МАРИО", "",
                  "Перемещение героя",
                  "с подгрузкой карты"]

    fon = pygame.transform.scale(load_img('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#000000'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "Data\\Levels\\" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_img('wall.png'),
    'empty': load_img('floor.png'),
    'stone': load_img('stone.png')
}
player_image = load_img('player.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    # клетка игрового поля: тип клетки и клеточные координаты
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        # Загрузить изображение в соответствии с типом
        self.image = tile_images[tile_type]
        # Поставить изображение на заданные координаты
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image  # Загрузить изображение персонажа
        # Поставить изображение на заданные координаты
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.count = 0

    def move(self, x, y):
        self.pos = (x, y)
        if level_map[y][x] == '*':
            Tile('empty', x, y)
            self.count += 1
            print(self.count)
            level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] != '#':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] != '#':
            hero.move(x, y + 1)
    if movement == 'left':
        if x > 0 and level_map[y][x - 1] != '#':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] != '#':
            hero.move(x + 1, y)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    # новый игрок и его координаты
    new_player, x, y = None, None, None
    for y in range(len(level)):  # перебор строк из файла с уровнем
        for x in range(len(level[y])):  # перебор символов в каждой строке
            if level[y][x] == '.':
                Tile('empty', x, y)  # пустая клетка
            elif level[y][x] == '#':
                Tile('wall', x, y)  # клетка со стеной
            elif level[y][x] == '*':
                Tile('stone', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)  # пустая клетка
                new_player = Player(x, y)  # создать персонажа по координатам х, у
                level[y] = level[y].replace('@', '.')
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


clock = pygame.time.Clock()
level_map = load_level('map1.txt')
player, max_x, max_y = generate_level(level_map)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                move(player, 'down')
            elif event.key == pygame.K_LEFT:
                move(player, 'left')
            elif event.key == pygame.K_RIGHT:
                move(player, 'right')
            elif event.key == pygame.K_UP:
                move(player, 'up')
    # изменяем ракурс камеры
    # обновляем положение всех спрайтов
    screen = pygame.display.set_mode((400, 400))
    screen.fill(pygame.Color('#000000'))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
