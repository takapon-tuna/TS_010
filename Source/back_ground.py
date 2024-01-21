import pygame


class Background:
    def __init__(self, screen):
        # 画像をロード
        self.bg_image = pygame.image.load('assets/bg/sky.png')
        self.hp_g_normal_image = pygame.image.load('assets/ui/g.png')
        self.hp_g_high_image = pygame.image.load('assets/ui/g_happy.png')
        self.hp_g_low_image = pygame.image.load('assets/ui/g_sad.png')
        self.g_benchi_summer_image = pygame.image.load(
            'assets/ui/g_benchi.png')

        # 画像のサイズを取得
        self.hp_normal_width, self.hp_normal_height = self.hp_g_normal_image.get_size()
        self.hp_high_width, self.hp_high_height = self.hp_g_high_image.get_size()
        self.hp_low_width, self.hp_low_height = self.hp_g_low_image.get_size()
        self.bc_summer_width, self.bc_summer_height = self.g_benchi_summer_image.get_size()

        # 画面のサイズを取得
        self.screen_width, self.screen_height = screen.get_size()

        # 長方形のサイズを計算し、横幅を少し縮める
        self.rect_width = int(self.screen_width // 4 * 0.8)
        self.rect_height = int(self.screen_height)

    def calculate_game_area(self):

        # ゲーム操作部分の開始位置とサイズを計算
        game_area_start = self.rect_width
        game_area_width = self.screen_width - 2 * self.rect_width
        game_area_height = self.screen_height

        return game_area_start, game_area_width, game_area_height

    def draw(self, screen, hp, time_elapsed):
        # じじい(HP)のサイズを変更
        g_image_normal_scaled = pygame.transform.scale(
            self.hp_g_normal_image, (self.hp_normal_width, self.hp_normal_height))
        g_image_high_scaled = pygame.transform.scale(
            self.hp_g_high_image, (self.hp_high_width, self.hp_high_height))
        g_image_low_scaled = pygame.transform.scale(
            self.hp_g_low_image, (self.hp_low_width, self.hp_low_height))

        # じじい(ベンチ)のサイズを0.8倍に変更
        g_benchi_summer_scaled = pygame.transform.scale(
            self.g_benchi_summer_image, (int(self.bc_summer_width * 0.8), int(self.bc_summer_height * 0.8)))

        # 画面に背景画像を描画
        screen.blit(self.bg_image, (0, 0))

        # 長方形の色を設定
        rect_color = (255, 224, 189)  # 薄い肌色

        # 左側の長方形を描画
        pygame.draw.rect(screen, rect_color, pygame.Rect(
            0, 0, self.rect_width, self.rect_height))

        # HPに応じて左上の画像を切り替え
        if hp > 20:  # HPが21以上の場合
            screen.blit(g_image_high_scaled, (self.rect_width // 4, 50))
        elif hp > 10:  # HPが11以上の場合
            screen.blit(g_image_normal_scaled, (self.rect_width // 4, 50))
        else:  # HPが10以下の場合
            screen.blit(g_image_low_scaled, (self.rect_width // 4, 50))

        # 時間が０秒以上なら表示し続ける
        if time_elapsed >= 0:
            screen.blit(g_benchi_summer_scaled,
                        (1, self.rect_height // 2 + 50))

        # 右側の長方形を描画
        pygame.draw.rect(screen, rect_color, pygame.Rect(
            self.screen_width - self.rect_width, 0, self.rect_width, self.rect_height))
