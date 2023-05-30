import os
import random

import pygame
from pygame import draw

from MenuScreen import MenuScreen

SCREEN_WIDTH = 1920
BACKGROUND_COLOR = (255, 240, 220)
BUY_BUTTON_WIDTH = 100
BUY_BUTTON_HEIGHT = 40
BUY_BUTTON_COLOR = (0, 255, 0)
BUY_BUTTON_TEXT_COLOR = (255, 255, 255)
buy_button_rect = pygame.Rect(100, 100, BUY_BUTTON_WIDTH, BUY_BUTTON_HEIGHT)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH // 2))
clock = pygame.time.Clock()

path = os.path.join(os.pardir, 'C:/Users/Piotrek/PycharmProjects/Monopoly/images')
menuscreen = MenuScreen()


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
FONT_SIZE = available_height // 30;


def sprawdz_typ_pola(indeks_pola):
    return Fields[indeks_pola].type


class Field:
    def __init__(self, name, position_x, position_y, type):
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.type = type

    def get_name(self):
        return self.name

    def get_coordinates(self):
        return self.position_x, self.position_y

    def get_type(self):
        return self.type


class Estate(Field):
    def __init__(self, name, position_x, position_y, type, price, rent):
        super().__init__(name, position_x, position_y, type)
        self.price = price
        self.rent = rent
        self.owner = None

    def get_price(self):
        return self.price

    def get_rent(self):
        return self.rent

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner


