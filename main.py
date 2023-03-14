import pygame
import random
import copy
from PIL import Image
from classes import Board, load_image, Square, make_tiles, \
    all_sprites, pitch, win_screen, startflag, start_screen, terminate, gameplay

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Пятнашки')
    image = Image.open('data\\pitch.png')
    size = width, height = image.size
    screen = pygame.display.set_mode((width, height + 50))
    clock = pygame.time.Clock()

    board = Board(4, 4)
    board.set_view(0, 0, width / 4)

    quarter = width // 4

    start_screen(screen, width, height + 50)

    gameplay(screen, quarter, width, height, board, clock)
