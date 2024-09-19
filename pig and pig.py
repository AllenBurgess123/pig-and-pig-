import pygame
import random
import sys
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)
FONT_PATH = R"D:\软件工程\第二次作业\simhei.ttf"
FONT_SIZE = 36
# 游戏时间限制（秒）
GAME_TIME = 60

# 游戏难度和时间设定
DIFFICULTY = {'normal': 70, 'medium': 50, 'hard': 30}

# 加载背景图片
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 加载字体
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 创建多层游戏板
layers = 3
board_layers = [[[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)] for _ in range(layers)]
selected = []

# 定义时钟
clock = pygame.time.Clock()

# 游戏结束标志
game_over = False

# 绘制游戏板
def draw_board():
    screen.fill(BG_COLOR)
    for layer in range(layers):
        for row in range(ROWS):
            for col in range(COLS):
                tile = board_layers[layer][row][col]
                if tile is not None:
                    screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
    pygame.display.flip()

# 匹配并消除图案
def check_match():
    if len(selected) == 3:
        r1, c1, l1 = selected[0]
        r2, c2, l2 = selected[1]
        r3, c3, l3 = selected[2]
        if (board_layers[l1][r1][c1] is not None and
                board_layers[l1][r1][c1] == board_layers[l2][r2][c2] == board_layers[l3][r3][c3]):
            board_layers[l1][r1][c1] = None
            board_layers[l2][r2][c2] = None
            board_layers[l3][r3][c3] = None
        selected.clear()


# 倒计时显示
def draw_countdown(time_left):
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Time Left: {time_left}", True, WHITE)
    time_rect = time_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(time_text, time_rect)

# 主菜单
def main_menu():
    menu = True
    while menu:
        screen.blit(background, (0, 0))
        easy_text = FONT.render("简单", True, WHITE)
        hard_text = FONT.render("困难", True, WHITE)
        veryhard_text = FONT.render("地狱", True, WHITE)
        start_text = FONT.render("点击开始游戏", True, WHITE)
        quit_text = FONT.render("退出游戏", True, WHITE)

        easy_rect = easy_text.get_rect(center=(WIDTH / 2, 100))
        hard_rect = hard_text.get_rect(center=(WIDTH / 2, 200))
        veryhard_rect = veryhard_text.get_rect(center=(WIDTH / 2, 300))
        start_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
        quit_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))

        screen.blit(easy_text, easy_rect)
        screen.blit(hard_text, hard_rect)
        screen.blit(veryhard_text, veryhard_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return 'easy'
                elif hard_rect.collidepoint(event.pos):
                    return 'hard'
                elif veryhard_rect.collidepoint(event.pos):
                    return 'very_hard'

        pygame.display.flip()

# 点击事件
def click(x, y):
    global selected
    clicked_item = None
    layer, row, col = get_tile_position(x, y)

    if layer is not None and row is not None and col is not None:
        clicked_item = board_layers[layer][row][col]

    if clicked_item and len(selected) < 3:
        selected.append((row, col, layer))
        check_match()

# 获取点击的图案位置
def get_tile_position(x, y):
    for layer in range(layers):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.collidepoint(x, y):
                    return layer, row, col
    return None, None, None

# 游戏结束画面
def end_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render('Game Over', True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(2000)

# 主循环
def main():
    global game_over

    difficulty = main_menu()  # 选择难度
    if difficulty == 'easy':
        game_time = 70
    elif difficulty == 'hard':
        game_time = 50
    else:
        game_time = 30

    start_ticks = pygame.time.get_ticks()  # 开始时的时间戳

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                click(x, y)

        # 计算剩余时间
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = game_time - seconds_passed

        if time_left <= 0:
            game_over = True
            end_screen()
            break

        draw_board()  # 重新绘制游戏板
        draw_countdown(time_left)  # 显示倒计时
        pygame.display.flip()

        clock.tick(FPS)  # 控制帧率

if __name__ == "__main__":
    main()
