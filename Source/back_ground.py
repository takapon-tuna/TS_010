# TS_010/Source/back_ground.py
import pygame


def draw_background(screen):

    # �w�i�摜�����[�h
    bg_image = pygame.image.load('assets/bg/sky.png')

    # ��ʂɔw�i�摜��`��
    screen.blit(bg_image, (0, 0))
