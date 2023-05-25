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


class Dice:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, px, py):
        super().__init__()
        self.image = pygame.transform.scale(image, PAWN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.current_point = 0
        self.money = 1500

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Property:
    def __init__(self, name, price, rent):
        self.name = name
        self.price = price
        self.rent = rent
        self.owner = None

    def is_owned(self):
        return self.owner is not None

    def is_available(self):
        return self.owner is None

    def buy(self, player):
        if self.is_available() and player.money >= self.price:
            player.money -= self.price
            self.owner = player
            return True
        return False

    def pay_rent(self, player):
        if self.is_owned() and player != self.owner:
            player.money -= self.rent
            self.owner.money += self.rent


class MenuScreen:
    def __init__(self):
        self.menu_rects = []
        self.num_players = 0

    def start(self):
        while self.num_players == 0:
            self.handle_menu_events()
            self.draw_menu()

        game_board = GameBoard(self.num_players)
        game_board.start()

    def handle_menu_events(self):
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
        button_color = (0, 255, 0)
        text_color = (0, 0, 0)

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


class GameBoard:
    def __init__(self, num_players):
        self.current_player_index = 0
        self.players = []
        self.player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
        self.num_players = num_players
        self.occupied_points = []  # Lista zajętych punktów na planszy
        self.window_open = True
        self.menu = MenuScreen()
        self.game_board_width, self.game_board_height = calculate_game_board_dimensions()
        self.dice_roll = 0

        self.properties = [
            Property("Property 1", 200, 20),
            Property("Property 2", 300, 30),
            Property("Property 3", 400, 40),
            Property("Property 4", 500, 50),
            Property("Property 5", 600, 60),
        ]

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players

    def roll_dice(self):
        dice = Dice()
        self.dice_roll = dice.roll()

    def initialize_players(self):
        for i in range(self.num_players):
            player_image = self.player_images[i % len(self.player_images)]
            player = Player(player_image, int(game_board_width * 1.45) - i * 10, int(game_board_height * 0.9))
            if i % 2 == 1:
                player.rect.move_ip([0, game_board_height // 20])
            self.players.append(player)

    def move_player(self, player):
        if self.dice_roll > 0:
            points = [
                (board_x + (game_board_width * 0.8), board_y + game_board_height - PAWN_SIZE[1]),  # 1 pole br
                (board_x + (game_board_width * 0.75), board_y + game_board_height - PAWN_SIZE[1]),  # 2 skrzynia
                (board_x + (game_board_width * 0.65), board_y + game_board_height - PAWN_SIZE[1]),  # 3 pole br
                (board_x + (game_board_width * 0.6), board_y + game_board_height - PAWN_SIZE[1]),  # 4 podatek
                (board_x + (game_board_width * 0.5), board_y + game_board_height - PAWN_SIZE[1]),  # 5 kolejka
                (board_x + (game_board_width * 0.4), board_y + game_board_height - PAWN_SIZE[1]),  # 6 pole bl
                (board_x + (game_board_width * 0.35), board_y + game_board_height - PAWN_SIZE[1]),  # 7 szansa
                (board_x + (game_board_width * 0.25), board_y + game_board_height - PAWN_SIZE[1]),  # 8 pole bl
                (board_x + (game_board_width * 0.17), board_y + game_board_height - PAWN_SIZE[1]),  # 9 pole bl
                (board_x + (game_board_width * 0.05), board_y + game_board_height - PAWN_SIZE[1]),  # wiezienie
            ]

            for _ in range(self.dice_roll):
                target_x, target_y = points[player.current_point]
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
                player.current_point = (player.current_point + 1) % len(points)

            if player.current_point > 0:
                property_to_buy = self.properties[player.current_point - 1]
                player.buy_property(property_to_buy)

    def draw_game_board(self):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(game_board, (board_x, board_y))
        for player in self.players:
            player.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render("Oczka: " + str(self.dice_roll), True, (0, 0, 0))
        text_rect = text.get_rect(center=(available_width // 8, available_width // 4 - 100))
        screen.blit(text, text_rect)

        current_player = self.players[self.current_player_index]
        player_position_text = font.render("Aktualne pole: " + str(current_player.current_point), True, (0, 0, 0))
        player_position_rect = player_position_text.get_rect(center=(available_width // 8, available_width // 4 - 50))
        screen.blit(player_position_text, player_position_rect)

        current_player_text = font.render("Aktualny gracz: " + str(self.current_player_index + 1), True, (0, 0, 0))
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


menu = MenuScreen()
menu.start()
