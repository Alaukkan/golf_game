import math

import scripts.definitions as defs
from scripts.clubs import clubs
from scripts.utils import load_image

class Player():
    clubs = []
    club = 0
    direction = 0
    swingspeed = 1
    turn_right = False
    turn_left = False
    direction_set = False
    crosshair_offset = (-3, -4)

    def __init__(self, game, clubs=["PT"]):
        self.game = game
        self.clubs = clubs
        self.club = len(clubs) - 1
        self.crosshair = self.game.assets["images"]["sprites/crosshair/00"]
        self.ball = Ball(self.game, self, self.game.map.tee)
        self.set_new_direction()
        self.strokes = 0
        self.total_strokes = 0

    def update(self):
        self.direction -= 0.02 if self.turn_right else 0
        self.direction += 0.02 if self.turn_left else 0

    def render(self, surf, offset):
        if self.ball.is_moving:
            return
        if self.ball.on_green:
            render_offset = (offset[0] + int(defs.GREEN_CAM_SCALE * (-self.ball.pos_x - self.game.map.green[0])) + self.crosshair_offset[0],
                             offset[1] + int(defs.GREEN_CAM_SCALE * (-self.ball.pos_z - self.game.map.green[1])) + self.crosshair_offset[0])
        else: 
            render_offset = (defs.GAME_RESOLUTION[0] / 2 + self.crosshair_offset[0], 
                             defs.GAME_RESOLUTION[1] / 2 + self.crosshair_offset[1])
        surf.blit(self.crosshair, (render_offset[0] - defs.CROSSHAIR_DISTANCE * math.sin(self.direction), render_offset[1] - defs.CROSSHAIR_DISTANCE * math.cos(self.direction)))

    def hit_ball(self):
        self.strokes += 1
        self.total_strokes += 1

        club = clubs[self.clubs[self.club]]
        self.ball.last_pos = [self.ball.pos_x, self.ball.pos_z]

        surface = self.ball.last_surface
        power = club["power"] * defs.SURFACE_SWING_AFFECT[surface][club["type"]] * self.swingspeed

        self.ball.vel_x = math.sin(self.direction) * math.cos(club["angle"]) * power
        self.ball.vel_y = math.sin(club["angle"]) * power
        self.ball.vel_z = math.cos(self.direction) * math.cos(club["angle"]) * power

    def set_new_direction(self):
        if not self.direction_set:
            self.direction = math.atan2(-self.ball.pos_x - self.game.map.pin[0], -self.ball.pos_z - self.game.map.pin[1])
            self.direction_set = True
        if self.ball.on_green:
            self.club = 0

