import pygame
import random
import math


class Cloud:
    def __init__(self, screen_width, screen_height, game_area_start, game_area_width, game_area_height):
        # 画面外のランダムな場所から生成
        self.x = random.choice(
            [random.uniform(-100, 0), random.uniform(screen_width, screen_width + 100)])
        self.y = random.choice(
            [random.uniform(-100, 0), random.uniform(screen_height, screen_height + 100)])
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.circles = []
        self.generate_random_cloud()

        # 正方形のエリアのサイズを定義
        self.target_area_size = 500  # 500ピクセルの正方形

        # 正方形のエリアの中心座標を計算
        self.target_area_center_x = screen_width / 2
        self.target_area_center_y = screen_height / 2

        # 正方形のエリア内でランダムな目標位置を生成
        self.target_x = random.uniform(
            self.target_area_center_x - self.target_area_size / 2,
            self.target_area_center_x + self.target_area_size / 2)
        self.target_y = random.uniform(
            self.target_area_center_y - self.target_area_size / 2,
            self.target_area_center_y + self.target_area_size / 2)

        # 雲が目標位置に向かう初期方向を設定
        direction_to_target = pygame.math.Vector2(
            self.target_x - self.x, self.target_y - self.y)
        direction_to_target.normalize_ip()
        self.dx = direction_to_target.x
        self.dy = direction_to_target.y

        # エリア
        self.game_area_start = game_area_start
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height

        # 移動スピードを設定
        self.speed = 2.0  # スピード係数、小さいほど遅くなる

        # ゆらぎのための変数
        self.wobble_amount = 2  # ゆらぎの大きさ
        self.wobble_speed = 0.05  # ゆらぎの速さ
        self.wobble_phase = random.uniform(0, math.pi * 2)  # ゆらぎの位相

        print(f"生成された ({self.x}, {self.y})")  # 雲の生成位置をログ出力

    def generate_random_cloud(self):
        # 雲の形をより細かくランダムに生成する
        num_circles = random.randint(100, 150)  # 100から150個の円で雲を形成
        for _ in range(num_circles):
            radius = random.randint(20, 40)  # 半径を小さくする 20,40
            offset_x = random.randint(-radius, radius)  # X軸のオフセットを半径に応じて調整
            offset_y = random.randint(-radius, radius)  # Y軸のオフセットを半径に応じて調整
            self.circles.append((self.x + offset_x, self.y + offset_y, radius))

    def move(self):
        # ゲームエリアの端に到達したら画面内に戻るように方向を変える
        if self.x <= self.game_area_start:
            self.dx = abs(self.dx)  # 左端に到達したら右に進む
        elif self.x >= self.game_area_start + self.game_area_width:
            self.dx = -abs(self.dx)  # 右端に到達したら左に進む

        if self.y <= 0:
            self.dy = abs(self.dy)  # 上端に到達したら下に進む
        elif self.y >= self.game_area_height:
            self.dy = -abs(self.dy)  # 下端に到達したら上に進む

        # 雲が目標位置に近づいたら新しい目標位置を設定
        if abs(self.x - self.target_x) < 10 and abs(self.y - self.target_y) < 10:
            self.target_x = random.uniform(
                self.game_area_start, self.game_area_start + self.game_area_width)
            self.target_y = random.uniform(
                0, self.game_area_height)
            direction_to_target = pygame.math.Vector2(
                self.target_x - self.x, self.target_y - self.y)
            direction_to_target.normalize_ip()
            self.dx = direction_to_target.x
            self.dy = direction_to_target.y

        # ゆらぎを加える
        self.wobble_phase += self.wobble_speed
        wobble_x = self.wobble_amount * math.sin(self.wobble_phase)
        wobble_y = self.wobble_amount * math.cos(self.wobble_phase)

        # 雲の位置を更新（スピード係数を掛ける）
        self.x += self.dx * self.speed + wobble_x
        self.y += self.dy * self.speed + wobble_y

       # 各円の位置も更新
        for i, (x, y, radius) in enumerate(self.circles):
            self.circles[i] = (x + self.dx * self.speed +
                               wobble_x, y + self.dy * self.speed + wobble_y, radius)

        print(f"移動 ({self.x}, {self.y})")  # 雲の新しい位置をログ出力

    def draw(self, screen):
        for x, y, radius in self.circles:
            # 楕円を描画するための長方形を定義
            ellipse_rect = pygame.Rect(
                x - radius, y - radius // 2, radius * 2, radius)
            pygame.draw.ellipse(screen, (255, 255, 255), ellipse_rect)

        # 雲が描画されたことをログ出力
        print(f"描画された {len(self.circles)} circles")

    def is_clicked(self, mouse_pos):
        # マウスの位置が雲のいずれかの円の中にあるかをチェック
        for x, y, radius in self.circles:
            if (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2 <= radius ** 2:
                return True
        return False
