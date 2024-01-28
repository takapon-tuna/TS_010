import pygame
from scene_manager_class import SceneManager

# フレームワーククラス


class Framework:
    def __init__(self, firebase, auth):
        pygame.init()  # pygameの初期化
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)  # フルスクリーンモードで画面を作成
        self.clock = pygame.time.Clock()  # 時計オブジェクトの作成
        self.scene_manager = SceneManager(
            self.screen, firebase, auth)  # シーンマネージャの作成

    # イベント処理
    def handle_events(self):
        for event in pygame.event.get():  # イベントループ
            if event.type == pygame.QUIT:  # 終了イベントの場合
                pygame.quit()  # pygameを終了
                return False

            if event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
                if event.key == pygame.K_ESCAPE:  # ESCキーが押された場合
                    pygame.quit()  # pygameを終了
                    return False

            # シーンマネージャにイベントを処理させる
            scene_result = self.scene_manager.handle_events(event)
            if scene_result == 'quit':
                pygame.quit()  # pygameを終了
                return False

            # self.manager.process_events(event)  # UIマネージャにイベントを処理させる

        return True

    # 更新処理
    def update(self):
        time_delta = self.clock.tick(60)/1000.0  # 時間差を計算
        # self.manager.update(time_delta)  # UIマネージャの更新
        self.scene_manager.update()  # シーンマネージャの更新

    # 描画処理
    def draw(self):
        # self.manager.draw_ui(self.screen)  # UIの描画
        self.scene_manager.draw()  # シーンの描画

        # # フレームレートの表示
        # fps = self.clock.get_fps()
        # font = pygame.font.Font(None, 36)
        # fps_text = font.render(f'FPS: {fps:.2f}', True, pygame.Color('white'))
        # screen_width = pygame.display.get_surface().get_size()[0]
        # fps_text_width = fps_text.get_rect().width
        # self.screen.blit(fps_text, (screen_width - fps_text_width - 10, 10))

        pygame.display.flip()

    # メインループ
    def run(self):
        while self.handle_events():  # イベント処理
            self.update()  # 更新
            self.draw()  # 描画


# メイン関数
if __name__ == "__main__":
    framework = Framework()  # フレームワークの作成
    framework.run()  # メインループの開始
