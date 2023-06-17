import os

import pygame

import GameRatio

path = 'images'


def load_images():
    images = {}
    file_names = sorted(os.listdir(path))
    file_names.remove('background.jpg')

    for file_name in file_names:
        image_name = file_name[:-4].upper()
        image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
        images[image_name] = image

    game_board_image = pygame.image.load(os.path.join(path, 'background.jpg')).convert()

    return game_board_image, images


def get_dice_images():
    dice_images = [pygame.image.load(os.path.join(path, f'{i}.png')).convert_alpha() for i in range(1, 20)]
    scaled_images = [pygame.transform.scale(image, (GameRatio.get_width() // 2, GameRatio.get_height() // 2)) for image
                     in
                     dice_images]
    dice_images = scaled_images
    return dice_images


def chance_card_image():
    card_image = pygame.image.load(os.path.join(path, 'chance_card.png')).convert_alpha()
    card_image_2 = pygame.image.load(os.path.join(path, 'chance_card_2.png')).convert_alpha()
    return card_image, card_image_2


def chest_card_image():
    card_image = pygame.image.load(os.path.join(path, 'community_card.png')).convert_alpha()
    card_image_2 = pygame.image.load(os.path.join(path, 'community_card_2.png')).convert_alpha()
    return card_image, card_image_2
