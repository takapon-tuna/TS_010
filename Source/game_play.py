import pygame
import time
import json
import getpass
from back_ground import Background
from player_class import Player
from cloud import Cloud
from cryptography.fernet import Fernet
from score_screen import ScoreScreen

TRANSITION_SCREEN = pygame.USEREVENT + 1


class GamePlayScene:
    def __init__(self, screen, firebase, auth):
        self.firebase = firebase
        self.auth = auth

        # BGMの初期化と再生
        pygame.mixer.init()
        pygame.mixer.music.load('assets/bgm/Plantation.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)  # -1は無限ループを意味します

        # SEをロード
        self.cloud_sound = pygame.mixer.Sound('assets/se/cloud.mp3')
        # 設定

        self.score = 0  # スコアの初期化
        self.score_multiplier = 1.0  # スコア乗算の初期化
        self.last_cloud_hit_time = 0  # 最後に雲を消した時間
        self.cloud_hit_streak = 0  # 連続して雲を消した回数
        self.streak_duration = 3  # ストリークの継続時間
        self.streak_points = 0  # ストリーク中に獲得したポイント
        self.last_score_update = time.time()  # 最後にスコアを更新した時間の初期化

        self.screen = screen
        self.background = Background(screen)  # 背景オブジェクトの作成
        self.player = Player()  # プレイヤーオブジェクトの作成
        self.start_time = time.time()  # 開始時間の記録
        self.elapsed_time = 0  # 経過時間の初期化
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()  # ゲームエリアの計算

        self.clouds = [Cloud(self.screen.get_width(), self.screen.get_height(
        ), self.game_area_start, self.game_area_width, self.game_area_height) for _ in range(5)]

        self.cloud_spawn_time = 0

        self.game_over = False  # ゲームオーバーフラグの初期化

        self.last_health_decrease_time = time.time()  # HPが減少した最後の時間を初期化

        self.top_scores = self.get_top_scores()

    # 雲の設定
        self.max_clouds = 15  # 雲の最大数
        self.cloud_spawn_interval = 1.3  # 何秒ごとに雲を生成

        self.last_cloud_update = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for cloud in self.clouds[:]:
                if cloud.is_clicked(mouse_pos):
                    self.clouds.remove(cloud)
                    self.cloud_sound.play()  # 雲を消したときの効果音を再生

                    current_time = time.time()
                    time_since_last_hit = current_time - self.last_cloud_hit_time

                    # ストリークのチェック
                    if time_since_last_hit <= self.streak_duration:
                        self.cloud_hit_streak += 1
                    else:
                        self.cloud_hit_streak = 1

                    # ストリーク時間に応じたスコア乗算率の設定
                    if time_since_last_hit <= 20:
                        score_multiplier = 4
                    elif time_since_last_hit <= 40:
                        score_multiplier = 6
                    elif time_since_last_hit <= 60:
                        score_multiplier = 12
                    else:
                        score_multiplier = 12  # 60秒以上は12倍のまま

                    self.last_cloud_hit_time = current_time
                    # ポイントの計算（ストリークと乗算率に応じて）
                    points = 10 * self.cloud_hit_streak * score_multiplier
                    # スコアにポイントを加算
                    self.score += points
                    # 雲を消したらHPを回復
                    if self.player.health <= 30:
                        self.player.health += 2.0
                    break  # 1つのクリックで複数の雲は消せない
        elif event.type == pygame.KEYDOWN:  # キーダウンイベントの場合
            # if event.key == pygame.K_SPACE:  # スペースキーが押された場合
            # return 'score_screen'  # ゲームオーバーシーンに切り替える
            if event.key == pygame.K_e:  # 'e'キーが押された場合
                self.player.health -= 40  # プレイヤーのHPを減らす

        # ゲームオーバーフラグが立っている場合はシーンを切り替える
        if self.game_over:
            return 'score_screen'

        return None

    def update(self):
        self.elapsed_time = time.time() - self.start_time  # 経過時間の更新

        # プレイヤーのHPが時間とともに減少するようにする
        if time.time() - self.last_health_decrease_time >= 1:
            self.player.health -= 2
            self.last_health_decrease_time = time.time()

        # 雲の数値を更新
        self.update_cloud_parameters()

        # ゲームエリアの再計算
        self.game_area_start, self.game_area_width, self.game_area_height = self.background.calculate_game_area()

        current_time = time.time()
        if len(self.clouds) < self.max_clouds and current_time - self.cloud_spawn_time > self.cloud_spawn_interval:
            # Cloud オブジェクトを生成する際に、ゲームエリアの情報を引数として渡す
            new_cloud = Cloud(
                self.screen.get_width(),
                self.screen.get_height(),
                self.game_area_start,
                self.game_area_width,
                self.game_area_height
            )
            self.clouds.append(new_cloud)
            self.cloud_spawn_time = current_time

        # 雲の更新
        for cloud in self.clouds:
            cloud.move()

        # ストリークが終了しているかどうかをチェック
        if time.time() - self.last_cloud_hit_time > self.streak_duration and self.streak_points > 0:
            # ストリーク終了時のポイントをスコアに加算し、ストリークポイントをリセット
            self.score += self.streak_points
            self.streak_points = 0

           # ゲームオーバーの条件をチェック
        if self.player.health <= 0 and not self.game_over:
            self.game_over = True  # ゲームオーバーフラグを立てる
            player_name = self.decrypt_player_name()  # プレイヤー名を復号化
            play_time = time.time() - self.start_time  # プレイ時間を計算
            pc_username = getpass.getuser()  # PCのユーザーネームを取得
            self.send_score_to_firebase(
                player_name, self.score, play_time, pc_username)  # スコアを送信

            # スコアとプレイ時間を JSON ファイルに出力
            with open('data/score_data.json', 'w') as f:
                json.dump({'score': self.score, 'play_time': play_time}, f)

            # return 'score_screen'  # ゲームオーバー時に'score_screen'を返す
            pygame.event.post(pygame.event.Event(TRANSITION_SCREEN))

    def draw(self):
        # 画面サイズを取得
        screen_width, screen_height = self.screen.get_size()

        self.background.draw(self.screen)  # 背景の描画
        # 雲の描画
        for cloud in self.clouds:
            cloud.draw(self.screen)
        # 左右の長方形描画
        self.background.draw_rectangles(self.screen)
        self.background.draw_ui(
            self.screen, self.player.health, self.elapsed_time)

    # UI(スコア)の描画
        self.draw_ui_elements()

        pygame.display.flip()  # 画面更新

    def update_cloud_parameters(self):
        # 経過時間が5秒ごとに増加したかをチェック
        if int(self.elapsed_time) // 5 > self.last_cloud_update:
            # 雲の最大数を増やす
            self.max_clouds = min(
                20, self.max_clouds + 1)
            # 各雲のスピードを増やす
            for cloud in self.clouds:
                cloud.speed_clouds = min(
                    8, cloud.speed_clouds + 0.33)
            # 最後の更新時間を記録する
            self.last_cloud_update = int(self.elapsed_time) // 5
        # ストリーク数が50の倍数に達する度に雲の生成間隔を短くする
        if self.cloud_hit_streak % 50 == 0 and self.cloud_hit_streak != 0:
            self.cloud_spawn_interval = max(
                0.6, self.cloud_spawn_interval * 0.95)  # 生成間隔を5%短くする

    def format_score(self, score):
        if score < 1000:
            return str(score)
        elif score < 1000000:
            # 1,000以上100万未満は小数点第一位まで表示してKで表示
            return f'{score / 1000:.1f}K'
        elif score < 1000000000:
            # 100万以上は小数点第三位まで表示してMで表示
            return f'{score / 1000000:.3f}M'
        else:
            # 10億以上は小数点第三位まで表示してBで表示
            return f'{score / 1000000000:.3f}B'

    def draw_ui_elements(self):
        # Background クラスから右側の長方形の横幅を取得
        right_rect_width = self.background.get_right_rectangle_width()

    # スコア表示

        # スコア表示エリアの横幅を計算（右側の長方形の80%）
        score_area_width = int(right_rect_width * 0.9)
        score_area_height = 100  # 高さ
        score_area_x = self.screen.get_width() - right_rect_width + \
            (right_rect_width - score_area_width) // 2
        score_area_y = 50  # 上からの位置を設定

        # 内側の四角形を描画
        score_area_color = (200, 200, 200)  # 灰色
        pygame.draw.rect(self.screen, score_area_color, (score_area_x,
                         score_area_y, score_area_width, score_area_height))

        # スコアのフォントサイズを計算（横幅に合わせる）
        score_font_size = int(
            score_area_width / len("Score: 999M") * 2.0)
        score_font = pygame.font.Font(None, score_font_size)

        # スコアの描画位置を設定
        score_text = "Score: "
        score_value = self.format_score(self.score)  # スコアをフォーマット
        score_rendered = score_font.render(
            f"{score_text}{score_value}", True, (0, 0, 0))  # 黒色でテキストを描画
        score_pos_x = score_area_x + \
            (score_area_width - score_rendered.get_width()) // 2  # 中央揃え
        score_pos_y = score_area_y + \
            (score_area_height - score_rendered.get_height()) // 2  # 中央揃え

    # ストリーク（コンボ）表示

        # ストリーク表示エリアの設定
        streak_area_height = 100  # ストリーク表示エリアの高さ
        streak_area_y = score_area_y + score_area_height + 50  # スコアエリアの下に配置

        # ストリーク表示エリアの四角形を描画（黄色）
        streak_area_color = (255, 255, 0)  # 黄色
        pygame.draw.rect(self.screen, streak_area_color, (score_area_x,
                         streak_area_y, score_area_width, streak_area_height))

        # ストリーク数のテキストを描画
        streak_font = pygame.font.Font(
            None, score_font_size)  # ストリーク数のフォントサイズはスコアと同じにする
        streak_text = f"Streak: {self.cloud_hit_streak}"
        streak_rendered = streak_font.render(
            streak_text, True, (0, 0, 0))  # 黒色でテキストを描画
        streak_pos_x = score_area_x + \
            (score_area_width - streak_rendered.get_width()) // 2  # 中央揃え
        streak_pos_y = streak_area_y + 20  # 上からの位置を設定
        self.screen.blit(streak_rendered, (streak_pos_x, streak_pos_y))

        # ストリーク継続時間のゲージバーを描画
        gauge_width = score_area_width - 20  # ゲージバーの横幅はスコアエリアの横幅からマージンを引いたもの
        gauge_height = 20  # ゲージバーの高さ
        gauge_x = score_area_x + 10  # ゲージバーのX位置（マージンを考慮）
        gauge_y = streak_pos_y + streak_rendered.get_height() + 10  # ゲージバーのY位置（テキストの下）

        # ストリーク継続時間の割合を計算
        streak_time_passed = time.time() - self.last_cloud_hit_time
        streak_ratio = max(
            0, min(1, streak_time_passed / self.streak_duration))

    # 描画
        # スコアを内側の四角形の中央に描画
        self.screen.blit(score_rendered, (score_pos_x, score_pos_y))

        # ゲージバーの背景を描画（灰色）
        pygame.draw.rect(self.screen, (200, 200, 200),
                         (gauge_x, gauge_y, gauge_width, gauge_height))

        # ゲージバーの前景を描画（緑色）
        pygame.draw.rect(self.screen, (0, 255, 0), (gauge_x, gauge_y,
                         gauge_width * (1 - streak_ratio), gauge_height))

        for index, score_data in enumerate(self.top_scores):  # 保存したスコアを使用
            score_text = f"{index + 1}. {score_data['name']}: {score_data['score']}"
            score_rendered = score_font.render(score_text, True, (0, 0, 0))
            text_x = score_area_x + \
                (right_rect_width - score_rendered.get_width()) // 2
            self.screen.blit(
                score_rendered, (text_x, score_area_y + 500 + index * 50))

    def decrypt_player_name(self):
        try:
            with open('data/iziruna.key', 'rb') as keyfile:
                key = keyfile.read()
            cipher_suite = Fernet(key)
            with open('data/player_name.json', 'rb') as file:
                encrypted_name = file.read()
            decrypted_name = cipher_suite.decrypt(
                encrypted_name).decode('utf-8')
            return decrypted_name
        except (FileNotFoundError, ValueError, json.decoder.JSONDecodeError):
            return "Unknown Player"

    def send_score_to_firebase(self, player_name, score, play_time, pc_username):
        # uid.txtからUIDを読み込む
        try:
            with open('data/uid.txt', 'r') as f:
                uid = f.read().strip()
        except FileNotFoundError:
            # uid.txtが存在しない場合は匿名認証を使用して新しいUIDを生成
            user = self.auth.sign_in_anonymous()
            uid = user['localId']
            with open('data/uid.txt', 'w') as f:
                f.write(uid)

        # Firebaseから既存のスコアを取得
        existing_score = self.firebase.database().child(
            "scores").child(uid).child("score").get().val()

        # 新しいスコアが既存のスコアより高い場合、または既存のスコアが存在しない場合にのみ書き込む
        if existing_score is None or score > existing_score:
            data = {"name": player_name, "score": score, "uid": uid,
                    "play_time": play_time, "pc_username": pc_username}
            # Firebase Realtime Databaseにデータを保存（既存のデータは上書きされる）
            self.firebase.database().child("scores").child(uid).set(data)

    def get_top_scores(self):
        # Firebaseからスコアデータを取得
        scores = self.firebase.database().child("scores").get().val()
        if scores:
            # スコアデータをスコアの値でソート
            sorted_scores = sorted(
                scores.values(), key=lambda s: s['score'], reverse=True)
            # トップ10のスコアを取得
            top_scores = sorted_scores[:10]
            return top_scores
        return []

    def draw_top_scores(self):
        # Background クラスから右側の長方形の横幅を取得
        right_rect_width = self.background.get_right_rectangle_width()

        # スコア表示エリアの設定
        score_area_x = self.screen.get_width() - right_rect_width
        score_area_y = self.screen.get_height() * 0.5  # 長方形の下側からの開始位置を下に移動

        # スコアのフォント設定
        score_font = pygame.font.Font(None, 60)  # フォントサイズを小さくする

        # トップ10のスコアを描画
        for index, score_data in enumerate(self.top_scores):  # 保存したスコアを使用
            score_text = f"{index + 1}. {score_data['name']}: {score_data['score']}"
            score_rendered = score_font.render(score_text, True, (0, 0, 0))
            text_x = score_area_x + \
                (right_rect_width - score_rendered.get_width()) // 2  # テキストを中央に寄せる
            self.screen.blit(
                score_rendered, (text_x, score_area_y + index * 50))  # 行間を狭くする
