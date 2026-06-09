class Drone:

    def __init__(self, drone_id, x, y):

        self.id = drone_id

        self.x = x
        self.y = y

        self.target = None

        self.battery = 100

    def move(self):

        if self.target is None:
            return

        target_x, target_y = self.target

        if self.x < target_x:
            self.x += 1

        elif self.x > target_x:
            self.x -= 1

        elif self.y < target_y:
            self.y += 1

        elif self.y > target_y:
            self.y -= 1

    def at_target(self):

        if self.target is None:
            return False

        return (
            self.x == self.target[0]
            and
            self.y == self.target[1]
        )