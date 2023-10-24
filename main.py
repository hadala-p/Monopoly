import pygame.mixer

from logic import GameRatio
from logic.BoardLogic import Board
from logic.MenuScreen import MenuScreen

pygame.init()
screen = GameRatio.screen
menuscreen = MenuScreen()
pygame.display.set_caption("Monopoly")
if __name__ == "__main__":
    menuscreen.start()
    game_board_start = Board(len(menuscreen.get_players_name()), menuscreen.get_players_name(),
                             menuscreen.get_selected_colors())
    game_board_start.start()
