import pygame
import time
from back_ground import Background
from ball_class import Ball
from player_class import Player


class GamePlayScene:
    def __init__(self, screen):
        self.screen = screen  # 画面オブジェクトの保存
        self.background = Background(screen)  # 背景オブジェクトの作成
        self.player = Player()  # プレイヤーオブジェクトの作成
        self.start_time = time.time()  # 開始時間の記録
        self.elapsed_time = 0  # 経過時間の初期化
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()  # ゲームエリアの計算
        self.ball = Ball(self.game_area_start + self.game_area_width //
                         2, self.game_area_height // 2, 5)  # ボールオブジェクトの作成

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                return 'game_over'  # ゲームオーバーシーンに切り替える
            elif event.key == pygame.K_e:  # 'e'キーが押された場合
                self.player.health -= 5  # プレイヤーのHPを減らす
            elif event.key == pygame.K_ESCAPE:  # ESCキーが押された場合
                return 'quit'  # ゲームを終了する
        return None

    def update(self):
        self.elapsed_time = time.time() - self.start_time  # 経過時間の更新
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()  # ゲームエリアの再計算

        # キーの長押しによるボールの移動処理をupdateメソッドに移動
        keys = pygame.key.get_pressed()
        self.ball.move(
            up=keys[pygame.K_UP],
            down=keys[pygame.K_DOWN],
            left=keys[pygame.K_LEFT],
            right=keys[pygame.K_RIGHT],
            game_area_start=self.game_area_start,
            game_area_width=self.game_area_width,
            game_area_height=self.game_area_height
        )

    def draw(self):
        self.background.draw(self.screen, self.player.health,
                             self.elapsed_time)  # 背景の描画
        debug_font = pygame.font.Font(None, 36)  # デバッグ用のフォント設定
        debug_time = debug_font.render(
            f"Elapsed time: {self.elapsed_time:.2f}", True, (0, 0, 0))  # 経過時間の描画用テキスト
        debug_hp = debug_font.render(
            f"'e' HP: {self.player.health}", True, (0, 0, 0))  # HPの描画用テキスト

        self.ball.draw(self.screen)  # ボールの描画
        self.screen.blit(debug_time, (0, 0))  # 経過時間の描画
        self.screen.blit(debug_hp, (0, 20))  # HPの描画

        pygame.display.flip()  # 画面更新
