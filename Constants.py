import pygame

from logic.GameRatio import calculate_game_board_dimensions, available_width, available_height
from resources.LoadImages import get_dice_images, chance_card_image, chest_card_image, get_house_image

BACKGROUND_COLOR = (255, 240, 220)
DICE_IMAGES = get_dice_images()
CHANCE_CARD_IMAGE, CHANCE_CARD_IMAGE_2 = chance_card_image()
CHEST_CARD_IMAGE, CHEST_CARD_IMAGE_2 = chest_card_image()
HOUSE_IMAGE = get_house_image()
GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT = calculate_game_board_dimensions()
BOARD_X = available_width // 4
BOARD_Y = int((available_height - GAME_BOARD_HEIGHT) / 2)
PAWN_SIZE = (GAME_BOARD_WIDTH // 13, GAME_BOARD_HEIGHT // 13)
FONT_SIZE = available_height // 30
BUY_BUTTON_RECT = pygame.Rect(available_width * 0.07, available_height * 0.85,
                              available_width * 0.1, available_height * 0.05)
