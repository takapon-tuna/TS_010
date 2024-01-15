# TS_010/Source/back_ground.py
import pygame


def draw_background(screen):

    # ”wŒi‰æ‘œ‚ğƒ[ƒh
    bg_image = pygame.image.load('assets/bg/sky.png')

    # ‰æ–Ê‚É”wŒi‰æ‘œ‚ğ•`‰æ
    screen.blit(bg_image, (0, 0))
