from environment import neighbors
import pygame
import json

episode_number = 4930

WINDOW_SIZE = 600
GRID_SIZE = 6
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

drone_img = pygame.image.load("drone.png")
robot_img = pygame.image.load("robot.png")
zap_img = pygame.image.load("zap.png")

drone_img = pygame.transform.scale(drone_img, (CELL_SIZE, CELL_SIZE))
robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))
zap_img = pygame.transform.scale(zap_img, (CELL_SIZE, CELL_SIZE))

with open("environment.json", "r") as f:
    env_data = json.load(f)

with open("trajectory.json", "r") as f:
    trajectory_data = json.load(f)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Grid World Visualization")
font = pygame.font.Font(None, 36)

episode = trajectory_data[str(episode_number)]
turn_keys = sorted(map(int, episode.keys()))  # Ensure turn order

turn_index = 0
running = True

while running:
    screen.fill(WHITE)
    for cell in env_data["red_cells"]:
        pygame.draw.rect(screen, RED, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for cell in env_data["green_cells"]:
        pygame.draw.rect(screen, GREEN, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for cell in env_data["obstacles"]:
        pygame.draw.rect(screen, GRAY, (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_SIZE))
        pygame.draw.line(screen, BLACK, (0, x), (WINDOW_SIZE, x))

    # Get current turn data
    turn = turn_keys[turn_index]
    turn_data = episode[str(turn)]

    # Extract player positions and type
    p1_pos = tuple(turn_data["p1t"])
    p2_pos = tuple(turn_data["p2t"])
    p2_type = turn_data["p2_type"]
    a1t = turn_data["a1t"]

    # Draw Players
    screen.blit(drone_img, (p1_pos[0] * CELL_SIZE, p1_pos[1] * CELL_SIZE))
    screen.blit(robot_img, (p2_pos[0] * CELL_SIZE, p2_pos[1] * CELL_SIZE))

    # Display Turn Number and Player 2 Type
    turn_text = font.render(f"Turn: {turn} | P2 Type: {p2_type}", True, BLACK)
    screen.blit(turn_text, (10, 10))

    # If Player 1 used 'Z', draw zap effect on neighboring cells
    if a1t == "Z":
        for zap_pos in neighbors(p1_pos):
            screen.blit(zap_img, (zap_pos[0] * CELL_SIZE, zap_pos[1] * CELL_SIZE))

    pygame.display.flip()

    # Wait for spacebar to continue or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    turn_index += 1
                    if turn_index >= len(turn_keys):
                        running = False  # Stop if out of turns

pygame.quit()