Fields = [
    Field("Start", board_x + (game_board_width * 0.9), board_y + game_board_height - PAWN_SIZE[1], "start"),
    Estate("Frankfurt", board_x + (game_board_width * 0.8), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    Field("Skrzynia", board_x + (game_board_width * 0.75), board_y + game_board_height - PAWN_SIZE[1], "skrzynia"),
    Estate("Berlin", board_x + (game_board_width * 0.65), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    Field("Podatek", board_x + (game_board_width * 0.6), board_y + game_board_height - PAWN_SIZE[1], "podatek"),
    Field("Kolejka", board_x + (game_board_width * 0.5), board_y + game_board_height - PAWN_SIZE[1], "kolejka"),
    Estate("Warszawa", board_x + (game_board_width * 0.4), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    Field("Szansa", board_x + (game_board_width * 0.35), board_y + game_board_height - PAWN_SIZE[1], "szansa"),
    Estate("Praga", board_x + (game_board_width * 0.25), board_y + game_board_height - PAWN_SIZE[1], "estate", 600, 10),
    Estate("Wiedeń", board_x + (game_board_width * 0.17), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    Field("Wiezienie", board_x + (game_board_width * 0.05), board_y + game_board_height - PAWN_SIZE[1], "wiezienie"),
]


class Dice:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, name, px, py):
        super().__init__()
        self.image = pygame.transform.scale(image, PAWN_SIZE)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.current_point = 0
        self.money = 1500
        self.properties = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_current_point(self):
        return self.current_point

    def set_current_point(self, new_point):
        self.current_point = new_point

    def add_money(self, money):
        self.money += money

    def subtract_money(self, money):
        self.money -= money

    def get_money(self):
        return self.money

    def add_property(self, field):
        self.properties.append(field)

    def pay_rent(self, rent):
        self.money -= rent


class Board:
    def __init__(self, num_players, player_names):
        self.current_player_index = 0
        self.players = []
        self.player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
        self.num_players = num_players
        self.window_open = True
        self.menu = menuscreen
        self.game_board_width, self.game_board_height = calculate_game_board_dimensions()
        self.game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
        self.dice_roll = 0
        self.player_names = player_names
        self.waiting_for_input = False

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        dice = Dice()
        self.dice_roll = dice.roll()

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[i % len(self.player_images)]
            player = Player(player_image, self.player_names[i], int(game_board_width * 1.45) - i * 10,
                            int(game_board_height * 0.9))
            if i % 2 == 1:
                player.rect.move_ip([0, game_board_height // 20])
            self.players.append(player)

    def move_player(self, player):
        if self.dice_roll > 0:
            player.current_point = (player.current_point + 1) % len(Fields)  # Aktualizacja pozycji gracza

            # Przesunięcie pionka o jedno pole za start
            target_x, target_y = Fields[player.current_point].get_coordinates()
            dx = target_x - player.rect.centerx
            dy = target_y - player.rect.centery
            step_x = dx / 12
            step_y = dy / 12

            for _ in range(12):
                player.rect.move_ip([step_x, step_y])
                pygame.time.wait(20)
                self.draw_game_board()
                clock.tick(60)

            player.rect.center = target_x, target_y

            # Przesunięcie pionka po pozostałych polach
            for _ in range(1, self.dice_roll):
                player.current_point = (player.current_point + 1) % len(Fields)
                target_x, target_y = Fields[player.current_point].get_coordinates()
                dx = target_x - player.rect.centerx
                dy = target_y - player.rect.centery
                step_x = dx / 12
                step_y = dy / 12

                for _ in range(12):
                    player.rect.move_ip([step_x, step_y])
                    pygame.time.wait(20)
                    self.draw_game_board()
                    clock.tick(60)

                player.rect.center = target_x, target_y

            # Sprawdzenie typu pola i wykonanie odpowiednich akcji
            typ_pola = sprawdz_typ_pola(player.current_point)
            if typ_pola == "estate":

                current_field = Fields[player.current_point]
                owner = current_field.get_owner()
                if owner and owner != player:
                    rent = current_field.get_rent()
                    player.pay_rent(rent)
                    owner.add_money(rent)

            elif typ_pola == "szansa":
                # Kod dla pola Szansy
                print("Wykonaj akcję związaną z polem Szansy.")

            elif typ_pola == "więzienie":
                # Kod dla pola Więzienie
                print("Jesteś w więzieniu. Wykonaj odpowiednie działania.")
            elif typ_pola == "podatek":
                # Kod dla pola Podatek
                print("Płacisz Podatek. Wykonaj odpowiednie działania.")
            elif typ_pola == "skrzynia":
                # Kod dla pola Skrzynia
                print("Otwierasz skrzynię. Wykonaj odpowiednie działania.")
            elif typ_pola == "kolejka":
                # Kod dla pola Kolejka
                print("Kolejka. Wykonaj odpowiednie działania.")

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(self.game_board, (board_x, board_y))
        for player in self.players:
            player.draw(screen)
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Oczka: " + str(self.dice_roll), True, (0, 0, 0))
        text_rect = text.get_rect(center=(available_width // 8, available_width // 4 - 100))
        screen.blit(text, text_rect)

        current_player = self.players[self.current_player_index]
        typ_polaa = sprawdz_typ_pola(current_player.current_point)
        player_position_text = font.render("Aktualne pole: " + str(current_player.current_point) + str(typ_polaa), True,
                                           (0, 0, 0))
        player_position_rect = player_position_text.get_rect(center=(available_width // 8, available_width // 4 - 50))
        screen.blit(player_position_text, player_position_rect)

        current_field = Fields[current_player.current_point]
        if isinstance(current_field, Estate) and current_field.get_owner():
            owner_text = font.render("Właściciel: " + current_field.get_owner().name, True, (0, 0, 0))
            owner_rect = owner_text.get_rect(center=(available_width * 0.125, available_width // 4))
            screen.blit(owner_text, owner_rect)

        current_player = self.players[self.current_player_index]
        current_player_text = font.render("Aktualny gracz: " + str(current_player.name), True, (0, 0, 0))
        current_player_rect = current_player_text.get_rect(center=(available_width // 8, available_width // 4 + 50))
        screen.blit(current_player_text, current_player_rect)

        money_text = font.render("Pieniądze: " + str(current_player.money), True, (0, 0, 0))
        money_rect = money_text.get_rect(center=(available_width // 8, available_width // 4 + 100))
        screen.blit(money_text, money_rect)

        # Wyświetlanie posiadanych własności obecnego gracza
        player_properties_text = font.render(
            "Posiadane własności: " + ", ".join([prop.get_name() for prop in current_player.properties]), True,
            (0, 0, 0))
        player_properties_rect = player_properties_text.get_rect(
            center=(available_width * 0.125, available_width // 4 + 150))
        screen.blit(player_properties_text, player_properties_rect)

        # Sprawdź typ pola i wyświetl przycisk kupowania dla pól do kupienia
        if typ_polaa == "estate" and current_field.get_owner() is None:
            draw.rect(screen, BUY_BUTTON_COLOR, buy_button_rect)
            buy_button_font = pygame.font.Font(None, FONT_SIZE // 2)
            buy_button_text = buy_button_font.render("Kup" + current_field.name, True, BUY_BUTTON_TEXT_COLOR)
            buy_button_text_rect = buy_button_text.get_rect(center=buy_button_rect.center)
            screen.blit(buy_button_text, buy_button_text_rect)
        elif isinstance(current_field,
                        Estate) and current_field.get_owner() and current_field.get_owner() != current_player:
            rent_text = font.render("Płacisz " + str(current_field.get_rent()) + " czynszu", True, (0, 0, 0))
            rent_rect = rent_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
            screen.blit(rent_text, rent_rect)

        pygame.display.flip()

    def handle_events(self):
        global buy_button_rect
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window_open = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.waiting_for_input:
                    self.roll_dice()
                    current_player = self.players[self.current_player_index]
                    self.move_player(current_player)
                    self.waiting_for_input = True  # Ustawienie flagi oczekiwania na wejście

                elif event.key == pygame.K_RIGHT and self.waiting_for_input:
                    self.waiting_for_input = False  # Zakończenie oczekiwania na wejście
                    self.switch_to_next_player()

                elif event.key == pygame.K_p and self.waiting_for_input:
                    current_player = self.players[self.current_player_index]
                    print("Posiadane pieniądze:", current_player.get_money())

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buy_button_rect.collidepoint(mouse_pos):
                    # Kod wykonujący kupno pola
                    current_player = self.players[self.current_player_index]
                    current_field = Fields[current_player.current_point]
                    if current_player.get_money() >= current_field.get_price():
                        if isinstance(current_field, Estate) and current_field.get_owner() is None:
                            # Aktualizacja informacji o polu i graczu
                            current_field.set_owner(current_player)
                            current_player.subtract_money(current_field.get_price())
                            current_player.add_property(current_field)

        for player in self.players:
            player.update(keys_pressed)

    def start(self):
        self.initialize_players()

        while self.window_open:
            self.handle_events()
            self.draw_game_board()
            clock.tick(60)


menu = menuscreen
menu.start()
game_board = Board(len(menu.get_players_name()), menu.get_players_name())
game_board.start()
