# TS_010/Source/main.py
import pygame
import pygame_gui
from title_screen import show_title_screen
from game_play import show_game_screen
from game_over import show_game_over
from score_screen import show_score_screen


def main():
    pygame.init()

    # 画面をフルスクリーンに設定
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # UIマネージャーの作成
    manager = pygame_gui.UIManager(pygame.display.get_surface().get_size())

    # ゲームの状態を管理する変数
    game_state = 'title'

    # クロックオブジェクトの作成
    clock = pygame.time.Clock()

    # ゲームループ
    while True:
        # 経過時間の計算
        time_delta = clock.tick(60)/1000.0

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # エスケープキーでゲーム終了
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            manager.process_events(event)

            # ゲームの状態に応じた処理
            if game_state == 'title':
                # タイトル画面の処理
                if show_title_screen(screen, event):
                    game_state = 'gameplay'
            elif game_state == 'gameplay':
                # ゲームプレイの処理
                if show_game_screen(screen, event):
                    game_state = 'game_over'
            elif game_state == 'game_over':
                # ゲームオーバーの処理
                if show_game_over(screen, event):
                    game_state = 'score_screen'
            elif game_state == 'score_screen':
                # スコア画面の処理
                if show_score_screen(screen, event):
                    game_state = 'title'

            manager.update(time_delta)

            manager.draw_ui(screen)

            pygame.display.update()


if __name__ == "__main__":
    main()
