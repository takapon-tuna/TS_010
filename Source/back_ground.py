import pygame


class Background:
    def __init__(self, screen):
        # 画像をロード
        self.bg_image = pygame.image.load('assets/bg/sky.png')
        self.hp_g_normal_image = pygame.image.load('assets/ui/g.png')
        self.hp_g_high_image = pygame.image.load('assets/ui/g_happy.png')
        self.hp_g_low_image = pygame.image.load('assets/ui/g_sad.png')
        self.g_benchi_summer_image = pygame.image.load('assets/ui/summer.png')
        self.g_benchi_autumn_image = pygame.image.load('assets/ui/autumn.png')
        self.g_benchi_winter_image = pygame.image.load('assets/ui/winter.png')
        self.g_benchi_spring_image = pygame.image.load('assets/ui/spring.png')

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

        # じじい(HP)のサイズを変更
        self.g_image_normal_scaled = pygame.transform.scale(
            self.hp_g_normal_image, (self.hp_normal_width, self.hp_normal_height))
        self.g_image_high_scaled = pygame.transform.scale(
            self.hp_g_high_image, (self.hp_high_width, self.hp_high_height))
        self.g_image_low_scaled = pygame.transform.scale(
            self.hp_g_low_image, (self.hp_low_width, self.hp_low_height))

       # じじい(ベンチ)のサイズを変更
        bench_scale_factor = self.rect_width / self.bc_summer_width  # 横を長方形に合わせる比率
        self.g_benchi_summer_scaled = pygame.transform.scale(
            self.g_benchi_summer_image, (self.rect_width, int(self.bc_summer_height * bench_scale_factor)))
        self.g_benchi_autumn_scaled = pygame.transform.scale(
            self.g_benchi_autumn_image, (self.rect_width, int(self.bc_summer_height * bench_scale_factor)))
        self.g_benchi_winter_scaled = pygame.transform.scale(
            self.g_benchi_winter_image, (self.rect_width, int(self.bc_summer_height * bench_scale_factor)))
        self.g_benchi_spring_scaled = pygame.transform.scale(
            self.g_benchi_spring_image, (self.rect_width, int(self.bc_summer_height * bench_scale_factor)))

    def get_right_rectangle_width(self):
        return self.rect_width

    def calculate_game_area(self):

        # ゲーム操作部分の開始位置とサイズを計算
        game_area_start = self.rect_width
        game_area_width = self.screen_width - 2 * self.rect_width
        game_area_height = self.screen_height

        return game_area_start, game_area_width, game_area_height

    def draw(self, screen):

        # 画面に背景画像を描画
        screen.blit(self.bg_image, (0, 0))

    def draw_rectangles(self, screen):
        # 長方形の色を設定
        rect_color = (255, 224, 189)  # 薄い肌色

        # 左側の長方形を描画
        pygame.draw.rect(screen, rect_color, pygame.Rect(
            0, 0, self.rect_width, self.rect_height))

        # 右側の長方形を描画
        pygame.draw.rect(screen, rect_color, pygame.Rect(
            self.screen_width - self.rect_width, 0, self.rect_width, self.rect_height))

    def draw_ui(self, screen, hp, time_elapsed):
        # じじい表示
        # HPに応じて左上の画像を切り替え
        if hp > 20:  # HPが21以上の場合
            # 長方形の幅に合わせ、縦は画面半分の上側にエフェクトを追加
            effect_rect = pygame.Surface(
                (self.rect_width, self.screen_height // 2 - 100), pygame.SRCALPHA)
            effect_rect.fill((50, 205, 50, 128))  # ライムグリーンの半透明のエフェクト
            screen.blit(effect_rect, (0, 0))  # 上端から描画
            screen.blit(self.g_image_high_scaled, (self.rect_width // 4, 50))
        elif hp > 10:  # HPが11以上の場合
            # 長方形の幅に合わせ、縦は画面半分の上側にエフェクトを追加
            effect_rect = pygame.Surface(
                (self.rect_width, self.screen_height // 2 - 100), pygame.SRCALPHA)
            effect_rect.fill((255, 255, 0, 128))  # 黄色の半透明のエフェクト
            screen.blit(effect_rect, (0, 0))  # 上端から描画
            screen.blit(self.g_image_normal_scaled, (self.rect_width // 4, 50))
        else:  # HPが10以下の場合
            # 長方形の幅に合わせ、縦は画面半分の上側にエフェクトを追加
            effect_rect = pygame.Surface(
                (self.rect_width, self.screen_height // 2 - 100), pygame.SRCALPHA)
            effect_rect.fill((255, 0, 0, 128))  # 赤い半透明のエフェクト
            screen.blit(effect_rect, (0, 0))  # 上端から描画
            screen.blit(self.g_image_low_scaled, (self.rect_width // 4, 50))

        # 時間に応じてベンチの画像を切り替え
        # 経過時間を10秒ごとのインデックスに変換し、画像リストのインデックスとして使用
        bench_image_list = [self.g_benchi_summer_scaled, self.g_benchi_autumn_scaled,
                            self.g_benchi_winter_scaled, self.g_benchi_spring_scaled]
        image_index = int(time_elapsed // 10) % len(bench_image_list)
        # 選択された画像を描画
        screen.blit(bench_image_list[image_index],
                    (1, self.rect_height // 2 + 50))
