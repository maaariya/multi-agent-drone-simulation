class Drone:

    def __init__(self, drone_id, x, y):

        self.id = drone_id

        self.x = x
        self.y = y

        self.target = None

        self.battery = 100

        self.state = "IDLE"

        self.charge_rate = 0.5

    def move(self):

        # -----------------------
        # CHARGING MODE (HIGHEST PRIORITY)
        # -----------------------
        if self.state == "CHARGING":

            target_x, target_y = 0, 0

            # move toward charger
            if self.x < target_x:
                self.x += 1
            elif self.x > target_x:
                self.x -= 1
            elif self.y < target_y:
                self.y += 1
            elif self.y > target_y:
                self.y -= 1

            # recharge when at charger
            if self.x == 0 and self.y == 0:
                self.battery += self.charge_rate

                if self.battery >= 100:
                    self.battery = 100
                    self.state = "IDLE"
                    self.target = None

            return

        # -----------------------
        # NO TARGET
        # -----------------------
        if self.target is None:
            return

        # -----------------------
        # NORMAL DELIVERY MOVEMENT
        # -----------------------
        self.battery -= 1

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

        return self.x == self.target[0] and self.y == self.target[1]