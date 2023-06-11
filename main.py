import pygame
from pygame import draw

import GameRatio
from Chance import Chance
from CommunityChest import CommunityChest
from Dice import Dice
from Estate import Estate
from Field import Field
from GameRatio import available_width, available_height, calculate_game_board_dimensions, game_board_image, IMAGES
from IncomeTax import IncomeTax
from LoadImages import get_dice_images, chance_card_image, chest_card_image
from MenuScreen import MenuScreen
from Player import Player
from RailRoad import RailRoad

BACKGROUND_COLOR = (255, 240, 220)
DICE_IMAGES = get_dice_images()
CHANCE_CARD_IMAGE, CHANCE_CARD_IMAGE_2 = chance_card_image()
CHEST_CARD_IMAGE, CHEST_CARD_IMAGE_2 = chest_card_image()

pygame.init()
screen = GameRatio.screen
clock = pygame.time.Clock()
menuscreen = MenuScreen()
pygame.display.set_caption("Monopoly")
game_board_width, game_board_height = calculate_game_board_dimensions()

game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
game_board_x = int((available_width - game_board_width) / 2)
game_board_y = int((available_height - game_board_height) / 2)

board_x = available_width // 4
board_y = int((available_height - game_board_height) / 2)
PAWN_SIZE = (game_board_width // 13, game_board_height // 13)
FONT_SIZE = available_height // 30
buy_button_rect = pygame.Rect(available_width * 0.07, available_height * 0.8,
                              available_width * 0.1, available_height * 0.05)


def sprawdz_typ_pola(indeks_pola):
    return Fields[indeks_pola].type


Fields = [
    Field("Start", board_x + (game_board_width * 0.9), board_y + game_board_height - PAWN_SIZE[1], "start"),
    Estate("Białystok", board_x + (game_board_width * 0.8), board_y + game_board_height - PAWN_SIZE[1], "estate", 60),
    CommunityChest("Skrzynia", board_x + (game_board_width * 0.73), board_y + game_board_height - PAWN_SIZE[1],
                   "chance"),
    Estate("Bełchatów", board_x + (game_board_width * 0.64), board_y + game_board_height - PAWN_SIZE[1], "estate", 60),
    IncomeTax("Podatek", board_x + (game_board_width * 0.56), board_y + game_board_height - PAWN_SIZE[1], "tax", 200),
    RailRoad("Pociąg Regio", board_x + (game_board_width * 0.48), board_y + game_board_height - PAWN_SIZE[1],
             "kolejka", 50),
    Estate("Lublin", board_x + (game_board_width * 0.4), board_y + game_board_height - PAWN_SIZE[1], "estate", 100),
    Chance("Szansa", board_x + (game_board_width * 0.32), board_y + game_board_height - PAWN_SIZE[1], "chance"),
    Estate("Katowice", board_x + (game_board_width * 0.25), board_y + game_board_height - PAWN_SIZE[1], "estate", 100),
    Estate("Kraków", board_x + (game_board_width * 0.17), board_y + game_board_height - PAWN_SIZE[1], "estate", 120),
    Field("Wiezienie", board_x + (game_board_width * 0.05), board_y + game_board_height - PAWN_SIZE[1], "jail"),
    Estate("Toruń", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.8), "estate", 140),
    IncomeTax("Łódź", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.7), "tax", 150),
    Estate("Elbląg", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.65), "estate", 140),
    Estate("Szczecin", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.55), "estate", 160),
    RailRoad("Kolejka linowa", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.46), "kolejka", 100),
    Estate("Bydgoszcz", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.38), "estate", 180),
    CommunityChest("Skrzynia", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.3),
                   "chance"),
    Estate("Tarnów", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.22), "estate", 180),
    Estate("Wrocław", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.15), "estate", 200),
    Field("Darmowy Parking", board_x + (game_board_width * 0.05), board_y + (game_board_height * 0.03), "parking"),
    Estate("Kalisz", board_x + (game_board_width * 0.17), board_y + (game_board_height * 0.03), "estate", 220),
    Chance("Szansa", board_x + (game_board_width * 0.25), board_y + (game_board_height * 0.03), "chance"),
    Estate("Gdynia", board_x + (game_board_width * 0.32), board_y + (game_board_height * 0.03), "estate", 220),
    Estate("Poznań", board_x + (game_board_width * 0.4), board_y + (game_board_height * 0.03), "estate", 240),
    RailRoad("Metro", board_x + (game_board_width * 0.48), board_y + (game_board_height * 0.03), "kolejka", 150),
    Estate("Opole", board_x + (game_board_width * 0.56), board_y + (game_board_height * 0.03), "estate", 260),
    Estate("Katowice", board_x + (game_board_width * 0.64), board_y + (game_board_height * 0.03), "estate", 260),
    IncomeTax("Podatek", board_x + (game_board_width * 0.73), board_y + (game_board_height * 0.03), "tax", 150),
    Estate("Rzeszów", board_x + (game_board_width * 0.8), board_y + (game_board_height * 0.03), "estate", 280),
    Field("Więzienie", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.03), "go_to_jail"),
    Estate("Gdańsk", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.15), "estate", 300),
    Estate("", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.22), "estate", 300),
    CommunityChest("Skrzynia", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.3),
                   "chance"),
    Estate("Kielce", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.38), "estate", 320),
    RailRoad("Tramwaj", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.46), "kolejka", 200),
    Chance("Szansa", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.55), "chance"),
    Estate("Olsztyn", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.65), "estate", 350),
    IncomeTax("Podatek", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.7), "tax", 150),
    Estate("Warszawa", board_x + (game_board_width * 0.93), board_y + (game_board_height * 0.8), "estate", 400),
]


