import pygame
import json


class ScoreScreen:
    def __init__(self, screen, firebase, auth, ):

        self.score_bg = pygame.image.load(
            'assets/score/score_bg.png')  # 背景をロード

        self.screen = screen
        self.firebase = firebase
        self.auth = auth

        self.current_score = 0  # 現在のスコアを初期化
        self.current_play_time = 0.0  # 現在のプレイ時間を初期化

        self.font = pygame.font.SysFont(
            ['msgothic', 'Hiragino Maru Gothic Pro'], 72)  # フォントの設定
        self.text = self.font.render(
            "score_screen", True, (144, 238, 144))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))  # テキストの位置

        self.prompt_text = "press to space"
        self.prompt_font = pygame.font.Font(None, 160)
        self.prompt_color = (255, 255, 255)  # 白色
        self.background_color = (255, 255, 255)  # 白色
        self.background_alpha = 128  # 半透明

        # スコアとプレイ時間を JSON ファイルから読み込む
        try:
            with open('data/score_data.json', 'r') as f:
                data = json.load(f)
                self.current_score = data['score']
                self.current_play_time = data['play_time']
        except FileNotFoundError:
            print("Score data file not found.")

        # トップ10のスコアを取得
        self.top_scores = self.get_top_scores()

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
        # self.screen.fill((255, 192, 192))  # 画面を薄い赤に
        self.screen.blit(self.score_bg, (0, 0))  # 背景を描画

        # ランキングのタイトルを表示
        title_font = pygame.font.SysFont(
            ['msgothic', 'Hiragino Maru Gothic Pro'], 72, False)
        title_text = title_font.render(
            "ランキング", True, (0, 0, 140))  # 白色でテキストを描画
        title_pos = (self.screen.get_width() // 2 -
                     title_text.get_width() // 2, 50)  # 位置を設定
        self.screen.blit(title_text, title_pos)

        # 現在のスコアをランキングの一番上に表示
        your_score_font = pygame.font.SysFont(
            ['msgothic', 'Hiragino Maru Gothic Pro'], 34, True)
        your_score_text = f"今回のスコア: {self.current_score}"
        your_score_rendered = your_score_font.render(
            your_score_text, True, (255, 255, 255))  # 白色でテキストを描画
        your_time_text = f"{self.current_play_time:.2f}秒"
        your_time_rendered = your_score_font.render(
            your_time_text, True, (255, 255, 255))  # 白色でテキストを描画

        # スコアとプレイ時間の位置を設定
        your_score_pos_x = self.screen.get_width() * 3 // 6 - \
            your_score_rendered.get_width() // 2
        your_time_pos_x = self.screen.get_width() * 4 // 6 - \
            your_time_rendered.get_width() // 2
        your_pos_y = 150  # トップスコアより少し上に配置

        self.screen.blit(your_score_rendered, (your_score_pos_x, your_pos_y))
        self.screen.blit(your_time_rendered, (your_time_pos_x, your_pos_y))

        # トップ10のスコアを表示
        for i, score_data in enumerate(self.top_scores):
            score_font = pygame.font.SysFont(
                ['msgothic', 'Hiragino Maru Gothic Pro'], 34, True)
            rank_text = f"{i+1}."
            name_text = f"{score_data['name']}"
            score_text = f"{score_data['score']}"
            time_text = f"{score_data['play_time']:.2f}秒"

            rank_rendered = score_font.render(
                rank_text, True, (255, 255, 255))  # 白色でテキストを描画
            name_rendered = score_font.render(
                name_text, True, (255, 255, 255))  # 白色でテキストを描画
            score_rendered = score_font.render(
                score_text, True, (255, 255, 255))  # 白色でテキストを描画
            time_rendered = score_font.render(
                time_text, True, (255, 255, 255))  # 白色でテキストを描画

            base_pos_y = i * 70 + 200
            self.screen.blit(rank_rendered, (self.screen.get_width(
            ) * 1 // 6 - rank_rendered.get_width() // 2, base_pos_y))
            self.screen.blit(name_rendered, (self.screen.get_width(
            ) * 2 // 6 - name_rendered.get_width() // 2, base_pos_y))
            self.screen.blit(score_rendered, (self.screen.get_width(
            ) * 3 // 6 - score_rendered.get_width() // 2, base_pos_y))
            self.screen.blit(time_rendered, (self.screen.get_width(
            ) * 4 // 6 - time_rendered.get_width() // 2, base_pos_y))

         # 長方形の背景の Surface を作成
        prompt_surface = self.prompt_font.render(
            self.prompt_text, True, self.prompt_color)
        prompt_rect = prompt_surface.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() - 100))

        background_surface = pygame.Surface(
            (self.screen.get_width(), prompt_surface.get_height()))
        background_surface.set_alpha(self.background_alpha)  # 透明度を半透明に設定
        background_surface.fill(self.background_color)  # 背景色を設定
        background_rect = background_surface.get_rect(
            topleft=(0, prompt_rect.top))  # 長方形の位置を設定

        # 長方形の背景とテキストを描画
        self.screen.blit(background_surface, background_rect)
        self.screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()  # 画面更新

    def get_top_scores(self):
        # Firebaseからトップ10のスコアを取得
        top_scores = self.firebase.database().child(
            "scores").order_by_child("score").limit_to_last(10).get().val()

        # スコアを適切な形式に変換
        scores_list = [{"name": data["name"], "score": data["score"], "play_time": data.get("play_time", 0)}
                       for uid, data in top_scores.items()]
        scores_list.sort(key=lambda x: x["score"], reverse=True)  # スコアで降順にソート

        return scores_list

    def set_current_score_and_time(self, score, play_time):
        self.current_score = score
        self.current_play_time = play_time

    def update_score(self, score):
        # 現在のスコアを更新
        self.current_score = score
