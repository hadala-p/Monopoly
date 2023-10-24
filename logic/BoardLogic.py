import pygame

from Constants import GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT, PAWN_SIZE, BUY_BUTTON_RECT, FONT_SIZE
from data.Dice import Dice
from data.Player import Player
from logic.GameRatio import IMAGES, calculate_game_board_dimensions
from logic.Ui import draw_current_field_information, draw_buy_button, \
    animate_card, draw_card, draw_message, animate_dice_roll, draw_results, draw_current_player_information
from logic.Utils import sprawdz_typ_pola, clock, Fields
from resources.LoadSounds import play_sound


class Board:
    def __init__(self, num_players, player_names, player_colors):
        self.current_player_index = 0
        self.players = []
        self.player_colors = player_colors
        self.player_images = {(255, 0, 0): IMAGES['REDPAWN'], (0, 255, 0): IMAGES['GREENPAWN'],
                              (0, 0, 255): IMAGES['BLUEPAWN'], (255, 255, 0): IMAGES['YELLOWPAWN']}
        self.num_players = num_players
        self.window_open = True
        self.GAME_BOARD_WIDTH, self.GAME_BOARD_HEIGHT = calculate_game_board_dimensions()
        self.dice = Dice()
        self.dice_roll_1 = 0
        self.dice_roll_2 = 0
        self.code_message = 0
        self.player_names = player_names
        self.waiting_for_input = False
        self.show_buy_button = False
        self.card_action = False
        self.show_card = False
        self.show_property_card = False
        self.dice_roll_animation = False
        self.card_animation = False
        self.current_card = None
        self.finish = False

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        if self.players[self.current_player_index].is_bankrupt:
            self.current_player_index = (self.current_player_index + 1) % self.num_players
        if self.players[self.current_player_index].in_jail:
            self.players[self.current_player_index].in_jail = False
            self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        self.dice_roll_1 = self.dice.roll()
        self.dice_roll_2 = self.dice.roll()
        play_sound("roll_dice")
        self.dice_roll_animation = True

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[self.player_colors[i]]
            player = Player(player_image, self.player_names[i], int(GAME_BOARD_WIDTH * 1.45) - i * 10,
                            int(GAME_BOARD_HEIGHT * 0.9), PAWN_SIZE)
            if i % 2 == 1:
                player.rect.move_ip([0, GAME_BOARD_HEIGHT // 20])
            self.players.append(player)

    def player_action(self, field_type, player):
        current_field = Fields[player.current_point]
        if field_type == "estate":
            self.show_property_card = True
            owner = current_field.get_owner()
            if owner and owner != player:
                rent = current_field.get_rent()
                player.pay_rent(rent)
                owner.add_money(rent)
                self.code_message = 1

            elif owner is None or owner is player:
                self.show_buy_button = True

        elif field_type == "chance":
            self.code_message = 2
            current_field = Fields[player.current_point]
            current_field.get_random_chance_cards()
            chance = current_field
            self.current_card = chance.get_current_card()
            self.card_animation = True
            self.card_action = True
            play_sound("card")

        elif field_type == "go_to_jail":
            self.code_message = 3
            player.current_point = 10
            player.rect.center = Fields[10].get_coordinates()
            player.in_jail = True
            play_sound("jail")
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
            play_sound("card")
        elif field_type == "kolejka":
            self.show_property_card = True
            owner = current_field.get_owner()
            if owner and owner != player:
                rent = current_field.get_rent()
                player.pay_rent(rent)
                owner.add_money(rent)
                self.code_message = 1
            elif owner is None:
                self.show_buy_button = True

    def player_move(self, player):
        if self.card_action:
            self.current_card.execute_action(player, self.players, Fields)
            self.card_action = False

    def player_is_bankrupt(self, player):
        if player.get_money() < 0:
            player.is_bankrupt = True
            self.code_message = 6
            play_sound("bankrupt")

    def is_enough_players(self):
        players_in_game = 0
        for player in self.players:
            if not player.is_bankrupt:
                players_in_game += 1
        if players_in_game < 2:
            play_sound("results")
            self.finish = True

    def buy_button_action(self):
        current_player = self.players[self.current_player_index]
        current_field = Fields[current_player.current_point]
        if current_player is not current_field.get_owner():
            if current_player.get_money() >= current_field.get_price():
                if current_field.get_owner() is None:
                    # Aktualizacja informacji o polu i graczu
                    current_field.set_owner(current_player)
                    current_player.subtract_money(current_field.get_price())
                    current_player.add_property(current_field)
                    current_player.set_score(current_field.get_value())
                    play_sound("buy_property")

            else:
                self.code_message = 7
                play_sound("error")
        elif current_field.get_owner() is current_player:
            if current_player.get_money() >= current_field.get_buy_home_price():
                current_field.buy_home()
                current_player.subtract_money(current_field.get_buy_home_price())
            else:
                self.code_message = 7
                play_sound("error")

    def move_player(self, player):
        if self.dice_roll_1 > 0:
            player.current_point = (player.current_point + 1) % len(Fields)  # Aktualizacja pozycji gracza

            # Przesunięcie pionka po pozostałych polach
            for _ in range(1, self.dice_roll_1 + self.dice_roll_2):
                player.current_point = (player.current_point + 1) % len(Fields)
                if player.current_point % 40 == 0:
                    player.add_money(200)
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
            play_sound("step")
            # Sprawdzenie typu pola i wykonanie odpowiednich akcji
            self.player_action(sprawdz_typ_pola(player.current_point), player)

    def draw_game(self):
        font = pygame.font.Font(None, FONT_SIZE)
        draw_current_player_information(font, self.players, self.player_colors, self.current_player_index,
                                        self.dice_roll_1, self.dice_roll_2)

        current_field = Fields[self.players[self.current_player_index].current_point]
        # Sprawdź typ pola i wyświetl przycisk kupowania dla pól do kupienia
        if self.show_property_card:
            draw_current_field_information(font, self.players, self.current_player_index)
        if self.show_buy_button:
            draw_buy_button(current_field.name)
        if self.card_animation:
            animate_card(self.players, self.current_player_index)
            self.card_animation = False
            self.show_card = True
        if self.show_card:
            draw_card(self.players, self.current_player_index)
        if self.code_message:
            draw_message(self.code_message, current_field, pygame.font.Font(None, FONT_SIZE * 2), self.players,
                         self.current_player_index)
        if self.dice_roll_animation:
            animate_dice_roll(self.dice_roll_1 - 1, self.dice_roll_2 - 1, self.players)
            self.dice_roll_animation = False
        if self.finish:
            draw_results(self.players)

        pygame.display.flip()

    def handle_events(self):
        current_player = self.players[self.current_player_index]
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
                    self.code_message = 0
                    self.roll_dice()
                    self.move_player(current_player)
                    self.waiting_for_input = True  # Ustawienie flagi oczekiwania na wejście

                elif event.key == pygame.K_RIGHT and self.waiting_for_input:
                    self.waiting_for_input = False  # Zakończenie oczekiwania na wejście
                    self.show_buy_button = False
                    self.show_card = False
                    self.show_property_card = False
                    self.code_message = 0
                    self.player_move(current_player)
                    self.player_is_bankrupt(current_player)
                    self.is_enough_players()
                    self.switch_to_next_player()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if BUY_BUTTON_RECT.collidepoint(mouse_pos):
                    self.buy_button_action()
                self.show_buy_button = False

        for player in self.players:
            player.update(keys_pressed)

    def start(self):
        self.initialize_players()
        play_sound("game_start")
        while self.window_open:
            self.handle_events()
            self.draw_game()
            clock.tick(60)
