import pygame
import json
from cryptography.fernet import Fernet


class NameInputScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.input_box = pygame.Rect(100, 100, 140, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

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

    def save_player_name(self, name):
        # 既存のキーを読み込むか、新しいキーを生成
        try:
            with open('iziruna.key', 'rb') as keyfile:
                key = keyfile.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('iziruna.key', 'wb') as keyfile:
                keyfile.write(key)

        cipher_suite = Fernet(key)
        encrypted_name = cipher_suite.encrypt(name.encode('utf-8'))

        with open('player_name.json', 'wb') as file:
            file.write(encrypted_name)

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)