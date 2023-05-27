import pygame
import os
import random
from MenuScreen import MenuScreen

SCREEN_WIDTH = 1920
BACKGROUND_COLOR = (255, 240, 220)

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
typy_pol = {
    0: "Start",
    1: "Pole do kupienia",
    2: "Skrzynia",
    3: "Pole do kupienia",
    4: "Podatek",
    5: "Kolejka",
    6: "Pole do kupienia",
    7: "Szansa",
    8: "Pole do kupienia",
    9: "Pole do kupienia",
    10: "Więzienie"
    # Dodaj inne typy pól według potrzeb
}


def sprawdz_typ_pola(indeks_pola):
    return Fields[indeks_pola].name


class Dice:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


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
    def __init__(self, name, price, rent, position_x, position_y, type):
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
    Field("Frankfurt", board_x + (game_board_width * 0.8), board_y + game_board_height - PAWN_SIZE[1], "estate"),
    Field("Skrzynia", board_x + (game_board_width * 0.75), board_y + game_board_height - PAWN_SIZE[1], "skrzynia"),
    Field("Berlin", board_x + (game_board_width * 0.65), board_y + game_board_height - PAWN_SIZE[1], "state"),
    Field("Podatek", board_x + (game_board_width * 0.6), board_y + game_board_height - PAWN_SIZE[1], "podatek"),
    Field("Kolejka", board_x + (game_board_width * 0.5), board_y + game_board_height - PAWN_SIZE[1], "kolejka"),
    Field("Warszawa", board_x + (game_board_width * 0.4), board_y + game_board_height - PAWN_SIZE[1], "estate"),
    Field("Szansa", board_x + (game_board_width * 0.35), board_y + game_board_height - PAWN_SIZE[1], "szansa"),
    Field("Praga", board_x + (game_board_width * 0.25), board_y + game_board_height - PAWN_SIZE[1], "estate"),
    Field("Wiedeń", board_x + (game_board_width * 0.17), board_y + game_board_height - PAWN_SIZE[1], "Wiedeń"),
    Field("Wiezienie", board_x + (game_board_width * 0.05), board_y + game_board_height - PAWN_SIZE[1], "wiezienie"),
]


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

    def add_money(self, money):
        self.money += money

    def subtract_money(self, money):
        self.money -= money

    def buy_field(self, field):
        self.properties.append(field)


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
            if typ_pola == "Pole do kupienia":
                # Kod dla pola do kupienia
                print("To pole można kupić.")

            elif typ_pola == "Szansa":
                # Kod dla pola Szansy
                print("Wykonaj akcję związaną z polem Szansy.")

            elif typ_pola == "Więzienie":
                # Kod dla pola Więzienie
                print("Jesteś w więzieniu. Wykonaj odpowiednie działania.")
            elif typ_pola == "Podatek":
                # Kod dla pola Podatek
                print("Płacisz Podatek. Wykonaj odpowiednie działania.")
            elif typ_pola == "Skrzynia":
                # Kod dla pola Skrzynia
                print("Otwierasz skrzynię. Wykonaj odpowiednie działania.")
            elif typ_pola == "Kolejka":
                # Kod dla pola Kolejka
                print("Kolejka. Wykonaj odpowiednie działania.")

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(self.game_board, (board_x, board_y))
        for player in self.players:
            player.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render("Oczka: " + str(self.dice_roll), True, (0, 0, 0))
        text_rect = text.get_rect(center=(available_width // 8, available_width // 4 - 100))
        screen.blit(text, text_rect)

        current_player = self.players[self.current_player_index]
        typ_polaa = sprawdz_typ_pola(current_player.current_point)
        player_position_text = font.render("Aktualne pole: " + str(current_player.current_point) + str(typ_polaa), True,
                                           (0, 0, 0))
        player_position_rect = player_position_text.get_rect(center=(available_width // 8, available_width // 4 - 50))
        screen.blit(player_position_text, player_position_rect)

        current_player_text = font.render("Aktualny gracz: " + str(self.player_names[self.current_player_index]), True,
                                          (0, 0, 0))
        current_player_rect = current_player_text.get_rect(center=(available_width // 8, available_width // 4))
        screen.blit(current_player_text, current_player_rect)

        pygame.display.flip()

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window_open = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.roll_dice()
                    current_player = self.players[self.current_player_index]
                    print("Gracz", self.current_player_index + 1, "wyrzucił", self.dice_roll, "oczka.")
                    self.move_player(current_player)
                    self.switch_to_next_player()

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
