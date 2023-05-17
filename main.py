import os

import pygame

pygame.init()
screen_width = 1800
screen = pygame.display.set_mode((screen_width, screen_width//2))
clock = pygame.time.Clock()

path = os.path.join(os.pardir, 'C:/Users/Piotrek/PycharmProjects/Monopoly/images')
file_names = sorted(os.listdir(path))
game_board_image = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
file_names.remove('background.jpg')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
    IMAGES[image_name] = image

available_width, available_height = pygame.display.get_surface().get_size()
image_aspect_ratio = game_board_image.get_width() / game_board_image.get_height()

if image_aspect_ratio > 1:
    game_board_width = available_width
    game_board_height = int(game_board_width / image_aspect_ratio)
else:
    game_board_height = available_height
    game_board_width = int(game_board_height * image_aspect_ratio)

game_board = pygame.transform.scale(game_board_image, (game_board_width, game_board_height))
game_board_x = int((available_width - game_board_width) / 2)
game_board_y = int((available_height - game_board_height) / 2)

board_x = available_width // 4
board_y = int((available_height - game_board_height) / 2)

window_open = True

# Dodatkowe zmienne dla menu wyboru ilości graczy
num_players = 0
selected_players = 2
font = pygame.font.Font(None, 36)
menu_options = [2, 3, 4]
menu_text = [font.render(str(option), True, (255, 255, 255)) for option in menu_options]
menu_rects = [text.get_rect(center=(available_width // 2, available_height // 2 + i * 50)) for i, text in
              enumerate(menu_text)]


class Pawn(pygame.sprite.Sprite):
    def __init__(self, image, px, py):
        super().__init__()
        self.image = pygame.transform.scale(image, (game_board_width // 20, game_board_height // 20))
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.movement_speed = 5

    def _handle_events(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.move_ip([-self.movement_speed, 0])
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.move_ip([self.movement_speed, 0])

    def update(self, keys_pressed):
        self._handle_events(keys_pressed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Funkcja do obsługi menu wyboru ilości graczy
def handle_menu():
    global num_players, selected_players
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(menu_rects):
                if rect.collidepoint(mouse_pos):
                    selected_players = menu_options[i]
                    num_players = selected_players
                    return


def draw_menu():
    screen.fill((255, 240, 220))
    button_color = (0, 255, 0)  # Zielony kolor przycisków
    text_color = (0, 0, 0)  # Kolor tekstu

    # Wyświetlanie tekstu "Wybierz ilość graczy"
    font = pygame.font.Font(None, 36)
    text = font.render("Wybierz ilość graczy", True, text_color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_width // 4))
    screen.blit(text, text_rect)

    for i, rect in enumerate(menu_rects):
        pygame.draw.rect(screen, button_color, rect)
        button_text = font.render(str(menu_options[i]), True, text_color)
        button_text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, button_text_rect)

    pygame.display.flip()



# Wywołanie funkcji menu wyboru ilości graczy
while num_players == 0:
    handle_menu()
    draw_menu()

# Inicjalizacja graczy
players = []
player_images = [IMAGES['GREENPAWN'], IMAGES['REDPAWN'], IMAGES['BLUEPAWN'], IMAGES['YELLOWPAWN']]
for i in range(num_players):
    player_image = player_images[i % len(player_images)]
    player = Pawn(player_image, int(game_board_width * 1.4) - i * 20, int(game_board_height * 0.9))
    players.append(player)

while window_open:
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False

    screen.fill((255, 240, 220))
    screen.blit(game_board, (board_x, board_y))
    for player in players:
        player.update(keys_pressed)
        player.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
