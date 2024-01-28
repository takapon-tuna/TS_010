import pygame
import os
from cryptography.fernet import Fernet


class NameInputScene:
    def __init__(self, screen, firebase, auth):
        self.screen = screen
        self.firebase = firebase
        self.auth = auth
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 100)
        self.input_box = pygame.Rect(self.screen.get_width(
        ) // 2 - 150, self.screen.get_height() // 2 - 50, 300, 100)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('red')
        self.text_color = pygame.Color('white')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.notice_font = pygame.font.SysFont('msgothic', 32)  # 注意書き用フォント
        self.enter_font = pygame.font.SysFont('msgothic', 40)  # エンターキー指示用のフォント
        self.click_font = pygame.font.SysFont('msgothic', 40)  # クリック指示用のフォント

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.save_player_name(self.text)
                    return 'game_play'  # 名前入力後にゲームプレイシーンに移行
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        txt_surface = self.font.render(self.text, True, self.text_color)
        width = max(300, txt_surface.get_width()+10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + self.input_box.w // 2 - txt_surface.get_width() //
                         2, self.input_box.y + self.input_box.h // 2 - txt_surface.get_height() // 2))
        border_width = 10 if self.active else 2
        pygame.draw.rect(self.screen, self.color, self.input_box, border_width)

        notice_text = [
            "1. 名前に使える文字はアルファベットと数字記号のみで。日本語は使えないよ。",
            "2. 名前はオンライン上に保存されるから、問題のある単語の使用はおすすめしないよ。",
            "3. ランキングはトップ10のまでが表示されるけど、ユーザーチェックでPCのユーザー名が紐づけられるから、俺にはバレるよ。",
            "4. あとから名前の変更は基本できないから、考えてつけてね。"
        ]
        for i, text in enumerate(notice_text):
            notice_surface = self.notice_font.render(
                text, True, (255, 255, 255))
            self.screen.blit(notice_surface, (50, 150 + i * 50))

        # 文字が入力されたら「エンターキーを押して」と表示
        if self.text:
            enter_surface = self.enter_font.render(
                "名前が決まったらエンターキーを押して", True, (255, 255, 255))
            self.screen.blit(enter_surface, (self.screen.get_width(
            ) // 2 - enter_surface.get_width() // 2, self.screen.get_height() - 300))

        # 入力が開始されていない場合、「クリックして」と表示
        if not self.active:
            click_surface = self.click_font.render(
                "クリックして", True, (255, 255, 255))
            self.screen.blit(click_surface, (self.input_box.x + self.input_box.w // 2 -
                             click_surface.get_width() // 2, self.input_box.y + self.input_box.h + 10))

    def save_player_name(self, name):
        try:
            with open('data/iziruna.key', 'rb') as keyfile:
                key = keyfile.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('data/iziruna.key', 'wb') as keyfile:
                keyfile.write(key)

        cipher_suite = Fernet(key)
        encrypted_name = cipher_suite.encrypt(name.encode('utf-8'))

        with open('data/player_name.json', 'wb') as file:
            file.write(encrypted_name)

        if not os.path.exists('data/uid.txt'):
            user = self.auth.sign_in_anonymous()
            uid = user['localId']
            with open('data/uid.txt', 'w') as f:
                f.write(uid)
