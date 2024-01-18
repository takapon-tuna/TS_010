# TS_010/Source/game_play.py
import pygame
import time
from back_ground import draw_background  # 背景
from ball_class import Ball  # Ball


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       # self.image = pygame.image.load('player.png')
       # self.rect = self.image.get_rect()
        self.health = 30  # プレイヤーの体力を30に設定


def show_game_screen(screen, event):
    # フォントの設定
    font = pygame.font.Font(None, 72)

    # テキストの設定
    text = font.render("Game_play", True, (0, 0, 0))

    # テキストの位置
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height()/2))

    # プレイヤーを生成
    player = Player()

    # ゲーム開始時刻を記録
    start_time = time.time()

    elapsed_time = 0  # 経過時間を初期化

    # 背景を描画し、ゲームエリアのサイズを取得
    game_area_start, game_area_width, game_area_height = draw_background(
        screen, player.health, elapsed_time)

    # 白いボールを生成
    ball = Ball(game_area_start + game_area_width //
                2, game_area_height // 2, 5)

    # ゲームループ
    while True:
        # 経過時間を計算
        elapsed_time = time.time() - start_time

        # デバッグ用に時間を表示
        debug_font = pygame.font.Font(None, 36)  # フォントを設定
        debug_time = debug_font.render(
            f"Elapsed time: {elapsed_time:.2f}", True, (0, 0, 0))  # テキストを設定

        # デバッグ用にHPを表示
        debug_hp = debug_font.render(
            f"HP: {player.health}", True, (0, 0, 0))  # テキストを設定

        # 背景を描画し、ゲームエリアのサイズを取得
        game_area_start, game_area_width, game_area_height = draw_background(
            screen, player.health, elapsed_time)

        for event in pygame.event.get():
            # スペースキーが押されたかどうかをチェック
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                # 'e'キーが押された瞬間だけHPを5減らす
                elif event.key == pygame.K_e:
                    player.health -= 5
                # esc で終了
                elif event.key == pygame.K_ESCAPE:
                    return 'quit'

        # 現在押されているすべてのキーを取得し矢印キーを押したままにすると移動します。
        keys = pygame.key.get_pressed()

        ball.move(
            up=keys[pygame.K_UP],
            down=keys[pygame.K_DOWN],
            left=keys[pygame.K_LEFT],
            right=keys[pygame.K_RIGHT],
            game_area_start=game_area_start,
            game_area_width=game_area_width,
            game_area_height=game_area_height
        )

        # 白い球を描画
        ball.draw(screen)

        # デバッグテキストを描画
        screen.blit(debug_time, (0, 0))  # time
        screen.blit(debug_hp, (0, 20))  # HP

        # テキストを描画
        screen.blit(text, text_rect)

        pygame.display.flip()  # 画面を更新

    return False
