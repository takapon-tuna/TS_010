import pygame
import random


class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.circles = []
        self.generate_random_cloud()

    def generate_random_cloud(self):
        # 雲の形をより細かくランダムに生成する
        num_circles = random.randint(100, 150)  # 50から70個の円で雲を形成
        for _ in range(num_circles):
            radius = random.randint(20, 40)  # 半径を小さくする 20,40
            offset_x = random.randint(-radius, radius)  # X軸のオフセットを半径に応じて調整
            offset_y = random.randint(-radius, radius)  # Y軸のオフセットを半径に応じて調整
            self.circles.append((self.x + offset_x, self.y + offset_y, radius))

    def draw(self, screen):
        for x, y, radius in self.circles:
            # 楕円を描画するための長方形を定義
            ellipse_rect = pygame.Rect(
                x - radius, y - radius // 2, radius * 2, radius)
            pygame.draw.ellipse(screen, (255, 255, 255), ellipse_rect)

    def is_clicked(self, mouse_pos):
        # マウスの位置が雲のいずれかの円の中にあるかをチェック
        for x, y, radius in self.circles:
            if (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2 <= radius ** 2:
                return True
        return False
