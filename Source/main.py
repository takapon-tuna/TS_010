# TS_010/Source/main.py
import pygame
from title_screen import show_title_screen  # title_screen.pyから関数をインポート
from game_play import show_game_screen


def main():
    pygame.init()

    # 画面の設定
    screen = pygame.display.set_mode((800, 600))

    # ゲームの状態を管理する変数
    game_state = 'title'

    # ゲームループ
    while True:
        # ゲームの状態に応じた処理
        if game_state == 'title':
            # タイトル画面の処理
            if show_title_screen(screen):
                game_state = 'gameplay'
        elif game_state == 'gameplay':
            # ゲームプレイの処理
            show_game_screen(screen)
        elif game_state == 'game_over':
            # ゲームオーバーの処理
            pass
        elif game_state == 'score_screen':
            # スコア画面の処理
            pass

        pygame.display.flip()

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    main()
