# TS_010/Source/game_over.py
import pygame


def show_game_over(screen, event):
    # フォントの設定
    font = pygame.font.Font(None, 72)

    # テキストの設定
    text = font.render("Game_over", True, (144, 238, 144))

    # テキストの位置
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height()/2))

    # 画面を薄い黄色に
    screen.fill((255, 255, 192))

    # テキストを描画
    screen.blit(text, text_rect)

    # スペースキーが押されたかどうかをチェック
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return True

    return False
