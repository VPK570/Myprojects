import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGTH = 800, 800
TILE_SIZE = 20

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGTH // TILE_SIZE
FPS = 120

screen = pygame.display.set_mode((WIDTH, HEIGTH))

clock = pygame.time.Clock()

def main():
    running = True
    playing = False
    count = 0
    update_frequencey = 60

    positions = set()

    pygame.display.set_caption("Game of Life - Press Space to Start/Stop, C to Clear, R to Randomize")
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >=update_frequencey:
            count = 0
            positions = update_postion(positions)

        pygame.display.set_caption("Playing" if playing else "Paused ")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing =  not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_r:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)


        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()

def draw_grid(positions):

    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))
    
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGTH))

def gen(num):
    return set([(random.randrange(0,GRID_WIDTH), random.randrange(0,GRID_HEIGHT)) for _ in range(num)])

def update_postion(postions):
    new_positions = set()
    all_neighbors = set()

    for pos in postions:
        neighbors = get_neighbors(pos)
        all_neighbors.update(neighbors)

        # Survival: live cell with 2 or 3 neighbors survives
        live_neighbors = [n for n in neighbors if n in postions]
        if len(live_neighbors) in [2, 3]:
            new_positions.add(pos)

    # Birth: dead cell with exactly 3 live neighbors becomes alive
    for pos in all_neighbors:
        if pos not in postions:
            neighbors = get_neighbors(pos)
            live_neighbors = [n for n in neighbors if n in postions]
            if len(live_neighbors) == 3:
                new_positions.add(pos)

    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if x + dx < 0 or x + dx >= GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors

if __name__ == "__main__":
    main()