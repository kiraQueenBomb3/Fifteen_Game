import pygame
import sys
import os
import random
import copy
from PIL import Image

all_sprites = pygame.sprite.Group()
pitch = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
startflag = False
step_ability = False


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def win_screen(screen, steps, width, height):
    string_steps = str(steps)
    if len(string_steps) > 2 and string_steps[-2] == '1':
        word = 'ходов'
    elif string_steps[-1] == '1':
        word = 'ход'
    elif string_steps[-1] in '234':
        word = 'хода'
    else:
        word = 'ходов'

    outro_text = ["Поздравляю!",
                  "Вы закончили эту партию.",
                  f"Вы потратили {steps} {word}.",
                  "Слишком сильная мозговая",
                  'активность не полезна. ',
                  'Предлагаю заняться',
                  'чем-то другим.']
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in outro_text:
        congratulates = font.render(line, 1, pygame.Color('white'), (0, 0, 0))
        rect_for_steps = congratulates.get_rect()
        rect_for_steps.x = 10
        rect_for_steps.top = text_coord
        place = congratulates.get_rect(center=(width//2, text_coord))
        text_coord += 40
        screen.blit(congratulates, place)
        pygame.draw.rect(screen, (0, 0, 0), (0, width + 1, width, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()


class Board:  # White lines
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (
                        self.left + col * self.cell_size,
                        self.top + row * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    ),
                    1
                )


class Square(pygame.sprite.Sprite):
    def __init__(self, group, normal_image, x, y, queue_number):
        super().__init__(group)
        self.image = normal_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.queue_number = queue_number

    def update(self, pos, quarter):
        global startflag
        startflag = False  # For a randomizer
        if self.rect.collidepoint(pos):  # Any tile clicked
            startflag = True
            # Searching tile
            for i in range(len(pitch)):
                if self.queue_number in pitch[i]:
                    index = pitch[i].index(self.queue_number)
                    # Searching hole
                    if 0 in pitch[i]:  # Horizontal hole
                        if index < pitch[i].index(0):  # Hole is on the right
                            # Counting tiles
                            if pitch[i].index(0) - index == 1:
                                try:
                                    pitch[i][index], pitch[i][index + 1] = pitch[i][index + 1], pitch[i][index]
                                    self.rect = self.rect.move(quarter, 0)
                                    return None
                                except Exception:
                                    print(1)
                            elif pitch[i].index(0) - index == 2:
                                try:
                                    for element in all_sprites:
                                        if element.rect.y == self.rect.y:
                                            if element.rect.x > self.rect.x and element.rect.x + quarter < quarter * 4:
                                                element.rect = element.rect.move(quarter, 0)
                                    pitch[i][index], pitch[i][index + 1], pitch[i][index + 2] = pitch[i][index + 2], \
                                                                                                pitch[i][index], \
                                                                                                pitch[i][index + 1]
                                    self.rect = self.rect.move(quarter, 0)
                                    return None
                                except Exception:
                                    print(2)
                            elif pitch[i].index(0) - index == 3:
                                try:
                                    for element in all_sprites:
                                        if element.rect.y == self.rect.y:
                                            if element.rect.x > self.rect.x and element.rect.x + quarter < quarter * 4:
                                                element.rect = element.rect.move(quarter, 0)
                                    pitch[i][index], pitch[i][index + 1], pitch[i][index + 2], pitch[i][index + 3] = \
                                        pitch[i][index + 3], pitch[i][index], pitch[i][index + 1], pitch[i][index + 2]
                                    self.rect = self.rect.move(quarter, 0)
                                    return None
                                except Exception:
                                    print(3)
                        else:  # Hole is on the left
                            # Counting tiles
                            if index - pitch[i].index(0) == 1:
                                try:
                                    pitch[i][index], pitch[i][index - 1] = pitch[i][index - 1], pitch[i][index]
                                    self.rect = self.rect.move(-quarter, 0)
                                except Exception:
                                    print(4)
                            elif index - pitch[i].index(0) == 2:
                                try:
                                    for element in all_sprites:
                                        if element.rect.y == self.rect.y:
                                            if element.rect.x < self.rect.x and element.rect.x - quarter >= 0:
                                                element.rect = element.rect.move(-quarter, 0)
                                    pitch[i][index - 2], pitch[i][index - 1], pitch[i][index] = pitch[i][index - 1], \
                                                                                                pitch[i][index], \
                                                                                                pitch[i][index - 2]
                                    self.rect = self.rect.move(-quarter, 0)
                                except Exception:
                                    print(5)
                            elif index - pitch[i].index(0) == 3:
                                try:
                                    for element in all_sprites:
                                        if element.rect.y == self.rect.y:
                                            if element.rect.x < self.rect.x and element.rect.x - quarter >= 0:
                                                element.rect = element.rect.move(-quarter, 0)
                                    pitch[i][index - 3], pitch[i][index - 2], pitch[i][index - 1], pitch[i][index] = \
                                        pitch[i][index - 2], pitch[i][index - 1], pitch[i][index], pitch[i][index - 3]
                                    self.rect = self.rect.move(-quarter, 0)
                                except Exception:
                                    print(6)
                    else:  # Vertical hole
                        # Searching hole
                        for j in range(len(pitch)):
                            if 0 in pitch[j]:
                                zero_index = pitch[j].index(0)
                                if index == zero_index:
                                    if i < j:  # Hole is lower
                                        # Counting tiles
                                        if j - i == 1:
                                            try:
                                                pitch[i][index], pitch[j][zero_index] = pitch[j][zero_index], pitch[i][
                                                    index]
                                                self.rect = self.rect.move(0, quarter)
                                            except Exception:
                                                print(7)
                                            return None
                                        elif j - i == 2:
                                            try:
                                                for element in all_sprites:
                                                    if element.rect.x == self.rect.x:
                                                        if element.rect.y > self.rect.y and element.rect.y + quarter < \
                                                                quarter * 4:
                                                            element.rect = element.rect.move(0, quarter)
                                                pitch[i][index], pitch[i + 1][index], pitch[j][zero_index] = \
                                                    pitch[j][zero_index], pitch[i][index], pitch[i + 1][index]
                                                self.rect = self.rect.move(0, quarter)
                                            except Exception:
                                                print(8)
                                            return None
                                        elif j - i == 3:
                                            try:
                                                for element in all_sprites:
                                                    if element.rect.x == self.rect.x:
                                                        if element.rect.y > self.rect.y and element.rect.y + quarter < \
                                                                quarter * 4:
                                                            element.rect = element.rect.move(0, quarter)
                                                pitch[i][index], pitch[i + 1][index], pitch[i + 2][index], pitch[j][
                                                    zero_index] = pitch[j][zero_index], pitch[i][index], pitch[i + 1][
                                                    index], pitch[i + 2][index]
                                                self.rect = self.rect.move(0, quarter)
                                            except Exception:
                                                print(9)
                                            return None
                                    if j < i:  # Hole is upper
                                        # Counting tiles
                                        if i - j == 1:
                                            try:
                                                pitch[i][index], pitch[j][zero_index] = pitch[j][zero_index], pitch[i][
                                                    index]
                                                self.rect = self.rect.move(0, -quarter)
                                            except Exception:
                                                print(10)
                                            return None
                                        elif i - j == 2:
                                            try:
                                                for element in all_sprites:
                                                    if element.rect.x == self.rect.x:
                                                        if element.rect.y < self.rect.y and \
                                                                element.rect.y - quarter >= 0:
                                                            element.rect = element.rect.move(0, -quarter)
                                                pitch[i][index], pitch[i - 1][index], pitch[j][zero_index] = \
                                                    pitch[j][zero_index], pitch[i][index], pitch[i - 1][index]
                                                self.rect = self.rect.move(0, -quarter)
                                            except Exception:
                                                print(11)
                                            return None
                                        elif i - j == 3:
                                            try:
                                                for element in all_sprites:
                                                    if element.rect.x == self.rect.x:
                                                        if element.rect.y < self.rect.y and \
                                                                element.rect.y - quarter >= 0:
                                                            element.rect = element.rect.move(0, -quarter)
                                                pitch[i][index], pitch[i - 1][index], pitch[i - 2][index], pitch[j][
                                                    zero_index] = pitch[j][zero_index], pitch[i][index], pitch[i - 1][
                                                    index], pitch[i - 2][index]
                                                self.rect = self.rect.move(0, -quarter)
                                            except Exception:
                                                print(12)
                                            return None
        '''else:
            startflag = False'''


def start_screen(screen, width, height):
    global step_ability
    step_ability = True
    screen.fill((0, 0, 0))
    intro_text = ['                Пятнашки', "",
                  '      Нажмите любую кнопку,',
                  '              чтобы начать']
    background = load_image('background.png')
    fon = pygame.transform.scale(background, (width, height))
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


def make_tiles(quarter):
    # Making a list of images (tiles)
    k_y = 0
    data_lst = []
    for now_y in range(4):
        k_x = 0
        im = Image.open('data\\pitch.png')
        for now_x in range(4):
            now_image = im.crop((k_x * quarter, k_y * quarter,
                                 (k_x + 1) * quarter, (k_y + 1) * quarter))
            data_lst.append(now_image)
            k_x += 1
        k_y += 1
    data_lst.pop(-1)
    ky = 0
    k1 = 0
    k2 = 0
    number = 1

    # Making a pitch
    for i in range(len(data_lst)):
        mode = data_lst[i].mode
        size = data_lst[i].size
        data = data_lst[i].tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        Square(all_sprites, py_image, ky * quarter, k1 * quarter, number)
        k2 += 1
        ky += 1
        if k2 - k1 == 4:
            k2 = k1 + 1
            k1 = k2
            ky = 0
        number += 1


def gameplay(screen, quarter, width, height, board, clock):
    global step_ability
    make_tiles(quarter)

    # Creating a situation
    for i in range(5000):
        all_sprites.update((random.randrange(width), random.randrange(width)), quarter)
    steps = 0

    fps = 50
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if step_ability:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        copied_pitch = copy.deepcopy(pitch)
                        pos = event.pos
                        all_sprites.update(pos, quarter)
                        if copied_pitch[:] != pitch[:]:
                            steps += 1
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        counting_steps = font.render(f'Ходов сделано: {steps}', 1, pygame.Color('white'))
        rect_for_steps = counting_steps.get_rect()
        rect_for_steps.x = 10
        rect_for_steps.top = width + 10
        screen.blit(counting_steps, rect_for_steps)
        all_sprites.draw(screen)
        board.render(screen)
        if pitch == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]:
            step_ability = False
            win_screen(screen, steps, width, height + 50)
        clock.tick(fps)
        pygame.display.flip()