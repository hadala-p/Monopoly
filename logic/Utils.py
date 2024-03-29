import pygame

from Constants import BOARD_X, GAME_BOARD_WIDTH, BOARD_Y, GAME_BOARD_HEIGHT, PAWN_SIZE
from data.Chance import Chance
from data.CommunityChest import CommunityChest
from data.Estate import Estate
from data.Field import Field
from data.IncomeTax import IncomeTax
from data.RailRoad import RailRoad

clock = pygame.time.Clock()


def sprawdz_typ_pola(indeks_pola):
    return Fields[indeks_pola].type


Fields = [
    Field("Start", BOARD_X + (GAME_BOARD_WIDTH * 0.9), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "start"),
    Estate("Białystok", BOARD_X + (GAME_BOARD_WIDTH * 0.8), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "estate",
           60, (55, 76, 95)),
    CommunityChest("Skrzynia", BOARD_X + (GAME_BOARD_WIDTH * 0.73), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1],
                   "chance"),
    Estate("Bełchatów", BOARD_X + (GAME_BOARD_WIDTH * 0.64), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "estate",
           60, (55, 76, 95)),
    IncomeTax("Podatek", BOARD_X + (GAME_BOARD_WIDTH * 0.56), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "tax", 200),
    RailRoad("Pociąg Regio", BOARD_X + (GAME_BOARD_WIDTH * 0.48), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1],
             "kolejka", 50),
    Estate("Lublin", BOARD_X + (GAME_BOARD_WIDTH * 0.4), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "estate",
           100, (190, 202, 218)),
    Chance("Szansa", BOARD_X + (GAME_BOARD_WIDTH * 0.32), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "chance"),
    Estate("Katowice", BOARD_X + (GAME_BOARD_WIDTH * 0.25), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "estate", 100,
           (190, 202, 218)),
    Estate("Kraków", BOARD_X + (GAME_BOARD_WIDTH * 0.17), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "estate", 120,
           (190, 202, 218)),
    Field("Wiezienie", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + GAME_BOARD_HEIGHT - PAWN_SIZE[1], "jail"),
    Estate("Toruń", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.8), "estate", 140,
           (162, 68, 118)),
    IncomeTax("Podatek", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.7), "tax", 150),
    Estate("Elbląg", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.65), "estate", 140,
           (162, 68, 118)),
    Estate("Szczecin", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.55), "estate", 160,
           (162, 68, 118)),
    RailRoad("Kolejka linowa", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.46), "kolejka",
             100),
    Estate("Bydgoszcz", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.38), "estate", 180,
           (247, 154, 41)),
    CommunityChest("Skrzynia", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.3),
                   "chance"),
    Estate("Tarnów", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.22), "estate", 180,
           (247, 154, 41)),
    Estate("Wrocław", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.15), "estate", 200,
           (247, 154, 41)),
    Field("Darmowy Parking", BOARD_X + (GAME_BOARD_WIDTH * 0.05), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "parking"),
    Estate("Kalisz", BOARD_X + (GAME_BOARD_WIDTH * 0.17), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 220,
           (253, 0, 0)),
    Chance("Szansa", BOARD_X + (GAME_BOARD_WIDTH * 0.25), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "chance"),
    Estate("Gdynia", BOARD_X + (GAME_BOARD_WIDTH * 0.32), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 220,
           (253, 0, 0)),
    Estate("Poznań", BOARD_X + (GAME_BOARD_WIDTH * 0.4), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 240,
           (253, 0, 0)),
    RailRoad("Metro", BOARD_X + (GAME_BOARD_WIDTH * 0.48), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "kolejka", 150),
    Estate("Opole", BOARD_X + (GAME_BOARD_WIDTH * 0.56), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 260,
           (255, 255, 1)),
    Estate("Katowice", BOARD_X + (GAME_BOARD_WIDTH * 0.64), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 260,
           (255, 255, 1)),
    IncomeTax("Podatek", BOARD_X + (GAME_BOARD_WIDTH * 0.73), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "tax", 150),
    Estate("Rzeszów", BOARD_X + (GAME_BOARD_WIDTH * 0.8), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "estate", 280,
           (255, 255, 1)),
    Field("Więzienie", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.03), "go_to_jail"),
    Estate("Gdańsk", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.15), "estate", 300,
           (0, 136, 54)),
    Estate("Gliwice", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.22), "estate", 300,
           (0, 136, 54)),
    CommunityChest("Skrzynia", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.3),
                   "chance"),
    Estate("Kielce", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.38), "estate", 320,
           (0, 136, 54)),
    RailRoad("Tramwaj", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.46), "kolejka", 200),
    Chance("Szansa", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.55), "chance"),
    Estate("Olsztyn", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.65), "estate", 350,
           (78, 102, 172)),
    IncomeTax("Podatek", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.7), "tax", 150),
    Estate("Warszawa", BOARD_X + (GAME_BOARD_WIDTH * 0.93), BOARD_Y + (GAME_BOARD_HEIGHT * 0.8), "estate", 400,
           (78, 102, 172)),
]
