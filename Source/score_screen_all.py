import pygame


class ScoreScreenAll:
    def __init__(self, screen, firebase, auth):
        self.screen = screen
        self.firebase = firebase
        self.auth = auth

        # 背景色を薄い赤色に設定
        self.background_color_t = (255, 200, 200)

        # フォントの設定
        self.font = pygame.font.SysFont(
            ['msgothic', 'ヒラキノ丸コpronw4'], 60)

        # トップ100のスコアを取得
        self.top_scores = self.get_top_scores()

        self.scroll_pos = 0

        self.prompt_text = "press to space"
        self.prompt_font = pygame.font.Font(None, 160)
        self.prompt_color = (255, 255, 255)  # 白色
        self.background_color = (255, 255, 255)  # 白色
        self.background_alpha = 128  # 半透明

    def handle_event(self, event):
        # ユーザーがスクロール操作を行った場合、スクロールの位置を更新
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # マウスホイールを上にスクロール
                self.scroll_pos = max(self.scroll_pos - 1, 0)
            elif event.button == 5:  # マウスホイールを下にスクロール
                self.scroll_pos = min(
                    self.scroll_pos + 1, len(self.top_scores) - 1)
        # スペースキーが押されたらタイトルシーンに遷移
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return 'title'
        return None

    def update(self):
        pass

    def get_top_scores(self):
        # Firebaseからトップ100のスコアを取得
        top_scores = self.firebase.database().child(
            "scores").order_by_child("score").limit_to_last(100).get().val()

        # スコアを適切な形式に変換
        scores_list = [{"name": data["name"], "score": data["score"], "play_time": data.get("play_time", 0)}
                       for uid, data in top_scores.items()]
        scores_list.sort(key=lambda x: x["score"], reverse=True)  # スコアで降順にソート

        return scores_list

    def draw(self):
        # 背景を描画
        self.screen.fill(self.background_color_t)

        # スコアとプレイ時間の最大幅を取得
        max_score_width = max(self.font.size(f"Score: {score['score']}")[
                              0] for score in self.top_scores)
        max_time_width = max(self.font.size(f"Play Time: {score['play_time']:.2f}秒")[
                             0] for score in self.top_scores)

        # トップ100のスコアを描画
        for index, score_data in enumerate(self.top_scores[self.scroll_pos:self.scroll_pos + 20]):
            # 順位を左端に寄せて描画
            rank_text = f"{self.scroll_pos + index + 1}."
            rank_rendered = self.font.render(rank_text, True, (255, 255, 255))
            rank_rect = rank_rendered.get_rect(left=10, top=50 + index * 60)
            self.screen.blit(rank_rendered, rank_rect)

            # 名前、スコア、時間を分けて描画
            name_text = f"{score_data['name'][:16]}"  # 名前を16文字に制限
            score_text = f"Score: {score_data['score']}"
            time_text = f"Play Time: {score_data['play_time']:.2f}秒"

            # 頭文字を左にそろえるための位置調整
            name_rendered = self.font.render(name_text, True, (255, 255, 255))
            score_rendered = self.font.render(
                score_text, True, (255, 255, 255))
            time_rendered = self.font.render(time_text, True, (255, 255, 255))

            # テキストの位置を順位の右隣に設定
            name_rect = name_rendered.get_rect(
                left=rank_rect.right + 10, top=50 + index * 60)

            # スコアのテキストを一定の位置に設定し、左側を揃える
            score_rect = score_rendered.get_rect(
                left=self.screen.get_width() // 2 - max_score_width // 2, top=50 + index * 60)

            # 時間のテキストを一定の位置に設定し、左側を揃える
            time_rect = time_rendered.get_rect(
                left=self.screen.get_width() - max_time_width - 10, top=50 + index * 60)

            self.screen.blit(name_rendered, name_rect)
            self.screen.blit(score_rendered, score_rect)
            self.screen.blit(time_rendered, time_rect)

        # 長方形の背景の Surface を作成
        prompt_surface = self.prompt_font.render(
            self.prompt_text, True, self.prompt_color)
        prompt_rect = prompt_surface.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() - 150))

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
