import pygame

from LoadImages import load_images
SCREEN_WIDTH = 1920
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH // 2))
available_width, available_height = pygame.display.get_surface().get_size()
game_board_image, IMAGES = load_images()
image_aspect_ratio = game_board_image.get_width() / game_board_image.get_height()

def get_width():
    return available_width


def get_height():
    return available_height

def calculate_game_board_dimensions():
    if image_aspect_ratio > 1:
        game_board_width = available_width
        game_board_height = int(game_board_width / image_aspect_ratio)
    else:
        game_board_height = available_height
        game_board_width = int(game_board_height * image_aspect_ratio)
    return game_board_width, game_board_height

