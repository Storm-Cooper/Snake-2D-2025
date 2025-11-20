import pygame
import random
import sys
import os


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

HIGH_SCORE_FILE = "highscore.txt"

def load_highscore():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def save_highscore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def draw_grid(surface):
    pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)

def draw_snake(surface, snake_body):
    for x, y in snake_body:
        pygame.draw.rect(surface, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_apple(surface, apple_pos):
    x, y = apple_pos
    pygame.draw.rect(surface, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def move_snake(direction, snake_body):
    head_x, head_y = snake_body[0]

    if direction == "UP":
        head_y -= 1
    elif direction == "DOWN":
        head_y += 1
    elif direction == "LEFT":
        head_x -= 1
    elif direction == "RIGHT":
        head_x += 1

    new_head = (head_x, head_y)
    snake_body.insert(0, new_head)
    snake_body.pop()
    return snake_body


def menu_screen(surface, font_large, font_small, high_score):
    surface.fill(BLACK)
    title = font_large.render("SNAKE 2D", True, GREEN)
    start_text = font_small.render("Press SPACE to Start", True, WHITE)
    hs_text = font_small.render(f"High Score: {high_score}", True, YELLOW)

    surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 200))
    surface.blit(start_text, ((SCREEN_WIDTH - start_text.get_width()) // 2, 350))
    surface.blit(hs_text, ((SCREEN_WIDTH - hs_text.get_width()) // 2, 420))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_over_screen(surface, font_large, font_small, score, high_score):
    surface.fill(BLACK)

    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    high_score_text = font_small.render(f"High Score: {high_score}", True, YELLOW)
    restart_text = font_small.render("Press SPACE to Restart", True, GREEN)

    surface.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, 200))
    surface.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 320))
    surface.blit(high_score_text, ((SCREEN_WIDTH - high_score_text.get_width()) // 2, 360))
    surface.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) // 2, 450))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# ---------- MAIN GAME LOOP ----------
def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake 2D")

    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont("Courier", 48, bold=True)
    font_small = pygame.font.SysFont("Courier", 24, bold=True)

    high_score = load_highscore()

    menu_screen(surface, font_large, font_small, high_score)

    def reset_game():
        snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        direction = "RIGHT"
        apple = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        score = 0
        return snake_body, direction, apple, score

    snake_body, direction, apple_pos, score = reset_game()

    running = True
    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(high_score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        snake_body = move_snake(direction, snake_body)
        head_x, head_y = snake_body[0]

        if head_x <= 0 or head_x >= GRID_WIDTH - 1 or head_y <= 0 or head_y >= GRID_HEIGHT - 1:
            if score > high_score:
                high_score = score
                save_highscore(high_score)
            game_over_screen(surface, font_large, font_small, score, high_score)
            snake_body, direction, apple_pos, score = reset_game()

        if snake_body[0] in snake_body[1:]:
            if score > high_score:
                high_score = score
                save_highscore(high_score)
            game_over_screen(surface, font_large, font_small, score, high_score)
            snake_body, direction, apple_pos, score = reset_game()

        if snake_body[0] == apple_pos:
            snake_body.append(snake_body[-1])
            score += 10
            apple_pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))

        surface.fill(BLACK)
        draw_grid(surface)
        draw_snake(surface, snake_body)
        draw_apple(surface, apple_pos)

        score_text = font_small.render(f"Score: {score}", True, WHITE)
        hs_text = font_small.render(f"High Score: {high_score}", True, YELLOW)

        surface.blit(score_text, (25, 25))
        surface.blit(hs_text, (25, 55))

        pygame.display.update()


if __name__ == "__main__":
    main()
