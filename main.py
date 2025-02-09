import pygame
import random

pygame.init()

BLACK = (255, 255, 255)
GREY = (0, 0, 0)
YELLOW = (255, 0, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 240

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    # decides which positions survive
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    # decide which positions are born
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


#  adjust  for continuous world
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            neighbors_x = (x + dx) % GRID_WIDTH
            neighbors_y = (y + dy) % GRID_HEIGHT
            neighbors.append((neighbors_x, neighbors_y))
    return neighbors


def main():
    # initialize basic variables
    running = True
    playing = False
    count = 0
    update_freq = 10
    positions = set()
    new_position = set()
    updatecount = 0

    #endless loop for the game engine
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            new_positions = adjust_grid(positions)
            if new_positions==positions:
                updatecount+= 1

            positions = new_positions

            if updatecount >= 3:
                positions = gen(random.randrange(4, 10) * GRID_WIDTH)




        pygame.display.set_caption("Start" if playing else "Pause")

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
                # start and stop the game
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # clear the field
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                # generate random positions (pixels)
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
