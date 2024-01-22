import pygame
import math

# タイトルシーンクラス


class TitleScene:
    def __init__(self, screen):
        self.screen = screen
        screen_width, screen_height = self.screen.get_size()
        # 画像をロード
        self.background_original = pygame.image.load(
            'assets/ui/titlescreen.png')  # 背景をロード
        self.background = pygame.transform.scale(
            self.background_original, (screen_width, screen_height))
        self.bg_start = pygame.image.load('assets/ui/start.png')
        self.bg_start_af = pygame.image.load('assets/ui/g.png')  # マウスオーバー用の画像
        self.bg_exit = pygame.image.load('assets/ui/exit.png')
        self.bg_exit_af = pygame.image.load(
            'assets/ui/g_sad.png')  # マウスオーバー用の画像
        self.font = pygame.font.Font(None, 72)  # フォントの設定
        self.text = self.font.render("Title", True, (255, 255, 255))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))  # テキストの位置
        # ボタンの位置を中央に設定
        self.start_button_pos = (
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 250)
        self.exit_button_pos = (
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 380)
        self.start_button_rect = self.bg_start.get_rect(
            center=self.start_button_pos)
        self.exit_button_rect = self.bg_exit.get_rect(
            center=self.exit_button_pos)
        # アニメーション用の時間変数
        self.time_start = 0
        self.time_exit = 0.8  # exitのアニメーションを少し遅らせる

    # イベント処理
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # マウスボタンが押された場合
            # スタートボタンがクリックされた場合
            if self.start_button_rect.collidepoint(event.pos):
                return 'game_play'  # ゲームプレイシーンに切り替える
            # 終了ボタンがクリックされた場合
            elif self.exit_button_rect.collidepoint(event.pos):
                return 'quit'  # ゲームを終了する
        return None

    # 更新処理
    def update(self):
        # ふわふわ動くアニメーションの速度を増加
        self.time_start += 0.05  # 速度を2倍にする
        self.time_exit += 0.06  # 速度を2倍にする
        offset_start_y = math.sin(self.time_start) * 10  # 上下のオフセット
        offset_start_x = math.cos(self.time_start) * 10  # 左右のオフセット
        offset_exit_y = math.sin(self.time_exit) * -10    # 上下のオフセット
        offset_exit_x = math.cos(self.time_exit) * -10    # 左右のオフセット

        # ボタンの位置を更新
        self.start_button_rect.center = (
            self.start_button_pos[0] + offset_start_x, self.start_button_pos[1] + offset_start_y)
        self.exit_button_rect.center = (
            self.exit_button_pos[0] + offset_exit_x, self.exit_button_pos[1] + offset_exit_y)

        # マウスの位置を取得し、画像を更新
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button_rect.collidepoint(mouse_pos):
            self.bg_start = self.bg_start_af
        else:
            self.bg_start = pygame.image.load('assets/ui/start.png')

        if self.exit_button_rect.collidepoint(mouse_pos):
            self.bg_exit = self.bg_exit_af
        else:
            self.bg_exit = pygame.image.load('assets/ui/exit.png')

    # 描画処理
    def draw(self):
        self.screen.blit(self.background, (0, 0))  # 背景描画
        self.screen.blit(self.bg_start, self.start_button_rect)  # スタートボタン描画
        self.screen.blit(self.bg_exit, self.exit_button_rect)  # 終了ボタン描画
        pygame.display.flip()  # 画面更新
