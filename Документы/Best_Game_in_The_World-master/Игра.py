import pygame, sys, os

pygame.init()
levels = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt']
size = WIDTH, HEIGHT = 1400, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Escape From Spaceship')
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


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


def load_level(filename):
    filename = "Data\\Levels\\" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["Escape From Spaceship", "",
                  "Управление курсорными клавиша"]

    fon = pygame.transform.scale(load_img('startscreen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#df0000'))
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


def end_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    intro_text = ["Поздравляем!", "Вы прошли игру!",
                  "Последний портал отправил вас на корабль, который находился рядом с главным.",
                  "Этот корабль, по неизвесным причинам, был пустой. Видимо, это был беспилотник.",
                  "Вы смогли отправить ваш новый корабль на другой маршрут, хоть и понадобилось на это много времени.",
                  "Пока вы можете отдохнуть... Надолго ли?"]

    fon = pygame.transform.scale(load_img('endscreen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#df0000'))
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
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

tile_images = {
    'wall': load_img('wall.jpg'),
    'empty': load_img('empty.jpg'),
    'portal': load_img('portal.jpg'),
    'keyR': load_img('keyR.jpg'),
    'doorR': load_img('doorR.jpg'),
    'keyW': load_img('keyW.jpg'),
    'doorW': load_img('doorW.jpg'),
    'keyB': load_img('keyB.jpg'),
    'doorB': load_img('doorB.jpg'),
    'keyG': load_img('keyG.jpg'),
    'doorG': load_img('doorG.jpg'),
    'fire': load_img('fire.jpg'),
    'space': load_img('space.jpg')
}
player_image = load_img('human.png')

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
            tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        global NUM_OF_LVL, player, level_map
        level = load_level(levels[NUM_OF_LVL])
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * x + 5, tile_height * y + 5)
        if level_map[y][x] == '@':
            NUM_OF_LVL += 1
            if NUM_OF_LVL == 4:
                end_screen()
            self.rect = self.image.get_rect().move(1000, 1000)
            tiles_group.empty()
            player_group.empty()
            level_map = load_level(levels[NUM_OF_LVL])
            player, max_x, max_y = generate_level(load_level(levels[NUM_OF_LVL]))
        elif level_map[y][x] == 'W':
            Tile('empty', x, y)
            level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level_map[y][x] == 'w':
                        Tile('empty', x, y)
                        level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
        elif level_map[y][x] == 'B':
            Tile('empty', x, y)
            level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level_map[y][x] == 'b':
                        Tile('empty', x, y)
                        level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
        elif level_map[y][x] == 'G':
            Tile('empty', x, y)
            level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level_map[y][x] == 'g':
                        Tile('empty', x, y)
                        level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
        elif level_map[y][x] == 'R':
            Tile('empty', x, y)
            level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level_map[y][x] == 'r':
                        Tile('empty', x, y)
                        level_map[y] = level_map[y][:x] + '.' + level_map[y][x + 1:]
        elif level_map[y][x] == '*':
            self.rect = self.image.get_rect().move(1000, 1000)
            tiles_group.empty()
            player_group.empty()
            level_map = load_level(levels[NUM_OF_LVL])
            player, max_x, max_y = generate_level(load_level(levels[NUM_OF_LVL]))


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        next_tile = level_map[y - 1][x]
        if next_tile == '#' or next_tile == 'w':
            next_tile = '#'
        if y > 0 and next_tile != '#':
            hero.move(x, y - 1)
    elif movement == 'down':
        next_tile = level_map[y + 1][x]
        if next_tile == '#' or next_tile == 'w':
            next_tile = '#'
        if y < max_y - 1 and next_tile != '#':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] != '#':
            hero.move(x - 1, y)
    elif movement == 'right':
        next_tile = level_map[y][x + 1]
        if next_tile == '#' or next_tile == 'b' or next_tile == 'g' or next_tile == 'r':
            next_tile = '#'
        if x < max_x - 1 and next_tile != '#':
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
            # Создаем пустую клетку
            if level[y][x] == '.':
                Tile('empty', x, y)
            # Создаем непроходимую клетку-стену
            elif level[y][x] == '#':
                Tile('wall', x, y)
            # Создаем портал - выход и переход на новый уровень
            elif level[y][x] == '@':
                Tile('portal', x, y)
            # Создаем персонажа на пустой клетке
            elif level[y][x] == 'S':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y] = level[y].replace('S', '.')
            # Создаем красную дверь
            elif level[y][x] == 'r':
                Tile('doorR', x, y)
            # Создаем белую дверь
            elif level[y][x] == 'w':
                Tile('doorW', x, y)
            # Создаем синюю дверь
            elif level[y][x] == 'b':
                Tile('doorB', x, y)
            # Создаем зеленую дверь
            elif level[y][x] == 'g':
                Tile('doorG', x, y)
            # Создаем красный ключ
            elif level[y][x] == 'R':
                Tile('keyR', x, y)
            # Создаем белый ключ
            elif level[y][x] == 'W':
                Tile('keyW', x, y)
            # Создаем синий ключ
            elif level[y][x] == 'B':
                Tile('keyB', x, y)
            # Создаем зеленый ключ
            elif level[y][x] == 'G':
                Tile('keyG', x, y)
            # Создаем клетку-убийцу - огнеметы
            elif level[y][x] == '*':
                Tile('fire', x, y)
            # Создаем клетку за стенами - космос
            elif level[y][x] == '^':
                Tile('space', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


clock = pygame.time.Clock()
NUM_OF_LVL = 0
level_map = load_level(levels[NUM_OF_LVL])
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
    screen = pygame.display.set_mode((400, 400))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
