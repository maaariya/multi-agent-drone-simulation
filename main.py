import pygame
from constants import *
from drone import Drone
from task import DeliveryTask
from coordinator import Coordinator

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Multi-Agent Simulation")

clock = pygame.time.Clock()

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

for task in tasks:

    assigned_drone = coordinator.assign_task(
        drones,
        task
    )

    assigned_drone.target = (task.x, task.y)

    print(
        f"Task ({task.x},{task.y}) assigned to Drone {assigned_drone.id}"
    )

def draw_grid():

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (0, y),
            (WIDTH, y)
        )


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for drone in drones:
        drone.move()

    for drone in drones:

        if drone.at_target():

            for task in tasks:

                if (
                    task.x == drone.x
                    and
                    task.y == drone.y
                ):
                    task.completed = True

            drone.target = None

    draw_grid()

    for drone in drones:

        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (
                drone.x * CELL_SIZE + CELL_SIZE // 2,
                drone.y * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 3
        )

    for task in tasks:

        if task.completed:
            continue


        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                task.x * CELL_SIZE,
                task.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()