import pygame
import time
from back_ground import Background
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

        self.clouds = [Cloud(self.screen.get_width(), self.screen.get_height(
        ), self.game_area_start, self.game_area_width, self.game_area_height) for _ in range(5)]

        # self.ball = Ball(self.game_area_start + self.game_area_width //
        #  2, self.game_area_height // 2, 5)  # ボールオブジェクトの作成
        self.cloud_spawn_time = 0

    # 雲の設定
        self.max_clouds = 20  # 雲の最大数
        self.cloud_spawn_interval = 2  # 何秒ごとに雲を生成

        self.last_cloud_update = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # マウスでクリックされた位置を取得
            mouse_pos = pygame.mouse.get_pos()
            # クリックされた雲をリストから削除
            self.clouds = [
                cloud for cloud in self.clouds if not cloud.is_clicked(mouse_pos)]
        elif event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                return 'score_screen'  # ゲームオーバーシーンに切り替える
            elif event.key == pygame.K_e:  # 'e'キーが押された場合
                self.player.health -= 5  # プレイヤーのHPを減らす
        return None

    def update(self):
        self.elapsed_time = time.time() - self.start_time  # 経過時間の更新

        # 雲の数値を更新
        self.update_cloud_parameters()

        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()  # ゲームエリアの再計算

        current_time = time.time()
        if len(self.clouds) < self.max_clouds and current_time - self.cloud_spawn_time > self.cloud_spawn_interval:
            # Cloud オブジェクトを生成する際に、ゲームエリアの情報を引数として渡す
            new_cloud = Cloud(
                self.screen.get_width(),
                self.screen.get_height(),
                self.game_area_start,
                self.game_area_width,
                self.game_area_height
            )
            self.clouds.append(new_cloud)
            self.cloud_spawn_time = current_time

        # 雲の更新
        for cloud in self.clouds:
            cloud.move()

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
        self.screen.blit(debug_time, (0, 0))  # 経過時間の描画
        self.screen.blit(debug_hp, (0, 25))  # HPの描画

        # 雲の数を取得
        cloud_count = len(self.clouds)
        # 雲の最大数
        max_cloud_count = self.max_clouds
        # 現在の雲のスピード（全雲の平均スピードを表示）
        average_speed = sum(
            cloud.speed_clouds for cloud in self.clouds) / cloud_count if cloud_count else 0

        # デバッグ情報のテキストを作成
        debug_cloud_count = debug_font.render(
            f"Clouds: {cloud_count}/{max_cloud_count}", True, (0, 255, 0))
        debug_speed = debug_font.render(
            f"Speed: {average_speed:.2f}", True, (0, 255, 0))

        # デバッグ情報を画面の右下に描画
        screen_width, screen_height = self.screen.get_size()
        self.screen.blit(debug_cloud_count, (screen_width -
                         debug_cloud_count.get_width(), screen_height - 70))
        self.screen.blit(debug_speed, (screen_width -
                         debug_speed.get_width(), screen_height - 35))

        pygame.display.flip()  # 画面更新

    def update_cloud_parameters(self):
       # 経過時間が5秒ごとに増加したかをチェック
        if int(self.elapsed_time) // 5 > self.last_cloud_update:
            # 雲の最大数を増やす (最大値は50)
            self.max_clouds = min(50, self.max_clouds + 1)
            # 雲の生成間隔を減らす（最小値は0.5秒）
            self.cloud_spawn_interval = max(
                0.5, self.cloud_spawn_interval - 0.1)
            # 各雲のスピードを増やす（最大値は10）
            for cloud in self.clouds:
                cloud.speed_clouds = min(10, cloud.speed_clouds + 1)
            # 最後の更新時間を記録する
            self.last_cloud_update = int(self.elapsed_time) // 5
