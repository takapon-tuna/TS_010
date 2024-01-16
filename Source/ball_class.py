# TS_010/Source/ball_class.py
import pygame


class Ball:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = (255, 255, 255)  # 白色
        self.radius = 10  # 半径

    def move(self, up=False, down=False, left=False, right=False, game_area_start=0, game_area_width=640, game_area_height=480):
        if right:
            self.x += self.speed
        if left:
            self.x -= self.speed
        if down:
            self.y += self.speed
        if up:
            self.y -= self.speed

        # 端に到達したら折り返す
        if self.x - self.radius < game_area_start:
            self.x = game_area_start + self.radius
        if self.x + self.radius > game_area_start + game_area_width:
            self.x = game_area_start + game_area_width - self.radius
        if self.y - self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > game_area_height:
            self.y = game_area_height - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
