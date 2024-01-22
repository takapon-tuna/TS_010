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
        self.screen.fill((255, 255, 192))  # 画面を薄い黄色に
        self.screen.blit(self.text, self.text_rect)  # テキストを描画
        pygame.display.flip()  # 画面更新

    def move(self, dx, dy):
        # 雲の位置を更新
        self.x += dx
        self.y += dy
        # 各円の位置も更新
        for i, (x, y, radius) in enumerate(self.circles):
            self.circles[i] = (x + dx, y+dy, radius)
