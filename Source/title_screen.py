import pygame
import math
import json
from cryptography.fernet import Fernet


# タイトルシーンクラス


class TitleScene:
    def __init__(self, screen, firebase, auth):
        self.screen = screen
        self.firebase = firebase
        self.auth = auth
        screen_width, screen_height = self.screen.get_size()

        # BGMの初期化と再生
        pygame.mixer.init()
        pygame.mixer.music.load('assets/bgm/title_2.mp3')
        pygame.mixer.music.play(-1)

        # SEのロード
        self.start_sound = pygame.mixer.Sound('assets/se/start.mp3')

    # 画像をロード
        self.background_original = pygame.image.load(
            'assets/ui/titlescreen.png')  # 背景をロード
        self.bg_start = pygame.image.load('assets/ui/start.png')  # スタートをロード
        self.bg_start_af = pygame.image.load(
            'assets/ui/start_af.png')  # マウスオーバー用の画像
        self.bg_exit = pygame.image.load('assets/ui/exit.png')  # exitをロード
        self.bg_exit_af = pygame.image.load(
            'assets/ui/exit_af.png')  # マウスオーバー用の画像
        self.bg_title_ori = pygame.image.load(
            'assets/ui/title.png')  # タイトルをロード
        self.bg_benchi_ori = pygame.image.load(
            'assets/ui/benchi.png')  # ベンチのみロード
        self.bg_g_title_ori = pygame.image.load(
            'assets/ui/g_title.png')  # タイトル用じじい

    # スケーリング
        scale_factor = 0.8

        self.background = pygame.transform.scale(
            self.background_original, (screen_width, screen_height))  # 背景のスケーリング
        self.bg_title = pygame.transform.scale(
            self.bg_title_ori, (int(self.bg_title_ori.get_width() * scale_factor), int(self.bg_title_ori.get_height() * scale_factor)))  # タイトルのスケーリング
        self.bg_benchi = pygame.transform.scale(
            self.bg_benchi_ori, (int(self.bg_benchi_ori.get_width() * scale_factor), int(self.bg_benchi_ori.get_height() * scale_factor)))  # ベンチのスケーリング
        self.bg_g_title = pygame.transform.scale(
            self.bg_g_title_ori, (int(self.bg_g_title_ori.get_width() * scale_factor), int(self.bg_g_title_ori.get_height() * scale_factor)))  # じじいスケーリング

    # 設定

        self.font = pygame.font.Font(None, 72)  # フォントの設定
        self.text = self.font.render("Title", True, (255, 255, 255))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))  # テキストの位置
        # ボタンの位置を中央に設定
        self.start_button_pos = (
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 210)
        self.exit_button_pos = (
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 210 + 130)
        self.start_button_rect = self.bg_start.get_rect(
            center=self.start_button_pos)
        self.exit_button_rect = self.bg_exit.get_rect(
            center=self.exit_button_pos)
        # アニメーション用の時間変数
        self.time_start = 0
        self.time_exit = 0.8  # exitのアニメーションを少し遅らせる

        # タイトル画像の位置を中央に設定
        self.bg_title_rect = self.bg_title.get_rect(
            center=(screen_width / 2, screen_height / 2 - 100))

        # ベンチ画像の位置を左下に設定
        self.bg_benchi_rect = self.bg_benchi.get_rect(
            bottomleft=(0, screen_height))

        # タイトル用じじい画像の位置を右下に設定
        self.bg_g_title_rect = self.bg_g_title.get_rect(
            bottomright=(screen_width, screen_height))

        # タイトルアニメーション用の時間変数
        self.time_title = 0

    # イベント処理
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.start_sound.play()  # 効果音
                player_name = self.load_player_name()
                if player_name:  # 名前が存在する場合
                    return 'game_play'  # ゲームプレイシーンに切り替える
                else:  # 名前が存在しない場合
                    return 'name_input'  # 名前入力シーンに切り替える
            elif self.exit_button_rect.collidepoint(event.pos):
                self.start_sound.play()  # 効果音
                player_name = self.load_player_name()
                return 'quit'  # ゲームを終了する
        return None

    # 更新処理
    def update(self):
        # ふわふわ動くアニメーションの速度を増加
        self.time_start += 0.05
        self.time_exit += 0.06
        offset_start_y = math.sin(self.time_start) * 10  # 上下のオフセット
        offset_start_x = math.cos(self.time_start) * 10  # 左右のオフセット
        offset_exit_y = math.sin(self.time_exit) * -10    # 上下のオフセット
        offset_exit_x = math.cos(self.time_exit) * -10    # 左右のオフセット

        # ボタンの位置を更新
        self.start_button_rect.center = (
            self.start_button_pos[0] + offset_start_x, self.start_button_pos[1] + offset_start_y)
        self.exit_button_rect.center = (
            self.exit_button_pos[0] + offset_exit_x, self.exit_button_pos[1] + offset_exit_y)

        # タイトルアニメーションの速度を増加
        self.time_title += 0.03
        offset_title_y = math.sin(self.time_title) * 10  # 上下のオフセット

        # タイトル画像の位置を更新
        self.bg_title_rect.centery = (
            self.screen.get_height() / 2 - 100 + offset_title_y)

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

        # タイトル画像の描画
        self.screen.blit(self.bg_title, self.bg_title_rect)

        # ベンチ画像の描画
        self.screen.blit(self.bg_benchi, self.bg_benchi_rect)

        # タイトル用じじい画像の描画
        self.screen.blit(self.bg_g_title, self.bg_g_title_rect)

        pygame.display.flip()  # 画面更新

# プレイヤー名をロードする関数
    def load_player_name(self):
        try:
            with open('data/iziruna.key', 'rb') as keyfile:
                key = keyfile.read()
            cipher_suite = Fernet(key)
            with open('data/player_name.json', 'rb') as file:
                encrypted_name = file.read()
            decrypted_name = cipher_suite.decrypt(
                encrypted_name).decode('utf-8')
            return decrypted_name if decrypted_name else None  # 名前が空でないことを確認
        except (FileNotFoundError, ValueError, json.decoder.JSONDecodeError):
            return None  # エラーが発生した場合は None を返す
