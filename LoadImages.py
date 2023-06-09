import os

import pygame

from GameRatio import available_width, available_height


def load_images(path):
    images = {}
    file_names = sorted(os.listdir(path))
    file_names.remove('background.jpg')

    for file_name in file_names:
        image_name = file_name[:-4].upper()
        image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
        images[image_name] = image

    game_board_image = pygame.image.load(os.path.join(path, 'background.jpg')).convert()

    return game_board_image, images


def get_dice_images(path):
    dice_images = [pygame.image.load(os.path.join(path, f'{i}.png')).convert_alpha() for i in range(1, 20)]
    scaled_images = [pygame.transform.scale(image, (available_width // 2, available_height // 2)) for image in
                     dice_images]
    dice_images = scaled_images
    return dice_images
