import pygame
import sys
import time
import random
from collections import deque

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 300, 420
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZIP Puzzle Game")

FONT = pygame.font.SysFont(None, 40)
SMALL_FONT = pygame.font.SysFont(None, 24)

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# ---------------- PUZZLE ----------------
TILE = 100
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
puzzle = [1, 2, 3, 4, 0, 6, 7, 5, 8]

start_time = time.time()
end_time = None
game_over = False

# ---------------- DRAW ----------------
def draw():
    WIN.fill(WHITE)

    for i in range(9):
        if puzzle[i] != 0:
            x = (i % 3) * TILE
            y = (i // 3) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            pygame.draw.rect(WIN, GRAY, rect)
            pygame.draw.rect(WIN, BLACK, rect, 2)

            text = FONT.render(str(puzzle[i]), True, BLACK)
            WIN.blit(text, (x + 40, y + 30))

    # TIMER (FIXED)
    if end_time:
        elapsed = round(end_time - start_time, 2)
    else:
        elapsed = round(time.time() - start_time, 2)

    WIN.blit(SMALL_FONT.render(f"Time: {elapsed}s", True, BLACK), (10, 305))

    # Buttons
    pygame.draw.rect(WIN, BLUE, (10, 340, 80, 40))
    pygame.draw.rect(WIN, GREEN, (110, 340, 80, 40))
    pygame.draw.rect(WIN, RED, (210, 340, 80, 40))

    WIN.blit(SMALL_FONT.render("Shuffle", True, WHITE), (18, 352))
    WIN.blit(SMALL_FONT.render("Solve", True, WHITE), (130, 352))
    WIN.blit(SMALL_FONT.render("Exit", True, WHITE), (235, 352))

    pygame.display.update()

# ---------------- GAME LOGIC ----------------
def move(index):
    zero = puzzle.index(0)
    r1, c1 = index // 3, index % 3
    r2, c2 = zero // 3, zero % 3

    if abs(r1 - r2) + abs(c1 - c2) == 1:
        puzzle[zero], puzzle[index] = puzzle[index], puzzle[zero]

def shuffle():
    global start_time, end_time, game_over
    random.shuffle(puzzle)
    while puzzle == list(goal):
        random.shuffle(puzzle)
    start_time = time.time()
    end_time = None
    game_over = False

# ---------------- BFS SOLVER ----------------
def solve():
    global puzzle
    queue = deque([(tuple(puzzle), [])])
    visited = {tuple(puzzle)}

    while queue:
        state, path = queue.popleft()
        if state == goal:
            animate(path)
            return

        zero = state.index(0)
        row, col = zero // 3, zero % 3

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                nz = nr * 3 + nc
                new = list(state)
                new[zero], new[nz] = new[nz], new[zero]
                new_t = tuple(new)

                if new_t not in visited:
                    visited.add(new_t)
                    queue.append((new_t, path + [new_t]))

def animate(path):
    global puzzle
    for state in path:
        puzzle = list(state)
        draw()
        pygame.time.delay(200)

# ---------------- MAIN LOOP ----------------
running = True
while running:
    draw()

    # STOP TIMER EXACTLY WHEN SOLVED
    if tuple(puzzle) == goal and not game_over:
        game_over = True
        end_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Buttons
            if 340 <= y <= 380:
                if 10 <= x <= 90:
                    shuffle()
                elif 110 <= x <= 190:
                    solve()
                elif 210 <= x <= 290:
                    pygame.quit()
                    sys.exit()

            # Tile click
            elif not game_over and y < 300:
                move((y // TILE) * 3 + (x // TILE))

pygame.quit()
