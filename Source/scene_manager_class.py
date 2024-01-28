from title_screen import TitleScene
from game_play import GamePlayScene
from game_over import GameOverScene
from score_screen import ScoreScreen
from name_input_scene import NameInputScene
from score_screen_all import ScoreScreenAll
# シーンマネージャークラス


class SceneManager:
    def __init__(self, screen, firebase, auth):
        self.screen = screen
        self.firebase = firebase
        self.auth = auth
        self.scenes = {
            'title': TitleScene,
            'game_play': GamePlayScene,
            'game_over': GameOverScene,
            'score_screen': ScoreScreen,
            'name_input': NameInputScene,
            'score_screen_all': ScoreScreenAll
        }
        self.current_scene = self.scenes['title'](
            self.screen, self.firebase, self.auth)  # 初期シーンを設定

    # イベント処理
    def handle_events(self, event):
        next_scene = self.current_scene.handle_event(
            event)  # 現在のシーンのイベント処理を呼び出す
        if next_scene == 'quit':
            return 'quit'  # 'quit'メッセージを返す
        elif next_scene is not None:  # 次のシーンが指定されている場合
            print(f"シーンが {next_scene} に切り替わります。")  # デバッグ用のログ出力
            self.current_scene = self.scenes[next_scene](
                self.screen, self.firebase, self.auth)  # 次のシーンに切り替える

    # 更新処理
    def update(self):
        self.current_scene.update()  # 現在のシーンの更新処理を呼び出す

    # 描画処理
    def draw(self):
        self.current_scene.draw()  # 現在のシーンの描画処理を呼び出す
