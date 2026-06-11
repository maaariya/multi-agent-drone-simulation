class Coordinator:

    def assign_task(self, drones, task):

        best_drone = None
        best_cost = 999999

        for drone in drones:

            if drone.state != "IDLE":
                continue

            cost = abs(drone.x - task.x) + abs(drone.y - task.y)

            if cost < best_cost:
                best_cost = cost
                best_drone = drone

        return best_drone