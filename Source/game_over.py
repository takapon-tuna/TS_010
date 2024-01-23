import pygame


class GameOverScene:
    def __init__(self, screen):

        self.screen = screen
        screen_width, screen_height = self.screen.get_size()
    # 画像の読み込み
        self.gameover_purple_ori = pygame.image.load(
            'assets/game_overe/gameover_purple.png')  # 紫のゲームオーバー
        self.gameover_yellow_ori = pygame.image.load(
            'assets/game_overe/gameover_yellow.png')  # 黄のゲームオーバー
        self.game_purple_ori = pygame.image.load(
            'assets/game_overe/game_purple.png')  # 紫のゲーム
        self.game_yellow_ori = pygame.image.load(
            'assets/game_overe/game_yellow.png')  # 黄のゲーム
        self.over_purple_ori = pygame.image.load(
            'assets/game_overe/over_purple.png')  # 紫のオーバー
        self.over_yellow_ori = pygame.image.load(
            'assets/game_overe/over_yellow.png')  # 黄のオーバー

    # 画像のスケーリング
        scale_factor = 0.6
        # ゲームオーバー
        self.gameover_purple_scaled = pygame.transform.scale(
            self.gameover_purple_ori, (int(self.gameover_purple_ori.get_width() * scale_factor), int(self.gameover_purple_ori.get_height() * scale_factor)))
        self.gameover_yellow_scaled = pygame.transform.scale(
            self.gameover_yellow_ori, (int(self.gameover_yellow_ori.get_width() * scale_factor), int(self.gameover_yellow_ori.get_height() * scale_factor)))
        # ゲーム
        self.game_purple = pygame.transform.scale(
            self.game_purple_ori, (int(self.game_purple_ori.get_width() * scale_factor), int(self.game_purple_ori.get_height() * scale_factor)))
        self.game_yellow = pygame.transform.scale(
            self.game_yellow_ori, (int(self.game_yellow_ori.get_width() * scale_factor), int(self.game_yellow_ori.get_height() * scale_factor)))
        # オーバー
        self.over_purple = pygame.transform.scale(
            self.over_purple_ori, (int(self.over_purple_ori.get_width() * scale_factor), int(self.over_purple_ori.get_height() * scale_factor)))
        self.over_yellow = pygame.transform.scale(
            self.over_yellow_ori, (int(self.over_yellow_ori.get_width() * scale_factor), int(self.over_yellow_ori.get_height()*scale_factor)))

    # 設定
        self.toggle_time = 1000  # 画像を一秒ごとに切り替え
        self.last_toggle = pygame.time.get_ticks()  # 最後に画像を切り替えた時刻
        self.current_image = 'purple'  # 現在表示している画像

        # ゲームオーバー画像の位置を中央よりさらに上に設定
        vertical_offset = 150  # 上にずらす量を指定
        self.gameover_purple_rect = self.gameover_purple_scaled.get_rect(
            center=(screen_width / 2, (screen_height / 2) - vertical_offset))
        self.gameover_purple_rect.top -= self.gameover_purple_scaled.get_height() / 2
        self.gameover_yellow_rect = self.gameover_yellow_scaled.get_rect(
            center=(screen_width / 2, (screen_height / 2) - vertical_offset))
        self.gameover_yellow_rect.top -= self.gameover_yellow_scaled.get_height() / 2

    # フォントの設定
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render(
            "Game_over", True, (144, 238, 144))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))  # テキストの位置

        self.prompt_text = "press to space"
        self.prompt_font = pygame.font.Font(None, 160)
        self.prompt_color = (255, 255, 255)  # 白色
        self.background_color = (255, 255, 255)  # 白色
        self.background_alpha = 128  # 半透明

        self.angle = 0  # 画像の角度
        self.angle_direction = 1  # 角度の変化方向
        self.angle_change_rate = 0.1  # 角度の変化率をもっと遅くする
        self.max_angle = 5  # 最大傾き角度

        self.original_center = self.gameover_purple_rect.center  # 元の中心位置を保存
        self.move_direction = 1  # 移動方向
        self.move_rate = 10  # 移動速度
        self.move_distance = 500  # 左右に動く距離

    def handle_event(self, event):
        # スペースキーが押されたかどうかをチェック
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'score_screen'
        return None

    def update(self):
        # 現在の時刻を取得
        current_time = pygame.time.get_ticks()
        # 最後に画像を切り替えてから1秒以上経過しているか確認
        if current_time - self.last_toggle > self.toggle_time:
            # 画像を切り替える
            self.current_image = 'yellow' if self.current_image == 'purple' else 'purple'
            # 最後の切り替え時刻を更新
            self.last_toggle = current_time

       # 画像を左右に動かす
        self.gameover_purple_rect.centerx += self.move_direction * self.move_rate
        self.gameover_yellow_rect.centerx += self.move_direction * self.move_rate
        # 移動限界を超えたら方向転換
        if abs(self.gameover_purple_rect.centerx - self.original_center[0]) >= self.move_distance:
            self.move_direction *= -1

        # 角度を更新
        self.angle += self.angle_direction * self.angle_change_rate
        if abs(self.angle) >= self.max_angle:
            self.angle_direction *= -1

        # オリジナルの画像を回転させる
        self.gameover_purple = pygame.transform.rotate(
            self.gameover_purple_scaled, self.angle)
        self.gameover_yellow = pygame.transform.rotate(
            self.gameover_yellow_scaled, self.angle)

        # 回転後の画像の中心が元の位置と同じになるようにrectを更新
        self.gameover_purple_rect = self.gameover_purple.get_rect(
            center=self.original_center)
        self.gameover_yellow_rect = self.gameover_yellow.get_rect(
            center=self.original_center)

    def draw(self):
        self.screen.fill((0, 0, 0))  # 画面を黒に
        # 現在の画像に応じて描画する画像を切り替え
        if self.current_image == 'purple':
            self.screen.blit(self.gameover_purple, self.gameover_purple_rect)
        else:
            self.screen.blit(self.gameover_yellow, self.gameover_yellow_rect)

        # 長方形の背景の Surface を作成
        prompt_surface = self.prompt_font.render(
            self.prompt_text, True, self.prompt_color)
        prompt_rect = prompt_surface.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() - 150))

        background_surface = pygame.Surface(
            (self.screen.get_width(), prompt_surface.get_height()))
        background_surface.set_alpha(self.background_alpha)  # 透明度を半透明に設定
        background_surface.fill(self.background_color)  # 背景色を設定
        background_rect = background_surface.get_rect(
            topleft=(0, prompt_rect.top))  # 長方形の位置を設定

        # 長方形の背景とテキストを描画
        self.screen.blit(background_surface, background_rect)
        self.screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()  # 画面更新
