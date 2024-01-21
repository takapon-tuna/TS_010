import pygame


class GameOverScene:
    def __init__(self, screen):

        # screenをインスタンス変数として保存
        self.screen = screen

        # フォントの設定
        self.font = pygame.font.Font(None, 72)

        # テキストの設定
        self.text = self.font.render("Game_over", True, (144, 238, 144))

        # テキストの位置
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))

    def handle_event(self, event):
        # スペースキーが押されたかどうかをチェック
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'score_screen'
        return None

    def update(self):
        # 今は必要ない
        pass

    def draw(self):
        # 画面を薄い黄色に
        self.screen.fill((255, 255, 192))

        # テキストを描画
        self.screen.blit(self.text, self.text_rect)
