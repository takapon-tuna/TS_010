import pygame


class ScoreScreen:
    def __init__(self, screen, firebase, auth):
        self.screen = screen
        self.firebase = firebase
        self.auth = auth

        self.font = pygame.font.Font(None, 72)  # フォントの設定
        self.text = self.font.render(
            "score_screen", True, (144, 238, 144))  # テキストの設定
        self.text_rect = self.text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2))  # テキストの位置

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
        self.screen.fill((255, 192, 192))  # 画面を薄い赤に
        self.screen.blit(self.text, self.text_rect)  # テキストを描画

        # トップ10のスコアを表示
        for i, score_data in enumerate(self.top_scores):
            score_text = f"{i+1}. {score_data['name']}: {score_data['score']}"
            score_font = pygame.font.Font(None, 36)
            score_rendered = score_font.render(
                score_text, True, (255, 255, 255))  # 白色でテキストを描画
            self.screen.blit(score_rendered, (10, i * 40 + 100))  # スコアを画面に表示

        pygame.display.flip()  # 画面更新

    def get_top_scores(self):
        # Firebaseからトップ10のスコアを取得
        top_scores = self.firebase.database().child(
            "scores").order_by_child("score").limit_to_last(10).get().val()

        # スコアを適切な形式に変換
        scores_list = [{"name": data["name"], "score": data["score"]}
                       for uid, data in top_scores.items()]
        scores_list.sort(key=lambda x: x["score"], reverse=True)  # スコアで降順にソート

        return scores_list
