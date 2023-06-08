import pygame
import os

SCREEN_WIDTH = 1920
BACKGROUND_COLOR = (255, 240, 200)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH // 2))
clock = pygame.time.Clock()

path = os.path.join(os.pardir, 'C:/Users/Janno/PycharmProjects/Monopoly_Lenovo/images')


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


class MenuScreen:
    def __init__(self):
        self.menu_rects = []
        self.num_players = 0
        self.players_names = None

    def start(self):
        while self.num_players == 0:
            self.handle_menu_events()
            self.draw_menu()

        self.players_names = self.add_player_names()

    def get_num_players(self):
        return self.num_players

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

    def add_player_names(self):
        player_names = []
        font = pygame.font.Font(None, 36)
        text = font.render("Wprowadź nazwy graczy", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 4 - 100))
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
                player_name_rect = player_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 4 + i * 50))
                screen.blit(player_name_text, player_name_rect)

                pygame.display.flip()

            player_names.append(name)

        return player_names