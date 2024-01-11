# TS_010/Source/main.py
import pygame
import pygame_gui
from pathlib import Path
from title_screen import show_title_screen
from game_play import show_game_screen


def main():
    pygame.init()

    # 画面の設定
    screen = pygame.display.set_mode((800, 600))

    # UIマネージャーの作成
    manager = pygame_gui.UIManager((800, 600))

    # プレイヤーの名前を保存/読み込むパス
    player_name_path = Path("P_name/player_name.txt")

    # ゲームの状態を管理する変数
    game_state = 'title'

    # クロックオブジェクトの作成
    clock = pygame.time.Clock()

    # テキストエントリーの初期化
    text_entry = None

    # ゲームループ
    while True:
        # 経過時間の計算
        time_delta = clock.tick(60)/1000.0

        # ゲームの状態に応じた処理
        if game_state == 'title':
            # タイトル画面の処理
            if show_title_screen(screen):
                # ファイルが存在するかチェック
                if not player_name_path.is_file():
                    # ファイルが存在しない場合、ダイアログを表示して入力を求める
                    dialog_window = pygame_gui.windows.UIMessageWindow(pygame.Rect((300, 250), (200, 100)),
                                                                       "name to input",
                                                                       manager)
                    text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((0, 0), (200, 50)),
                                                                     manager=manager,
                                                                     container=dialog_window)
                    text_entry.set_text('名前を入れて')
                else:
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

            # UIイベントの処理
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if text_entry is not None and event.ui_element == text_entry:
                        player_name = event.text
                        # 名前を保存
                        player_name_path.parent.mkdir(
                            parents=True, exist_ok=True)
                        with open(player_name_path, 'w') as file:
                            file.write(player_name)
                        game_state = 'gameplay'

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
