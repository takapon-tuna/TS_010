import pygame

# タイトルシーンクラス


class TitleScene:
    def __init__(self, screen):
        self.screen = screen  # 画面オブジェクトの保存
        self.font = pygame.font.Font(None, 72)  # フォントの設定
        self.text = self.font.render("Title", True, (255, 255, 255))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))  # テキストの位置
        self.background = pygame.image.load(
            'assets/ui/titlescreen.png')  # 背景をロード

    # イベント処理
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                return 'game_play'  # ゲームプレイシーンに切り替える
        return None

    # 更新処理
    def update(self):
        pass

    # 描画処理
    def draw(self):
        self.screen.blit(self.background, (0, 0))  # 背景描画
        self.screen.blit(self.text, self.text_rect)  # テキスト描画
        pygame.display.flip()  # 画面更新
