# TS_010/Source/back_ground.py
import pygame

# 背景画像をロード(ゲーム開始時に一度だけ)
bg_image = pygame.image.load('assets/bg/sky.png')
# 別背景（テスト）
bg_test_image = pygame.image.load('assets/concept_art/UI.png')

# じじい(HP)をロード
hp_g_normal_image = pygame.image.load('assets/ui/g.png')
hp_g_high_image = pygame.image.load('assets/ui/g_happy.png')
hp_g_low_image = pygame.image.load('assets/ui/g_sad.png')

# じじい(HP)のサイズを取得
hp_normal_width, hp_normal_height = hp_g_normal_image.get_size()
hp_high_width, hp_high_height = hp_g_high_image.get_size()
hp_low_width, hp_low_height = hp_g_low_image.get_size()

# じじい(ベンチ)をロード
g_benchi_summer_image = pygame.image.load('assets/ui/g_benchi.png')

# じじい(ベンチ)のサイズを取得
bc_summer_width, bc_summer_height = g_benchi_summer_image.get_size()


def draw_background(screen, hp, time_elapsed):

    # 画面のサイズを取得
    screen_width, screen_height = screen.get_size()

    # 長方形のサイズを計算し、横幅を少し縮める
    rect_width = int(screen_width // 4 * 0.8)
    rect_height = int(screen_height)

    # じじい(HP)のサイズを変更
    g_image_normal_scaled = pygame.transform.scale(
        hp_g_normal_image, (hp_normal_width, hp_normal_height))
    g_image_high_scaled = pygame.transform.scale(
        hp_g_high_image, (hp_high_width, hp_high_height))
    g_image_low_scaled = pygame.transform.scale(
        hp_g_low_image, (hp_low_width, hp_low_height))

    # じじい(ベンチ)のサイズを0.8倍に変更
    g_benchi_summer_scaled = pygame.transform.scale(
        g_benchi_summer_image, (int(bc_summer_width * 0.8), int(bc_summer_height * 0.8)))

    # 画面に背景画像を描画
    screen.blit(bg_image, (0, 0))

    # 長方形の色を設定
    rect_color = (255, 224, 189)  # 薄い肌色

    # 左側の長方形を描画
    pygame.draw.rect(screen, rect_color, pygame.Rect(
        0, 0, rect_width, rect_height))

    # HPに応じて左上の画像を切り替え
    if hp > 20:  # HPが21以上の場合
        screen.blit(g_image_high_scaled, (rect_width // 4, 50))
    elif hp > 10:  # HPが11以上の場合
        screen.blit(g_image_normal_scaled, (rect_width // 4, 50))
    else:  # HPが10以下の場合
        screen.blit(g_image_low_scaled, (rect_width // 4, 50))

    # 時間が０秒以上なら表示し続ける
    if time_elapsed >= 0:
        screen.blit(g_benchi_summer_scaled, (1, rect_height // 2 + 50))

    # 右側の長方形を描画
    pygame.draw.rect(screen, rect_color, pygame.Rect(
        screen_width - rect_width, 0, rect_width, rect_height))

    # ゲーム操作部分の開始位置とサイズを計算
    game_area_start = rect_width
    game_area_width = screen_width - 2 * rect_width
    game_area_height = screen_height

    return game_area_start, game_area_width, game_area_height
