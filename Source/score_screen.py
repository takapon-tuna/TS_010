import pygame


class ScoreScreen:
    def __init__(self, screen):
        # フォントの設定
        self.font = pygame.font.Font(None, 72)

        # テキストの設定
        self.text = self.font.render("score_screen", True, (144, 238, 144))

        # テキストの位置
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))

    def handle_event(self, event):
        # スペースキーが押されたかどうかをチェック
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'title'
        return None

    def draw(self, screen):
        # 画面を薄い赤に
        screen.fill((255, 192, 192))

        # テキストを描画
        screen.blit(self.text, self.text_rect)