class Board:
    def __init__(self, num_players, player_names, player_colors):
        self.current_player_index = 0
        self.players = []
        self.player_colors = player_colors
        self.player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
        self.num_players = num_players
        self.window_open = True
        self.game_board_width, self.game_board_height = calculate_game_board_dimensions()
        self.game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
        self.dice = Dice()
        self.dice_roll_1 = 0
        self.dice_roll_2 = 0
        self.code_message = 0
        self.player_names = player_names
        self.waiting_for_input = False
        self.show_buy_button = False
        self.card_action = False
        self.dice_roll_animation = False
        self.card_animation = False
        self.current_card = None
        self.show_card = False

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        if self.players[self.current_player_index].in_jail:
            self.players[self.current_player_index].in_jail = False
            self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        # self.dice_roll_1 = self.dice.roll()
        self.dice_roll_1 = 3
        self.dice_roll_2 = 2
        self.dice_roll_animation = True

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[i % len(self.player_images)]
            player = Player(player_image, self.player_names[i], int(game_board_width * 1.45) - i * 10,
                            int(game_board_height * 0.9), PAWN_SIZE)
            if i % 2 == 1:
                player.rect.move_ip([0, game_board_height // 20])
            self.players.append(player)

    def player_action(self, field_type, player):
        current_field = Fields[player.current_point]
        if field_type == "estate":
            owner = current_field.get_owner()
            if owner and owner != player:
                rent = current_field.get_rent()
                player.pay_rent(rent)
                owner.add_money(rent)
                self.code_message = 1
            elif owner is None:
                self.show_buy_button = True

        elif field_type == "chance":
            self.code_message = 2
            current_field = Fields[player.current_point]
            current_field.get_random_chance_cards()
            chance = current_field
            self.current_card = chance.get_current_card()
            self.card_animation = True
            self.card_action = True

        elif field_type == "go_to_jail":
            self.code_message = 3
            player.current_point = 10
            player.rect.center = Fields[10].get_coordinates()
            player.in_jail = True
        elif field_type == "tax":
            tax = current_field.get_tax()
            player.subtract_money(tax)
            self.code_message = 4
        elif field_type == "chest":
            self.code_message = 2
            current_field = Fields[player.current_point]
            current_field.get_random_chance_cards()
            chance = current_field
            self.current_card = chance.get_current_card()
            self.card_action = True
        elif field_type == "kolejka":
            owner = current_field.get_owner()
            if owner and owner != player:
                rent = current_field.get_rent()
                player.pay_rent(rent)
                owner.add_money(rent)
                self.code_message = 1
            elif owner is None:
                self.show_buy_button = True

    def player_move(self):
        player = self.players[self.current_player_index]
        if self.card_action:
            self.current_card.execute_action(player, self.players, Fields)
            self.card_action = False

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
        if code == 1:
            message = ("Płacisz " + str(field.get_rent()) + " czynszu")

        elif code == 2:
            current_card = field.get_current_card()
            description = current_card.get_description()
            # message = ("Twoja karta: \n" + description)
            colletion = [word.split(' ') for word in description.splitlines()]
            space = font.size(' ')[0]
            x, y = available_width * 0.35, available_height * 0.4
            for lines in colletion:
                for words in lines:
                    word_surface = font.render(words, True, (0, 0, 0))
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= available_width * 0.65:
                        x = available_width * 0.35
                        y += word_height
                    screen.blit(word_surface, (x, y))
                    x += word_width + space
                x = available_width * 0.35
                y += word_height
        elif code == 3:
            message = "Idziesz do więzienia"
        elif code == 4:
            tax = field.get_tax()
            message = ("Płacisz" + str(tax) + "$ podatku")
        else:
            message = ""
        if code != 2:
            message_text = font.render(message, True, (0, 0, 0))
            message_rect = message_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
            screen.blit(message_text, message_rect)

    def draw_buy_button(self, field_name):
        draw.rect(screen, (0, 255, 0), buy_button_rect)
        buy_button_font = pygame.font.Font(None, FONT_SIZE // 2)
        buy_button_text = buy_button_font.render("Kup " + field_name, True, (255, 255, 255))
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
        self.dice_roll_animation = False

    def animate_card(self):
        field_type = self.players[self.current_player_index].get_current_point()
        print("Field type:" + str(field_type))
        if field_type == 7 or field_type == 22 or field_type == 36:
            image_1 = CHANCE_CARD_IMAGE
            image_2 = CHANCE_CARD_IMAGE_2
        else:
            image_1 = CHEST_CARD_IMAGE
            image_2 = CHEST_CARD_IMAGE_2
        frames = 30  # Liczba klatek animacji
        delay = 30  # Opóźnienie między klatkami w milisekundach
        for j in range(0, 3):
            for i in range(frames):
                self.draw_game_board()
                for player in self.players:
                    player.draw(screen)
                if j == 0:
                    scaled_image = pygame.transform.scale(image_1, ((GameRatio.get_width() * i) // 80,
                                                                    GameRatio.get_height() * i // 60))
                elif j == 1:
                    scaled_image = pygame.transform.scale(image_1, ((GameRatio.get_width() * (30 - i) // 80),
                                                                    GameRatio.get_height() // 2))
                else:
                    scaled_image = pygame.transform.scale(image_2, ((GameRatio.get_width() * i) // 80,
                                                                    GameRatio.get_height() // 2))
                card_rect = scaled_image.get_rect(center=(available_width // 2, available_height // 2))
                screen.blit(scaled_image, card_rect)
                pygame.time.wait(delay)
                clock.tick(60)
                pygame.display.flip()
        self.card_animation = False
        self.show_card = True

    def draw_card(self):
        field_type = self.players[self.current_player_index].get_current_point()
        if field_type == 7 or field_type == 22 or field_type == 36:
            image = CHANCE_CARD_IMAGE_2
        else:
            image = CHEST_CARD_IMAGE_2
        card_image = pygame.transform.scale(image, ((GameRatio.get_width() * 30) // 80,
                                                    GameRatio.get_height() // 2))
        card_rect = card_image.get_rect(center=(available_width // 2, available_height // 2))
        screen.blit(card_image, card_rect)

    def draw_players_information(self, font):
        proportion = 0.015
        temp = 0
        for player in self.players:
            current_player = player
            current_player_text = font.render("gracz: " + str(current_player.name), True, self.player_colors[temp])
            current_player_rect = current_player_text.get_rect(
                center=(available_width * 0.9, available_height * proportion))
            proportion = proportion + 0.030
            screen.blit(current_player_text, current_player_rect)
            money_text = font.render("Pieniądze: " + str(current_player.money), True, (0, 0, 0))
            money_rect = money_text.get_rect(center=(available_width * 0.9, available_height * proportion))
            proportion = proportion + 0.030
            screen.blit(money_text, money_rect)
            player_properties_text = font.render("Posiadane własności: ", True, (0, 0, 0))
            player_properties_rect = player_properties_text.get_rect(
                center=(available_width * 0.9, available_height * proportion))
            proportion = proportion + 0.030
            screen.blit(player_properties_text, player_properties_rect)
            player_properties_text = font.render(", ".join([prop.get_name() for prop in current_player.properties]),
                                                 True, (0, 0, 0))
            player_properties_rect = player_properties_text.get_rect(
                center=(available_width * 0.9, available_height * proportion))
            proportion = proportion + 0.18
            screen.blit(player_properties_text, player_properties_rect)
            temp += 1

    def draw_current_field_information(self, font):
        current_player = self.players[self.current_player_index]
        current_player_text = font.render("Aktualny gracz: " + str(current_player.name),
                                          True, self.player_colors[self.current_player_index])
        current_player_rect = current_player_text.get_rect(center=(available_width // 8, available_height * 0.2))
        screen.blit(current_player_text, current_player_rect)

        text = font.render("Wyrzucone oczka: " + str(self.dice_roll_1) + " oraz " + str(self.dice_roll_2),
                           True, (0, 0, 0))
        text_rect = text.get_rect(center=(available_width // 8, available_height * 0.3))
        screen.blit(text, text_rect)

        current_player = self.players[self.current_player_index]
        current_field = Fields[current_player.current_point]
        player_position_text = font.render("Aktualne pole: " + current_field.get_name(), True,
                                           (0, 0, 0))
        player_position_rect = player_position_text.get_rect(center=(available_width // 8, available_height * 0.4))
        screen.blit(player_position_text, player_position_rect)

        money_text = font.render("Pieniądze: " + str(current_player.money), True, (0, 0, 0))
        money_rect = money_text.get_rect(center=(available_width // 8, available_height * 0.6))
        screen.blit(money_text, money_rect)

        # Wyświetlanie posiadanych własności obecnego gracza
        player_properties_text = font.render(
            "Posiadane własności: " + ", ".join([prop.get_name() for prop in current_player.properties]), True,
            (0, 0, 0))
        player_properties_rect = player_properties_text.get_rect(
            center=(available_width * 0.125, available_width // 4 + 150))
        screen.blit(player_properties_text, player_properties_rect)

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(self.game_board, (board_x, board_y))

    def draw_game(self):
        font = pygame.font.Font(None, FONT_SIZE)
        self.draw_game_board()
        for player in self.players:
            player.draw(screen)
        self.draw_players_information(font)
        self.draw_current_field_information(font)

        current_field = Fields[self.players[self.current_player_index].current_point]
        # Sprawdź typ pola i wyświetl przycisk kupowania dla pól do kupienia
        if self.show_buy_button:
            self.draw_buy_button(current_field.name)
        if self.card_animation:
            self.animate_card()
        if self.show_card:
            self.draw_card()
        if self.code_message:
            self.draw_message(self.code_message, current_field, font)
        if self.dice_roll_animation:
            self.animate_dice_roll(self.dice_roll_1 - 1, self.dice_roll_2 - 1)

        pygame.display.flip()

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window_open = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.window_open = False
                    pygame.quit()
                elif event.key == pygame.K_SPACE and not self.waiting_for_input:
                    self.roll_dice()
                    current_player = self.players[self.current_player_index]
                    self.move_player(current_player)
                    self.waiting_for_input = True  # Ustawienie flagi oczekiwania na wejście

                elif event.key == pygame.K_RIGHT and self.waiting_for_input:
                    self.waiting_for_input = False  # Zakończenie oczekiwania na wejście
                    self.show_buy_button = False
                    self.show_card = False
                    self.code_message = 0
                    self.player_move()
                    self.switch_to_next_player()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if buy_button_rect.collidepoint(mouse_pos):
                    # Kod wykonujący kupno pola
                    current_player = self.players[self.current_player_index]
                    current_field = Fields[current_player.current_point]
                    if current_player.get_money() >= current_field.get_price():
                        if current_field.get_owner() is None:
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


menuscreen.start()
print(menuscreen.get_selected_colors())
game_board_start = Board(len(menuscreen.get_players_name()), menuscreen.get_players_name(),
                         menuscreen.get_selected_colors())
game_board_start.start()

