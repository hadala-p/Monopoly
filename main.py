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
pygame.display.set_caption("Monopoly")


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
DICE_IMAGES = [pygame.image.load(os.path.join(path, f'{i}.png')).convert_alpha() for i in range(1, 20)]
scaled_images = [pygame.transform.scale(image, (available_width // 2, available_height // 2)) for image in DICE_IMAGES]
DICE_IMAGES = scaled_images


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
FONT_SIZE = available_height // 30


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


class CommunityChest(Field):
    def __init__(self, name, position_x, position_y, type):
        super().__init__(name, position_x, position_y, type)
        self.num_cards = 3


class Chance(Field):
    def __init__(self, name, position_x, position_y, type):
        super().__init__(name, position_x, position_y, type)
        self.cards = self.get_chance_cards()
        self.current_card_index = 0

    def add_card(self, card):
        self.cards.append(card)

    def get_chance_cards(self):
        return [ChanceCard("Card1", "Przejdź do Warszawa"),
                ChanceCard("Card2", "Przejdź na Start (Zabierz 200 $)"),
                ChanceCard("Card3", "Przejdź do Illinois Avenue. Jeśli zdasz Go, odbierz 200 $"),
                ChanceCard("Card4", "Przejdź do St. Charles Place. Jeśli zdasz Go, odbierz 200 $"),
                ChanceCard("Card5", "Przejdź do najbliższej linii kolejowej. Jeśli go nie posiadasz, możesz go kupić"
                                    " w banku. Jeśli są właścicielami, zapłaćcie podwójną kwotę czynszu, do którego są"
                                    " w inny sposób uprawnieni"),
                ChanceCard("Card6", "Żeton postępu do najbliższego Narzędzia. Jeśli go nie posiadasz, możesz go kupić"
                                    " w banku. Jeśli posiadasz, rzuć kostką i zapłać właścicielowi łącznie"
                                    " dziesięciokrotność wyrzuconej kwoty."),
                ChanceCard("Card7", "Bank wypłaca Ci dywidendę w wysokości 50 $", ),
                ChanceCard("Card8", "Cofnij się o 3 pola"),
                ChanceCard("Card9", "Iść do więzienia. Idź bezpośrednio do więzienia, nie przechodź przez Start, nie "
                                    "zabieraj 200 $"),
                ChanceCard("Card10", "Dokonaj generalnych napraw całej swojej nieruchomości. Za każdy dom zapłać 25 $."
                                     " Za każdy hotel zapłać 100 $"),
                ChanceCard("Card11", "Kara za przekroczenie prędkości 15zł"),
                ChanceCard("Card12", "Wybierz się na wycieczkę do Reading Railroad. Jeśli przekroczysz Start,"
                                     " odbierz 200 $"),
                ChanceCard("Card13", "Otrzymałeś kredyt budowlany pobierz 150zł"),
                ChanceCard("Card13", "Zostałeś wybrany na Przewodniczącego Rady. Zapłać każdemu graczowi 50 $")]

    def get_current_card(self):
        return self.cards[self.current_card_index]

    def get_random_chance_cards(self):
        random_number = random.randint(0, len(self.cards))
        print(random_number)
        print(len(self.cards))
        self.current_card_index = 13
        return self.cards[13]


class ChanceCard:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute_action(self, player):
        # Wykonaj akcję związaną z kartą szansy
        pass

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class IncomeTax(Field):
    def __init__(self, name, position_x, position_y, type, tax):
        super().__init__(name, position_x, position_y, type)
        self.tax = tax

    def get_tax(self):
        return self.tax


Fields = [
    Field("Start", board_x + (game_board_width * 0.9), board_y + game_board_height - PAWN_SIZE[1], "start"),
    Estate("Frankfurt", board_x + (game_board_width * 0.8), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    CommunityChest("Skrzynia", board_x + (game_board_width * 0.75), board_y + game_board_height - PAWN_SIZE[1],
                   "skrzynia"),
    Estate("Berlin", board_x + (game_board_width * 0.65), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    IncomeTax("Podatek", board_x + (game_board_width * 0.6), board_y + game_board_height - PAWN_SIZE[1], "podatek",
              200),
    Field("Kolejka", board_x + (game_board_width * 0.5), board_y + game_board_height - PAWN_SIZE[1], "kolejka"),
    Estate("Warszawa", board_x + (game_board_width * 0.4), board_y + game_board_height - PAWN_SIZE[1], "estate", 600,
           10),
    Chance("Szansa", board_x + (game_board_width * 0.35), board_y + game_board_height - PAWN_SIZE[1], "szansa"),
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
        self.money = 3000
        self.properties = []
        self.in_jail = False

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

    def jail_status(self, status):
        self.in_jail = status


class Board:
    def __init__(self, num_players, player_names):
        self.current_player_index = 0
        self.players = []
        self.player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
        self.num_players = num_players
        self.window_open = True
        self.game_board_width, self.game_board_height = calculate_game_board_dimensions()
        self.game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
        self.dice = Dice()
        self.dice_roll_1 = 0
        self.dice_roll_2 = 0
        self.code_message = "0"
        self.player_names = player_names
        self.waiting_for_input = False
        self.show_buy_button = False
        self.action = False

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        self.dice_roll_1 = self.dice.roll()
        self.dice_roll_2 = self.dice.roll()
        self.action = True

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[i % len(self.player_images)]
            player = Player(player_image, self.player_names[i], int(game_board_width * 1.45) - i * 10,
                            int(game_board_height * 0.9))
            if i % 2 == 1:
                player.rect.move_ip([0, game_board_height // 20])
            self.players.append(player)

    def cards_action(self, player, card):
        pass

    def player_action(self, field_type, player):
        current_field = Fields[player.current_point]
        if field_type == "estate":
            owner = current_field.get_owner()
            if owner and owner != player:
                rent = current_field.get_rent()
                player.pay_rent(rent)
                owner.add_money(rent)
                self.code_message = "1"
            elif owner is None:
                self.show_buy_button = True

        elif field_type == "szansa":
            current_field = Fields[player.current_point]
            current_field.get_random_chance_cards()
            card = current_field
            self.cards_action(player, card)

            self.code_message = "2"

        elif field_type == "więzienie":
            # Kod dla pola Więzienie
            print("Jesteś w więzieniu. Wykonaj odpowiednie działania.")
        elif field_type == "podatek":
            tax = current_field.get_tax()
            player.subtract_money(tax)
            self.code_message = "2"
        elif field_type == "skrzynia":
            # Kod dla pola Skrzynia
            print("Otwierasz skrzynię. Wykonaj odpowiednie działania.")
        elif field_type == "kolejka":
            # Kod dla pola Kolejka
            print("Kolejka. Wykonaj odpowiednie działania.")

    def move_player(self, player):
        if self.dice_roll_1 > 0:
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
                self.draw_game()
                clock.tick(60)

            player.rect.center = target_x, target_y

            # Przesunięcie pionka po pozostałych polach
            for _ in range(1, self.dice_roll_1 + self.dice_roll_2):
                player.current_point = (player.current_point + 1) % len(Fields)
                target_x, target_y = Fields[player.current_point].get_coordinates()
                dx = target_x - player.rect.centerx
                dy = target_y - player.rect.centery
                step_x = dx / 12
                step_y = dy / 12

                for _ in range(12):
                    player.rect.move_ip([step_x, step_y])
                    pygame.time.wait(20)
                    self.draw_game()
                    clock.tick(60)

                player.rect.center = target_x, target_y

            # Sprawdzenie typu pola i wykonanie odpowiednich akcji
            self.player_action(sprawdz_typ_pola(player.current_point), player)

    def draw_message(self, code, field, font):
        if code == "1":
            rent_text = font.render("Płacisz " + str(field.get_rent()) + " czynszu", True, (0, 0, 0))
            rent_rect = rent_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
            screen.blit(rent_text, rent_rect)
        if code == "2":
            current_card = field.get_current_card()
            name = current_card.get_description()
            card_text = font.render("Twoja karta: " + name, True, (0, 0, 0))
            card_rect = card_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
            screen.blit(card_text, card_rect)
            rent_text = font.render("Twoja karta: " + name, True, (0, 0, 0))
            rent_rect = rent_text.get_rect(center=(available_width * 0.5, available_width // 4 + 150))
            screen.blit(rent_text, rent_rect)

    def draw_buy_button(self, field_name):
        draw.rect(screen, BUY_BUTTON_COLOR, buy_button_rect)
        buy_button_font = pygame.font.Font(None, FONT_SIZE // 2)
        buy_button_text = buy_button_font.render("Kup" + field_name, True, BUY_BUTTON_TEXT_COLOR)
        buy_button_text_rect = buy_button_text.get_rect(center=buy_button_rect.center)
        screen.blit(buy_button_text, buy_button_text_rect)

    def animate_dice_roll(self, dice_1_dots, dice_2_dots):
        frames = 20  # Liczba klatek animacji
        delay = 20  # Opóźnienie między klatkami w milisekundach

        for i in range(frames):
            self.draw_game_board()
            for player in self.players:
                player.draw(screen)
            if i + 1 == frames:
                dice_image_1 = DICE_IMAGES[dice_1_dots]
                dice_image_2 = DICE_IMAGES[dice_2_dots]
            else:
                dice_image_1 = DICE_IMAGES[i - 1]
                dice_image_2 = DICE_IMAGES[frames - i - 2]
            dice_1_rect = dice_image_1.get_rect(center=(available_width * 0.6, available_height // 2))
            dice_2_rect = dice_image_1.get_rect(center=(available_width * 0.4, available_height // 2))
            screen.blit(dice_image_1, dice_1_rect)
            screen.blit(dice_image_2, dice_2_rect)
            pygame.time.wait(delay)
            clock.tick(60)
            pygame.display.flip()
        pygame.time.wait(1000)
        self.action = False

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(self.game_board, (board_x, board_y))

    def draw_game(self):
        self.draw_game_board()
        for player in self.players:
            player.draw(screen)

        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Oczka: " + str(self.dice_roll_1) + str(self.dice_roll_2), True, (0, 0, 0))
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
        if self.show_buy_button:
            self.draw_buy_button(current_field.name)
        if self.code_message:
            self.draw_message(self.code_message, current_field, font)
        if self.action:
            self.animate_dice_roll(self.dice_roll_1 - 1, self.dice_roll_2 - 1)

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
                    self.show_buy_button = False
                    self.code_message = "0"
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
                self.show_buy_button = False

        for player in self.players:
            player.update(keys_pressed)

    def start(self):
        self.initialize_players()

        while self.window_open:
            self.handle_events()
            self.draw_game()
            clock.tick(60)


menu = menuscreen
menu.start()
game_board = Board(len(menu.get_players_name()), menu.get_players_name())
game_board.start()
