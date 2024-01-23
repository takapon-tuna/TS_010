import pygame


class ScoreScreen:
    def __init__(self, screen):
        self.screen = screen  # screenをインスタンス変数として保存
        self.font = pygame.font.Font(None, 72)  # フォントの設定
        self.text = self.font.render(
            "score_screen", True, (144, 238, 144))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))  # テキストの位置

    def handle_event(self, event):
        # スペースキーが押されたかどうかをチェック
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'game_over'
        return None

    def update(self):
        # 今は必要ない
        pass

    def draw(self):
        self.screen.fill((255, 192, 192))  # 画面を薄い赤に
        self.screen.blit(self.text, self.text_rect)  # テキストを描画
        pygame.display.flip()  # 画面更新
