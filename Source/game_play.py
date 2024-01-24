import pygame
import time
from back_ground import Background
from player_class import Player
from cloud import Cloud


class GamePlayScene:
    def __init__(self, screen):
        # 設定

        self.score = 0  # スコアの初期化
        self.score_multiplier = 1.0  # スコア乗算の初期化
        self.last_cloud_hit_time = 0  # 最後に雲を消した時間
        self.cloud_hit_streak = 0  # 連続して雲を消した回数
        self.streak_duration = 3  # ストリークの継続時間
        self.streak_points = 0  # ストリーク中に獲得したポイント
        self.last_score_update = time.time()  # 最後にスコアを更新した時間の初期化

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

        self.game_over = False  # ゲームオーバーフラグの初期化

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for cloud in self.clouds[:]:
                if cloud.is_clicked(mouse_pos):
                    self.clouds.remove(cloud)
                    current_time = time.time()
                    time_since_last_hit = current_time - self.last_cloud_hit_time

                    # ストリークのチェック
                    if time_since_last_hit <= self.streak_duration:
                        self.cloud_hit_streak += 1
                    else:
                        self.cloud_hit_streak = 1

                    # ストリーク時間に応じたスコア乗算率の設定
                    if time_since_last_hit <= 20:
                        score_multiplier = 1.5
                    elif time_since_last_hit <= 40:
                        score_multiplier = 2
                    elif time_since_last_hit <= 60:
                        score_multiplier = 5
                    else:
                        score_multiplier = 5  # 60秒以上は5倍のまま

                    self.last_cloud_hit_time = current_time
                    # ポイントの計算（ストリークと乗算率に応じて）
                    points = 10 * self.cloud_hit_streak * score_multiplier
                    # スコアにポイントを加算
                    self.score += points
                    break  # 1つのクリックで複数の雲は消せない
        elif event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                return 'score_screen'  # ゲームオーバーシーンに切り替える
            elif event.key == pygame.K_e:  # 'e'キーが押された場合
                self.player.health -= 5  # プレイヤーのHPを減らす

        # ゲームオーバーフラグが立っている場合はシーンを切り替える
        if self.game_over:
            return 'score_screen'

        return None

    def update(self):
        self.elapsed_time = time.time() - self.start_time  # 経過時間の更新

        # 雲の数値を更新
        self.update_cloud_parameters()

        # ゲームエリアの再計算
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()

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

        # ストリークが終了しているかどうかをチェック
        if time.time() - self.last_cloud_hit_time > self.streak_duration and self.streak_points > 0:
            # ストリーク終了時のポイントをスコアに加算し、ストリークポイントをリセット
            self.score += self.streak_points
            self.streak_points = 0

    # ゲームオーバーの条件をチェック
        if self.player.health <= 0:
            self.game_over = True  # ゲームオーバーフラグ

    def draw(self):
        # 画面サイズを取得
        screen_width, screen_height = self.screen.get_size()

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

        # スコアの描画
        debug_score = debug_font.render(
            f"Score: {int(self.score)}", True, (0, 0, 0))
        self.screen.blit(debug_score, (0, 50))  # スコアを画面に表示

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

        # ストリーク数とストリークの残り時間のデバッグ情報を追加
        streak_time_remaining = max(
            0, self.streak_duration - (time.time() - self.last_cloud_hit_time))
        debug_streak_info = debug_font.render(
            f"Streak: {self.cloud_hit_streak} (Time: {streak_time_remaining:.2f}s)", True, (255, 255, 0))
        self.screen.blit(debug_streak_info, (screen_width -
                         debug_streak_info.get_width(), screen_height - 105))

        # 次の雲が生成されるまでの残り時間のデバッグ情報を追加
        next_cloud_spawn_time_remaining = max(
            0, self.cloud_spawn_interval - (time.time() - self.cloud_spawn_time))
        debug_next_cloud_spawn_info = debug_font.render(
            f"Next Cloud: {next_cloud_spawn_time_remaining:.2f}s", True, (255, 255, 0))
        self.screen.blit(debug_next_cloud_spawn_info, (screen_width -
                         debug_next_cloud_spawn_info.get_width(), screen_height - 140))

        # 現在のスコアのデバッグ情報を追加
        debug_current_score_info = debug_font.render(
            f"Current Score: {int(self.score)}", True, (255, 255, 0))
        self.screen.blit(debug_current_score_info, (screen_width -
                         debug_current_score_info.get_width(), screen_height - 175))

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
                0.2, self.cloud_spawn_interval - 0.1)
            # 各雲のスピードを増やす（最大値は10）
            for cloud in self.clouds:
                cloud.speed_clouds = min(20, cloud.speed_clouds + 1)
            # 最後の更新時間を記録する
            self.last_cloud_update = int(self.elapsed_time) // 5
