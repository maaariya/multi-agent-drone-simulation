import pygame
from constants import *
from drone import Drone
from task import DeliveryTask
from coordinator import Coordinator
import random

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Multi-Agent Simulation")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

task_spawn_timer = 0

# -----------------------
# AGENTS
# -----------------------
drones = [
    Drone(1, 2, 2),
    Drone(2, 5, 8),
    Drone(3, 10, 4),
    Drone(4, 15, 15),
    Drone(5, 18, 6)
]

tasks = [
    DeliveryTask(4, 15),
    DeliveryTask(10, 3),
    DeliveryTask(17, 12)
]

coordinator = Coordinator()

# -----------------------
# INITIAL ASSIGNMENT
# -----------------------
for task in tasks:

    drone = coordinator.assign_task(drones, task)

    if drone:
        drone.target = (task.x, task.y)
        drone.state = "DELIVERING"
        task.assigned = True


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


# -----------------------
# MAIN LOOP
# -----------------------
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # -----------------------
    # SPAWN TASKS
    # -----------------------
    task_spawn_timer += 1

    if task_spawn_timer >= 50:

        new_task = DeliveryTask(
            random.randint(1, GRID_SIZE - 1),
            random.randint(1, GRID_SIZE - 1)
        )

        tasks.append(new_task)

        task_spawn_timer = 0

    # -----------------------
    # BATTERY CHECK (OVERRIDE)
    # -----------------------
    for drone in drones:

        if drone.battery < 20:
            drone.state = "CHARGING"
            drone.target = (CHARGER_X, CHARGER_Y)

    # -----------------------
    # MOVE DRONES
    # -----------------------
    for drone in drones:
        drone.move()

    # -----------------------
    # CHECK TASK COMPLETION
    # -----------------------
    for drone in drones:

        if drone.at_target():

            if drone.state == "DELIVERING":

                for task in tasks:

                    if task.x == drone.x and task.y == drone.y:
                        task.completed = True

                drone.target = None
                drone.state = "IDLE"

    # -----------------------
    # ASSIGN NEW TASKS
    # -----------------------
    for task in tasks:

        if task.completed or task.assigned:
            continue

        drone = coordinator.assign_task(drones, task)

        if drone:

            drone.target = (task.x, task.y)
            drone.state = "DELIVERING"
            task.assigned = True

    # -----------------------
    # DRAW GRID
    # -----------------------
    draw_grid()

    # charging station
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (CHARGER_X * CELL_SIZE, CHARGER_Y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

    # -----------------------
    # DRAW DRONES
    # -----------------------
    for drone in drones:

        color = (255, 165, 0) if drone.state == "CHARGING" else (0, 0, 255)

        pygame.draw.circle(
            screen,
            color,
            (
                drone.x * CELL_SIZE + CELL_SIZE // 2,
                drone.y * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 3
        )

        state_text = font.render(drone.state, True, (0, 0, 0))
        battery_text = font.render(f"{int(drone.battery)}%", True, (0, 100, 0))

        screen.blit(state_text, (drone.x * CELL_SIZE, drone.y * CELL_SIZE - 15))
        screen.blit(battery_text, (drone.x * CELL_SIZE, drone.y * CELL_SIZE + 20))

    # -----------------------
    # DRAW TASKS
    # -----------------------
    for task in tasks:

        if task.completed:
            continue

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (task.x * CELL_SIZE, task.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()