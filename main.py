import os
import random

import pygame

SCREEN_WIDTH = 1920
BACKGROUND_COLOR = (255, 240, 220)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH // 2))
clock = pygame.time.Clock()

path = os.path.join(os.pardir, 'C:/Users/Piotrek/PycharmProjects/Monopoly/images')


def load_images(path):
    file_names = sorted(os.listdir(path))
    game_board_image = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
    file_names.remove('background.jpg')
    images = {}

    for file_name in file_names:
        image_name = file_name[:-4].upper()
        image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
        images[image_name] = image

    return game_board_image, images


game_board_image, IMAGES = load_images(path)

available_width, available_height = pygame.display.get_surface().get_size()
image_aspect_ratio = game_board_image.get_width() / game_board_image.get_height()


def calculate_game_board_dimensions():
    if image_aspect_ratio > 1:
        game_board_width = available_width
        game_board_height = int(game_board_width / image_aspect_ratio)
    else:
        game_board_height = available_height
        game_board_width = int(game_board_height * image_aspect_ratio)
    return game_board_width, game_board_height


game_board_width, game_board_height = calculate_game_board_dimensions()

game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
game_board_x = int((available_width - game_board_width) / 2)
game_board_y = int((available_height - game_board_height) / 2)

board_x = available_width // 4
board_y = int((available_height - game_board_height) / 2)
PAWN_SIZE = (game_board_width // 13, game_board_height // 13)


class Dice:

    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


class Pawn(pygame.sprite.Sprite):

    def __init__(self, image, px, py):
        super().init()
        self.image = pygame.transform.scale(image, PAWN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.movement_speed = 5

    def handle_events(self, keys_pressed):
        self.move(keys_pressed, pygame.K_LEFT, [-self.movement_speed, 0])
        self.move(keys_pressed, pygame.K_RIGHT, [self.movement_speed, 0])

    def move(self, keys_pressed, key, movement):
        if keys_pressed[key]:
            self.rect.move_ip(movement)

    def update(self, keys_pressed):
        self.handle_events(keys_pressed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player:

    def __init__(self, image, px, py):
        self.image = pygame.transform.scale(image, PAWN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.movement_speed = 5

    def move_left(self):
        self.rect.move_ip([-self.movement_speed, 0])

    def move_right(self):
        self.rect.move_ip([self.movement_speed, 0])

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.move_left()
        if keys_pressed[pygame.K_RIGHT]:
            self.move_right()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Menu:

    def __init__(self):
        self.menu_rects = []
        self.num_players = 0

    def handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(mouse_pos):
                        self.num_players = i + 2
                        return

    def draw_menu(self):
        screen.fill(BACKGROUND_COLOR)
        button_color = (0, 255, 0)  # Zielony kolor przycisków
        text_color = (0, 0, 0)  # Kolor tekstu

        # Wyświetlanie tekstu "Wybierz ilość graczy"
        font = pygame.font.Font(None, 36)
        text = font.render("Wybierz ilość graczy", True, text_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 4 - 100))
        screen.blit(text, text_rect)

        self.menu_rects = []
        menu_options = [2, 3, 4]
        for i, option in enumerate(menu_options):
            rect = pygame.Rect((available_width // 2) + ((i * 120) - 180), (available_height // 2), 100, 40)
            pygame.draw.rect(screen, button_color, rect)
            button_text = font.render(str(option), True, text_color)
            button_text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, button_text_rect)
            self.menu_rects.append(rect)

        pygame.display.flip()

    def execute_menu_action(self):
        if self.num_players > 0:
            print("Rozpoczynam grę dla", self.num_players, "graczy.")
            # Tutaj dodać kod, który wykona akcję na podstawie liczby graczy, na przykład rozpocznie grę dla odpowiedniej liczby graczy.

    def start(self):
        while self.num_players == 0:
            self.handle_menu()
            self.draw_menu()

        # przekazanie wartości num_players do obiektu Board
        board = Board(self.num_players)
        board.start()


class Board:

    def __init__(self, num_players):
        self.current_player_index = 0
        self.players = []
        self.player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
        self.num_players = num_players
        self.window_open = True
        self.menu = Menu()
        self.game_board_width = int((available_width * 2) // 3)
        self.game_board_height = int(self.game_board_width / image_aspect_ratio)

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        dice = Dice()
        return dice.roll()

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[i % len(self.player_images)]
            player = Player(player_image, int(game_board_width * 1.4) - i * 10, int(game_board_height * 0.9))
            if i % 2 == 1:
                player.rect.move_ip([0, game_board_height // 20])  # Przesuń gracza w dół
            self.players.append(player)

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(game_board, (board_x, board_y))
        for player in self.players:
            player.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render("Oczka", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 8, SCREEN_WIDTH // 4 - 100))
        screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window_open = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice_roll = self.roll_dice()
                    current_player = self.players[self.current_player_index]
                    print("Gracz", self.current_player_index + 1, "wyrzucił", dice_roll, "oczka.")
                    self.switch_to_next_player()

                    # Tutaj możesz wykorzystać wartość dice_roll do zaimplementowania logiki gry

        for player in self.players:
            player.update(keys_pressed)

    def start(self):
        self.initialize_players()

        while self.window_open:
            self.handle_events()
            self.draw_game_board()
            clock.tick(60)


menu = Menu()
menu.start()
