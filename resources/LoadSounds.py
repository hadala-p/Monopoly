import pygame


def play_sound(temp):
    sound = pygame.mixer.Sound(f'sounds/{temp}.mp3')
    sound.play()


