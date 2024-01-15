# TS_010/Source/game_play.py
import pygame
from back_ground import draw_background  # 背景


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.health = 30  # プレイヤーの体力を30に設定


def show_game_screen(screen, event):
    # フォントの設定
    font = pygame.font.Font(None, 72)

    # テキストの設定
    text = font.render("Game_play", True, (0, 0, 0))

    # テキストの位置
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height()/2))

    # 背景を描画し、ゲームエリアのサイズを取得
    game_area_width, game_area_height = draw_background(screen)

    # テキストを描画
    screen.blit(text, text_rect)

    # スペースキーが押されたかどうかをチェック
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return True

    return False
