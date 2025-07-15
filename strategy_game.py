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

class Troop:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner  # "blue" or "red"
        self.has_moved = False

    def draw(self, surface):
        center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)
        color = BLUE_COLOR if self.owner == "blue" else RED_COLOR
        pygame.draw.circle(surface, color, center, 20, 3)
        pygame.draw.circle(surface, (0,0,0), center, 20, 1)

    def can_move_to(self, tx, ty, grid):
        # Within 2 squares, not occupied by another troop of same owner
        if abs(self.x - tx) > 2 or abs(self.y - ty) > 2:
            return False
        if tx < 0 or tx >= COLUMNS or ty < 0 or ty >= ROWS:
            return False
        for troop in troops:
            if troop.x == tx and troop.y == ty:
                return False
        return True

# Troop lists
troops = []

# Spawn initial troops at capitals
troops.append(Troop(0, 4, "blue"))
troops.append(Troop(11, 4, "red"))

current_player = "blue"
moves_left = 1  # Will be set at turn start
selected_troop = None

def start_turn():
    global moves_left
    # Reset troop move status
    for troop in troops:
        if troop.owner == current_player:
            troop.has_moved = False
    # Count available troops for player
    player_troops = [t for t in troops if t.owner == current_player]
    moves_left = min(5, len(player_troops))
    # Spawn new troops on owned farms
    for row in grid:
        for tile in row:
            if tile.has_farm:
                if current_player == "blue" and tile.is_conquered_by_blue:
                    # Only spawn if no troop already there
                    if not any(t.x == tile.x and t.y == tile.y for t in troops):
                        troops.append(Troop(tile.x, tile.y, "blue"))
                elif current_player == "red" and tile.is_conquered_by_red:
                    if not any(t.x == tile.x and t.y == tile.y for t in troops):
                        troops.append(Troop(tile.x, tile.y, "red"))

def end_turn():
    global current_player, selected_troop
    current_player = "red" if current_player == "blue" else "blue"
    selected_troop = None
    start_turn()

start_turn()


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
        elif event.type == pygame.MOUSEBUTTONDOWN and moves_left > 0:
            mx, my = pygame.mouse.get_pos()
            tx, ty = mx // TILE_SIZE, my // TILE_SIZE

            if not selected_troop:
                for troop in troops:
                    if troop.owner == current_player and not troop.has_moved and troop.x == tx and troop.y == ty:
                        selected_troop = troop
                        break
            else:
                if selected_troop.can_move_to(tx, ty, grid):
                    selected_troop.x = tx
                    selected_troop.y = ty
                    selected_troop.has_moved = True
                    moves_left -= 1
                    tile = grid[ty][tx]
                    if current_player == "blue":
                        tile.is_conquered_by_blue = True
                        tile.is_conquered_by_red = False
                    else:
                        tile.is_conquered_by_red = True
                        tile.is_conquered_by_blue = False
                    selected_troop = None
                    if moves_left == 0:
                        end_turn()
                else:
                    selected_troop = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                end_turn()
    screen.fill((255, 255, 255))

    for row in grid:
        for tile in row:
            tile.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()