class Ball():
    mass = 0.046 # kilograms
    radius = 0.0213 # metres
    inertia = 2 / 5 * mass * radius ** 2
    cross_sectional_area = math.pi * radius**2
    pos_x = 0
    pos_y = 0
    pos_z = 0
    vel_x = 0
    vel_y = 0
    vel_z = 0
    image = ""
    img_offset = (-3, -4)
    on_green = False
    is_moving = False

    def __init__(self, game, player, pos):
        self.game = game
        self.player = player
        self.pos_x = pos[0]
        self.pos_z = pos[1]
        self.last_pos = [self.pos_x, self.pos_z]
        self.shadow_img = self.game.assets["images"]["sprites/ball/00"]

    def render(self, surf, offset):
        ball_height = 0
        if self.pos_y > 0.05:
            ball_height = - self.pos_y * math.cos(math.radians(defs.VIEWING_ANGLE))
        if self.on_green:
            offset = (offset[0] + int(defs.GREEN_CAM_SCALE * (-self.pos_x - self.game.map.green[0])), offset[1] + int(defs.GREEN_CAM_SCALE * (-self.pos_z - self.game.map.green[1])))
            if self.pos_y > 0.05:
                surf.blit(self.shadow_img, (offset[0] + self.img_offset[0], offset[1] + self.img_offset[1]))
            surf.blit(self.game.assets["images"][f"sprites/ball/0{int(min(self.pos_y // (5 / defs.GREEN_CAM_SCALE) + 1, 4))}"], (offset[0] + self.img_offset[0], offset[1] + defs.GREEN_CAM_SCALE * ball_height + self.img_offset[1]))
        else:
            if self.pos_y > 0.05:
                surf.blit(self.shadow_img, (offset[0] + self.img_offset[0], offset[1] + self.img_offset[1]))
            surf.blit(self.game.assets["images"][f"sprites/ball/0{int(min(self.pos_y // 5 + 1, 4))}"], (offset[0] + self.img_offset[0], offset[1] + ball_height + self.img_offset[1]))

    def update(self):
        velocity_magnitude_2d = math.sqrt(self.vel_x**2 + self.vel_z**2)
        velocity_magnitude_3d = math.sqrt(self.vel_x**2 + self.vel_y**2 + self.vel_z**2)

        # update position based on velocity
        self.pos_x += self.vel_x / defs.FRAME_RATE
        self.pos_y = max(self.pos_y + self.vel_y / defs.FRAME_RATE, 0)
        self.pos_z += self.vel_z / defs.FRAME_RATE

        self.last_surface = self.game.map.get_surface(defs.GAME_RESOLUTION[0] / 2, defs.GAME_RESOLUTION[1] / 2)
        # ground collision check
        if self.pos_y == 0:
            energy = 1/2 * self.mass * self.vel_y**2
            energy *= defs.SURFACE_HARDNESS[self.last_surface]
            self.vel_y = math.sqrt(2 * energy / self.mass)

            if self.vel_y > defs.VELOCITY_THRESHOLD * 10:
                energy = 1/2 * self.mass * velocity_magnitude_2d**2
                energy *= defs.SURFACE_HARDNESS[self.last_surface]
                self.vel_x = math.sqrt(2 * energy / self.mass) * self.vel_x / velocity_magnitude_2d
                self.vel_z = math.sqrt(2 * energy / self.mass) * self.vel_z / velocity_magnitude_2d
            else:
                self.vel_y = 0

        # Calculate drag force
        if velocity_magnitude_3d > defs.VELOCITY_THRESHOLD and self.pos_y > 0:
            drag_acceleration = (defs.BALL_WIND_RESISTANCE * defs.AIR_DENSITY * self.cross_sectional_area * velocity_magnitude_3d**2) / (2 * self.mass)
            
            # apply drag acceleration
            if (self.vel_x > 0):
                self.vel_x = max(self.vel_x - drag_acceleration * (self.vel_x / velocity_magnitude_3d) / defs.FRAME_RATE, 0)
            else:
                self.vel_x = min(self.vel_x - drag_acceleration * (self.vel_x / velocity_magnitude_3d) / defs.FRAME_RATE, 0)
            
            if (self.vel_y > 0):
                self.vel_y = max(self.vel_y - drag_acceleration * (self.vel_y / velocity_magnitude_3d) / defs.FRAME_RATE, 0)
            else:
                self.vel_y = min(self.vel_y - drag_acceleration * (self.vel_y / velocity_magnitude_3d) / defs.FRAME_RATE, 0)

            if (self.vel_z > 0):
                self.vel_z = max(self.vel_z - drag_acceleration * (self.vel_z / velocity_magnitude_3d) / defs.FRAME_RATE, 0)
            else:
                self.vel_z = min(self.vel_z - drag_acceleration * (self.vel_z / velocity_magnitude_3d) / defs.FRAME_RATE, 0)

        # apply gravity and wind
        if self.pos_y > 0:
            self.vel_y -= defs.GRAVITY / defs.FRAME_RATE

            wind_acceleration = (defs.BALL_WIND_RESISTANCE * defs.AIR_DENSITY * self.cross_sectional_area * self.game.map.wind[1]**2) / (2 * self.mass)
            # apply wind
            self.vel_x += wind_acceleration * math.sin(self.game.map.wind[0]) / defs.FRAME_RATE
            self.vel_x += wind_acceleration * math.cos(self.game.map.wind[0]) / defs.FRAME_RATE

        # apply rolling resistance
        elif velocity_magnitude_2d > defs.VELOCITY_THRESHOLD: 
            if (self.vel_x > 0):
                self.vel_x = max(self.vel_x - (self.vel_x * velocity_magnitude_2d + 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
            else:
                self.vel_x = min(self.vel_x - (self.vel_x * velocity_magnitude_2d - 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
            
            if (self.vel_z > 0):
                self.vel_z = max(self.vel_z - (self.vel_z * velocity_magnitude_2d + 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
            else:
                self.vel_z = min(self.vel_z - (self.vel_z * velocity_magnitude_2d - 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)

        else:
            self.vel_x = 0
            self.vel_z = 0 

        # apply accel on green
        if self.on_green:
            roll_direction, gradient = self.game.map.get_green_gradient(self.pos_x, self.pos_z)
            roll_acceleration = math.tan(gradient) * defs.GRAVITY

            self.vel_x += math.sin(roll_direction) * roll_acceleration / defs.FRAME_RATE
            self.vel_z += math.cos(roll_direction) * roll_acceleration / defs.FRAME_RATE

        # check OB
        if self.pos_y == 0 and self.vel_x == 0 and self.vel_z == 0:
            if self.last_surface == "OB":
                self.pos_x = self.last_pos[0]
                self.pos_z = self.last_pos[1]
            self.is_moving = False
            self.game.player.set_new_direction()
        else:
            self.is_moving = True
            self.game.player.direction_set = False

    def distance_from_pin(self):
        return math.sqrt((-self.pos_x - self.game.map.pin[0]) ** 2 + (-self.pos_z - self.game.map.pin[1]) ** 2)
