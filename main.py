import pygame.mixer

import GameRatio
from Board import Board
from MenuScreen import MenuScreen

pygame.init()
screen = GameRatio.screen
menuscreen = MenuScreen()
pygame.display.set_caption("Monopoly")
if __name__ == "__main__":
    menuscreen.start()
    game_board_start = Board(len(menuscreen.get_players_name()), menuscreen.get_players_name(),
                             menuscreen.get_selected_colors())
    game_board_start = Board(2, ["Piotr", "Angelika"], [(0, 255, 0), (255, 0, 0)])
    game_board_start.start()
