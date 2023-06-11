from turtledemo import clock

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, name, px, py, pawn_size):
        super().__init__()
        self.image = pygame.transform.scale(image, pawn_size)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.current_point = 0
        self.money = 3000
        self.properties = []
        self.in_jail = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def get_name(self):
        return self.name

    def get_current_point(self):
        return self.current_point

    def set_current_point(self, new_point):
        self.current_point = new_point

    def add_money(self, money):
        self.money += money

    def subtract_money(self, money):
        self.money -= money

    def get_money(self):
        return self.money

    def add_property(self, field):
        self.properties.append(field)

    def pay_rent(self, rent):
        self.money -= rent

    def jail_status(self, status):
        self.in_jail = status
