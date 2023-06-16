import sys

import pygame
import os

import GameRatio
from GameRatio import calculate_game_board_dimensions, available_width, available_height
from LoadImages import load_images

BACKGROUND_COLOR = (255, 240, 200)

pygame.init()
screen = GameRatio.screen
clock = pygame.time.Clock()

path = os.path.join(os.pardir, 'C:/Users/Piotrek/PycharmProjects/Monopoly/images/')

game_board_image, IMAGES = load_images()

game_board_width, game_board_height = calculate_game_board_dimensions()

game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
game_board_x = int((available_width - game_board_width) / 2)
game_board_y = int((available_height - game_board_height) / 2)

board_x = available_width // 4
board_y = int((available_height - game_board_height) / 2)


class MenuScreen:
    def __init__(self):
        self.menu_rects = []
        self.num_players = 0
        self.players_names = None
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.selected_colors = []

    def start(self):
        self.show_start_button()
        while self.num_players == 0:
            self.handle_menu_events()
            self.draw_menu()

        self.players_names = self.add_player_names()

    def get_num_players(self):
        return self.num_players

    def get_selected_colors(self):
        return self.selected_colors

    def get_players_name(self):
        return self.players_names

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
        text_rect = text.get_rect(center=(GameRatio.SCREEN_WIDTH // 2, GameRatio.SCREEN_WIDTH // 7))
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

    def add_player_names(self):
        player_names = []
        font = pygame.font.Font(None, 36)
        text = font.render("Wprowadź nazwy graczy", True, (0, 0, 0))
        text_rect = text.get_rect(center=(GameRatio.SCREEN_WIDTH // 2, GameRatio.SCREEN_WIDTH // 7 ))
        screen.blit(text, text_rect)

        pygame.display.flip()

        for i in range(self.num_players):
            name = ""
            should_break = False  # Zmienna logiczna do śledzenia, czy obie pętle powinny być przerwane
            while not should_break:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            should_break = True  # Ustawienie zmiennej should_break na True, aby przerwać obie pętle
                            break

                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        elif event.unicode.isprintable():
                            name += event.unicode
                screen.fill(BACKGROUND_COLOR)
                screen.blit(text, text_rect)
                player_name_text = font.render("Gracz {}: {}".format(i + 1, name), True, (0, 0, 0))
                player_name_rect = player_name_text.get_rect(center=(
                    GameRatio.SCREEN_WIDTH // 2, GameRatio.SCREEN_WIDTH // 6))
                screen.blit(player_name_text, player_name_rect)

                pygame.display.flip()

            player_names.append(name)
            self.selected_colors.append(self.select_color())

        return player_names

    def select_color(self):
        selected_color = None
        while selected_color is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.color_rects):
                        if rect.collidepoint(mouse_pos):
                            selected_color = self.colors[i]
                            break

            self.draw_color_selection()
            pygame.display.flip()

        return selected_color

    def show_start_button(self):
        image = pygame.image.load(os.path.join(path, 'start_background.png')).convert_alpha()
        scaled = pygame.transform.scale(image, (available_width, available_height ))
        image = scaled
        image_rect = image.get_rect(center=(available_width // 2, available_height // 2))
        start_button_rect = pygame.Rect((available_width // 4), (available_height // 4), available_width // 2,
                                        available_height // 3)
        start_button_color = (0, 255, 0)
        text_color = (0, 0, 0)

        font = pygame.font.Font(None, 36)
        start_button_text = font.render("Start", True, text_color)
        start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        return

            screen.fill(BACKGROUND_COLOR)
            screen.blit(image, image_rect)
            pygame.draw.rect(screen, start_button_color, start_button_rect)
            screen.blit(start_button_text, start_button_text_rect)
            pygame.display.flip()
            clock.tick(60)

    def draw_color_selection(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Wybierz kolor pionka", True, (0, 0, 0))
        text_rect = text.get_rect(center=(GameRatio.SCREEN_WIDTH // 2, GameRatio.SCREEN_WIDTH // 4))
        screen.blit(text, text_rect)

        self.color_rects = []
        for i, color in enumerate(self.colors):
            rect = pygame.Rect((available_width // 2) + ((i * 120) - 180), (available_height // 2) + 100, 100, 40)
            pygame.draw.rect(screen, color, rect)
            self.color_rects.append(rect)

        pygame.display.flip()


