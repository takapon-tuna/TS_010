# TS_010/Source/game_play.py
import pygame


def show_game_screen(screen):
    # フォントの設定
    font = pygame.font.Font(None, 72)

    # テキストの設定
    text = font.render("Game", True, (144, 238, 144))

    # テキストの位置
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height()/2))

    # 画面を黒に
    screen.fill((0, 0, 0))

    # テキストを描画
    screen.blit(text, text_rect)

    # 画面を更新
    pygame.display.flip()

    # スペースキーが押されたかどうかをチェック
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True

    return False
