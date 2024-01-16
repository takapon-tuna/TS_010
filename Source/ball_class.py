# TS_010/Source/ball_class.py
import pygame


class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (255, 255, 255)  # 白色
        self.radius = 10  # 半径

    def move(self, game_area_width, game_area_height):
        self.x += self.speed_x
        self.y += self.speed_y

        # 端に到達したら折り返す
        if self.x - self.radius < 0 or self.x + self.radius > game_area_width:
            self.speed_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > game_area_height:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
