#starters
import pygame
import sys
import random

pygame.init()

#setups
TILE_SIZE = 80
ROWS = 9
COLUMNS = 12

WIDTH, HEIGHT = TILE_SIZE * COLUMNS, TILE_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("easy game")

clock = pygame.time.Clock()

#colors
LAND_COLOR = (255, 255, 0)            # Yellow land
CITY_COLOR = (255, 215, 0)            # Gold (player capital)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (65, 105, 225)
CONQUERED_RED_TERRITORY = (255, 0, 0, 100)       # With transparency
CONQUERED_BLUE_TERRITORY = (65, 105, 225, 100)   # With transparency

#tile
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = LAND_COLOR
        self.is_blue_capital = False
        self.is_red_capital = False
        self.has_farm = False

        self.is_conquered_by_blue = False
        self.is_conquered_by_red = False

    def draw(self, surface):
        # Draw the base tile
        pygame.draw.rect(surface, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surface, (0, 0, 0), (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        # Draw conquered overlay if needed
        tile_rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        if self.is_conquered_by_blue:
            overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            overlay.fill(CONQUERED_BLUE_TERRITORY)
            surface.blit(overlay, tile_rect)

        elif self.is_conquered_by_red:
            overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            overlay.fill(CONQUERED_RED_TERRITORY)
            surface.blit(overlay, tile_rect)
        if self.has_farm:
            dot_center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(surface, (0, 200, 0), dot_center, 8)


        
        # Draw capital marker
        center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)

        if self.is_blue_capital:
            pygame.draw.circle(surface, BLUE_COLOR, center, 10)
        elif self.is_red_capital:
            pygame.draw.circle(surface, RED_COLOR, center, 10)

# Create grid
grid = [[Tile(x, y) for x in range(COLUMNS)] for y in range(ROWS)]

# Set capital positions and conquered states
grid[4][0].is_blue_capital = True
grid[4][0].is_conquered_by_blue = True

grid[4][11].is_red_capital = True
grid[4][11].is_conquered_by_red = True

num_farms = 20
placed = 0
while placed < num_farms:
    x = random.randint(0, COLUMNS - 1)
    y = random.randint(0, ROWS - 1)
    tile = grid[y][x]
    if not tile.is_blue_capital and not tile.is_red_capital and not tile.has_farm:
        tile.has_farm = True
        placed += 1

# Main loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for row in grid:
        for tile in row:
            tile.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()