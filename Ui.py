import pygame
from pygame import draw

import GameRatio
from Board import Fields
from Constants import BUY_BUTTON_RECT, FONT_SIZE, BACKGROUND_COLOR, BOARD_X, BOARD_Y, DICE_IMAGES, CHANCE_CARD_IMAGE, \
    CHANCE_CARD_IMAGE_2, CHEST_CARD_IMAGE, CHEST_CARD_IMAGE_2, GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT
from GameRatio import available_width, available_height, screen
from MenuScreen import clock

game_board = pygame.transform.scale(GameRatio.game_board_image, (GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT))


def draw_buy_button(field_name):
    draw.rect(screen, (0, 255, 0), BUY_BUTTON_RECT)
    buy_button_font = pygame.font.Font(None, FONT_SIZE // 2)
    buy_button_text = buy_button_font.render("Kup " + field_name, True, (255, 255, 255))
    buy_button_text_rect = buy_button_text.get_rect(center=BUY_BUTTON_RECT.center)
    screen.blit(buy_button_text, buy_button_text_rect)


def draw_game_board():
    screen.fill(BACKGROUND_COLOR)
    screen.blit(game_board, (BOARD_X, BOARD_Y))


def draw_message(code, field, font, players, current_player_index):
    global message, word_height
    if code == 1:
        message = (
        "Płacisz " + str(field.get_rent()) + "$ czynszu!")

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
        message = "Idziesz do więzienia!"
    elif code == 4:
        tax = field.get_tax()
        message = ("Płacisz" + str(tax) + "$ podatku")
    elif code == 6:
        message = "Gracz" + players[current_player_index - 1].get_name() + " bankrutuje!"
        message_text = font.render(message, True, (255, 0, 0))
        message_rect = message_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
        screen.blit(message_text, message_rect)
        pygame.time.wait(2000)
    elif code == 7:
        message = "Nie masz wystarczająco dużo Pieniędzy!"
    else:
        message = ""
    if code != 2 and code != 6:
        message_text = font.render(message, True, (0, 0, 0))
        message_rect = message_text.get_rect(center=(available_width * 0.5, available_width // 4 + 50))
        screen.blit(message_text, message_rect)


def animate_dice_roll(dice_1_dots, dice_2_dots, players):
    frames = 20  # Liczba klatek animacji
    delay = 20  # Opóźnienie między klatkami w milisekundach

    for i in range(frames):
        draw_game_board()
        for player in players:
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


def animate_card(players, current_player_index):
    field_type = players[current_player_index].get_current_point()
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
            draw_game_board()
            for player in players:
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


def draw_results(players):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE * 4)
    message = "Podsumowanie gry"
    message_text = font.render(message, True, (0, 0, 0))
    message_rect = message_text.get_rect(center=(available_width * 0.5, available_height * 0.1))
    screen.blit(message_text, message_rect)
    font = pygame.font.Font(None, FONT_SIZE * 2)
    space = 0.3
    for player in players:
        message = player.get_name() + "   " + str(player.get_score() + " pkt")
        message_text = font.render(message, True, (0, 0, 0))
        message_rect = message_text.get_rect(center=(available_width * 0.5, available_height * space))
        screen.blit(message_text, message_rect)
        space += 0.1


def draw_card(players, current_player_index):
    field_type = players[current_player_index].get_current_point()
    if field_type == 7 or field_type == 22 or field_type == 36:
        image = CHANCE_CARD_IMAGE_2
    else:
        image = CHEST_CARD_IMAGE_2
    card_image = pygame.transform.scale(image, ((GameRatio.get_width() * 30) // 80,
                                                GameRatio.get_height() // 2))
    card_rect = card_image.get_rect(center=(available_width // 2, available_height // 2))
    screen.blit(card_image, card_rect)


def draw_players_information(font, players, player_colors):
    proportion = 0.015
    temp = 0
    for player in players:
        current_player = player
        if current_player.is_bankrupt:
            current_player_text = font.render("gracz: " + str(current_player.name) + " - BANKRUT", True,
                                              player_colors[temp])
        else:
            current_player_text = font.render("gracz: " + str(current_player.name), True, player_colors[temp])
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


def draw_current_field_information(font, players, current_player_index):
    current_player = players[current_player_index]
    current_field = Fields[current_player.current_point]

    back_rect = pygame.Rect(available_width * 0.021, available_height * 0.35,
                            available_width * 0.22, available_height * 0.6)
    draw.rect(screen, (255, 255, 255), back_rect, 0, 20)
    back_rect = pygame.Rect(available_width * 0.03, available_height * 0.37,
                            available_width * 0.2, available_height * 0.56)
    draw.rect(screen, (0, 0, 0), back_rect, 3)
    back_rect = pygame.Rect(available_width * 0.021, available_height * 0.35,
                            available_width * 0.22, available_height * 0.6)
    draw.rect(screen, (0, 0, 0), back_rect, 3, 20)
    if current_field.get_type() == "estate":
        back_rect = pygame.Rect(available_width * 0.03, available_height * 0.37,
                                available_width * 0.2, available_height * 0.06)
        draw.rect(screen, current_field.get_color(), back_rect)
        rent_text = font.render("Rent: " + str(current_field.get_rent()), True, (0, 0, 0))
        rent_rect = rent_text.get_rect(center=(available_width // 8, available_height * 0.45))
        screen.blit(rent_text, rent_rect)
        for number in range(1, 5):
            rent_text = font.render("With " + str(number) + " house: " +
                                    str(current_field.get_rent_for_number_of_houses(number)), True, (0, 0, 0))
            rent_rect = rent_text.get_rect(center=(available_width // 8, available_height * (0.45 + 0.05 * number)))
            screen.blit(rent_text, rent_rect)
    field_title_font = pygame.font.Font(None, FONT_SIZE * 2)
    title_text = field_title_font.render(str(current_field.get_name()), True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(available_width // 8, available_height * 0.4))
    screen.blit(title_text, title_rect)
