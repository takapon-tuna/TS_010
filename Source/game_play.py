import pygame
import time
import random
from back_ground import Background
from ball_class import Ball
from player_class import Player
from cloud import Cloud


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
        # ゲームエリア内にのみ雲を配置
        self.clouds = [
            Cloud(
                random.randint(self.game_area_start,
                               self.game_area_start + self.game_area_width),
                random.randint(0, self.game_area_height // 2)
            ) for _ in range(5)
        ]
        self.add_cloud = False  # 新しい雲を追加するフラグの初期化

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # マウスでクリックされた位置を取得
            mouse_pos = pygame.mouse.get_pos()
            # クリックされた雲をリストから削除
            self.clouds = [
                cloud for cloud in self.clouds if not cloud.is_clicked(mouse_pos)]
        elif event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                return 'game_over'  # ゲームオーバーシーンに切り替える
            elif event.key == pygame.K_e:  # 'e'キーが押された場合
                self.player.health -= 5  # プレイヤーのHPを減らす
            elif event.key == pygame.K_r:  # 'r'キーが押された場合
                self.add_cloud = True  # 新しい雲を追加するフラグを立てる
        return None

    def update(self):
        self.elapsed_time = time.time() - self.start_time  # 経過時間の更新
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()  # ゲームエリアの再計算

        # 'r'キーが押された場合に新しい雲を追加
        if self.add_cloud:
            new_cloud = Cloud(
                random.randint(self.game_area_start,
                               self.game_area_start + self.game_area_width),
                random.randint(0, self.game_area_height)
            )
            self.clouds.append(new_cloud)
            self.add_cloud = False  # フラグをリセット

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
        self.background.draw(self.screen)  # 背景の描画
        # 雲の描画
        for cloud in self.clouds:
            cloud.draw(self.screen)
        # 左右の長方形描画
        self.background.draw_rectangles(self.screen)
        self.background.draw_ui(
            self.screen, self.player.health, self.elapsed_time)
        debug_font = pygame.font.Font(None, 36)  # デバッグ用のフォント設定
        debug_time = debug_font.render(
            f"Elapsed time: {self.elapsed_time:.2f}", True, (0, 0, 0))  # 経過時間の描画用テキスト
        debug_hp = debug_font.render(
            f"'e' HP: {self.player.health}", True, (0, 0, 0))  # HPの描画用テキスト
        debug_cloud = debug_font.render(
            f"'r' Cloud", True, (0, 0, 0))  # 雲を生成するボタン
        self.ball.draw(self.screen)  # ボールの描画
        self.screen.blit(debug_time, (0, 0))  # 経過時間の描画
        self.screen.blit(debug_hp, (0, 25))  # HPの描画
        self.screen.blit(debug_cloud, (0, 50))  # 雲のボタン

        pygame.display.flip()  # 画面更新
