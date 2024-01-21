from title_screen import TitleScene
from game_play import GamePlayScene
from game_over import GameOverScene
from score_screen import ScoreScreen

# シーンマネージャークラス


class SceneManager:
    def __init__(self, screen):
        self.screen = screen  # 画面オブジェクトの保存
        self.scenes = {  # 各シーンのインスタンスを作成
            'title': TitleScene(self.screen),
            'game_play': GamePlayScene(self.screen),
            'game_over': GameOverScene(self.screen),
            'score_screen': ScoreScreen(self.screen)
        }
        self.current_scene = self.scenes['title']  # 初期シーンを設定

    # イベント処理
    def handle_events(self, event):
        next_scene = self.current_scene.handle_event(
            event)  # 現在のシーンのイベント処理を呼び出す
        if next_scene is not None:  # 次のシーンが指定されている場合
            self.current_scene = self.scenes[next_scene]  # 次のシーンに切り替える

    # 更新処理
    def update(self):
        self.current_scene.update()  # 現在のシーンの更新処理を呼び出す

    # 描画処理
    def draw(self):
        self.current_scene.draw()  # 現在のシーンの描画処理を呼び出す
