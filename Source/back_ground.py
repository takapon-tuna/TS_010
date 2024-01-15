# TS_010/Source/back_ground.py
import pygame


def draw_background(screen):

    # 背景画像をロード
    bg_image = pygame.image.load('assets/bg/sky.png')

    # 画面に背景画像を描画
    screen.blit(bg_image, (0, 0))

    # 画面のサイズを取得
    screen_width, screen_height = screen.get_size()

    # 長方形のサイズを計算し、横幅を少し縮める
    rect_width = int(screen_width // 4 * 0.8)
    rect_height = int(screen_height)

    # 長方形の色を設定
    rect_color = (255, 224, 189)  # 薄い肌色

    # 左側の長方形を描画
    pygame.draw.rect(screen, rect_color, pygame.Rect(
        0, 0, rect_width, rect_height))

    # 右側の長方形を描画
    pygame.draw.rect(screen, rect_color, pygame.Rect(
        screen_width - rect_width, 0, rect_width, rect_height))
    # ゲーム操作部分のサイズを計算
    game_area_width = screen_width - 2 * rect_width
    game_area_height = screen_height

    return game_area_width, game_area_height
