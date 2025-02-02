import math
import pygame

import scripts.definitions as defs
from scripts.clubs import clubs

class Player():
    clubs = []
    club = 0
    direction = 0
    backswing = 0
    swingspeed = 1
    overswung = False
    turn_right = False
    turn_left = False
    direction_set = False
    crosshair_offset = (-3, -4)

    def __init__(self, game, clubs=["PT"]):
        self.game = game
        self.clubs = clubs
        self.club = len(clubs) - 1
        self.crosshair = self.game.assets["images"]["crosshair/00"]
        self.new_ball()
        self.set_new_direction()
        self.strokes = 0
        self.total_strokes = 0

    def new_ball(self):
        self.ball = Ball(self.game, self, self.game.map.tee)

    def update(self):
        self.direction -= 0.02 if self.turn_right else 0
        self.direction += 0.02 if self.turn_left else 0

    def render(self, surf, offset):
        if self.ball.is_moving:
            return
        if self.ball.on_green:
            render_offset = (defs.GAME_RESOLUTION[0] / 2 + int(defs.GREEN_CAM_SCALE * (-self.ball.pos_x - self.game.map.green[0])) + self.crosshair_offset[0],
                             defs.GAME_RESOLUTION[1] / 2 + int(defs.GREEN_CAM_SCALE * (-self.ball.pos_z - self.game.map.green[1])) + self.crosshair_offset[0])
        else: 
            render_offset = (offset[0] + self.crosshair_offset[0], 
                             offset[1] + self.crosshair_offset[1])
        surf.blit(self.crosshair, (render_offset[0] - defs.CROSSHAIR_DISTANCE * math.sin(self.direction), render_offset[1] - defs.CROSSHAIR_DISTANCE * math.cos(self.direction)))

        if self.game.assets["hitting"] != 0:
            if self.game.assets["hitting_meter"] < 0:
                self.miss_ball()
                return
            elif self.game.assets["hitting"] == 1:
                if self.game.assets["hitting_meter"] > defs.MAX_BACKSWING or self.overswung:
                    self.overswung = True
                    self.game.assets["hitting_meter"] -= self.swingspeed * 100 / defs.FRAME_RATE
                else:
                    self.game.assets["hitting_meter"] += self.swingspeed * 100 / defs.FRAME_RATE

                hitting_meter_width = self.game.assets["hitting_meter"]
                
            elif self.game.assets["hitting"] == 2:
                self.game.assets["hitting_meter"] -= self.swingspeed * 200 / defs.FRAME_RATE
                if self.ball.on_green:
                    self.hit_ball()
                    self.game.assets["state"] = defs.MAP
                    return

                hitting_meter_width = self.backswing * defs.MAX_BACKSWING

            surf.blit(self.game.assets["images"]["HUD/hit_bar"], (defs.HITTING_METER_POS[0] - defs.MAX_BACKSWING - 2, defs.HITTING_METER_POS[1] - 3))

            hitting_meter = pygame.Rect(defs.HITTING_METER_POS[0] - hitting_meter_width, defs.HITTING_METER_POS[1], hitting_meter_width, defs.HITTING_METER_HEIGHT)
            pygame.draw.rect(surf, defs.HITTING_METER_COLOR, hitting_meter)

            hitting_indicator = self.game.assets["images"]["HUD/hit_indicator"]
            surf.blit(hitting_indicator, (defs.HITTING_METER_POS[0] - self.game.assets["hitting_meter"] - 1, defs.HITTING_METER_POS[1] - 1))


    def miss_ball(self):
        self.overswung = False
        self.strokes += 1
        self.total_strokes += 1
        self.game.assets["hitting"] = 0
        self.game.assets["hitting_meter"] = 0


    def hit_ball(self):
        self.overswung = False
        self.strokes += 1
        self.game.assets["hitting"] = 0
        self.game.assets["hitting_meter"] = 0

        club = clubs[self.clubs[self.club]]
        surface = self.ball.last_surface
        power = club["power"] * defs.SURFACE_SWING_AFFECT[surface][club["type"]] * self.swingspeed * self.backswing

        self.ball.vel_x = math.sin(self.direction) * math.cos(club["angle"]) * power
        self.ball.vel_y = math.sin(club["angle"]) * power
        self.ball.vel_z = math.cos(self.direction) * math.cos(club["angle"]) * power

        self.ball.last_pos = [self.ball.pos_x, self.ball.pos_z]
        self.ball.spin = self.spin * self.swingspeed * self.backswing * math.sin(club["angle"])
        self.ball.direction = self.direction

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
    spin = 0
    direction = 0
    backspin = 0
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
        self.shadow_img = self.game.assets["images"]["ball/00"]

    def render(self, surf, offset):
        ball_height = - self.pos_y * math.cos(math.radians(defs.VIEWING_ANGLE)) * 3

        if self.on_green:
            offset = (offset[0] + int(defs.GREEN_CAM_SCALE * (-self.pos_x - self.game.map.green[0])), offset[1] + int(defs.GREEN_CAM_SCALE * (-self.pos_z - self.game.map.green[1])))
            if self.in_air:
                surf.blit(self.shadow_img, (offset[0] + self.img_offset[0], offset[1] + self.img_offset[1]))
            surf.blit(self.game.assets["images"][f"ball/0{int(min(self.pos_y // (5 / defs.GREEN_CAM_SCALE) + 1, 4))}"], (offset[0] + self.img_offset[0], offset[1] + defs.GREEN_CAM_SCALE * ball_height + self.img_offset[1]))
        
        else:
            if -self.pos_x < defs.GAME_RESOLUTION[0] / 2:
                offset[0] = -self.pos_x
            if -self.pos_x > self.game.map.img_size[0] - defs.GAME_RESOLUTION[0] / 2:
                offset[0] = defs.GAME_RESOLUTION[0] - (self.game.map.img_size[0] + self.pos_x)
            if -self.pos_z < defs.GAME_RESOLUTION[1] / 2:
                offset[1] = -self.pos_z
            if -self.pos_z > self.game.map.img_size[1] - defs.GAME_RESOLUTION[1] / 2:
                offset[1] = defs.GAME_RESOLUTION[1] - (self.game.map.img_size[1] + self.pos_z)

            self.game.offset = offset

            if self.in_air:
                surf.blit(self.shadow_img, (offset[0] + self.img_offset[0], offset[1] + self.img_offset[1]))
            surf.blit(self.game.assets["images"][f"ball/0{int(min(self.pos_y // 5 + 1, 4))}"], (offset[0] + self.img_offset[0], offset[1] + ball_height + self.img_offset[1]))

            
    def update(self):
        velocity_magnitude_2d = math.sqrt(self.vel_x**2 + self.vel_z**2)
        velocity_magnitude_3d = math.sqrt(self.vel_x**2 + self.vel_y**2 + self.vel_z**2)

        self.update_position()

        self.check_ground_collision(velocity_magnitude_2d)

        if self.in_air:
            self.apply_drag(velocity_magnitude_3d)
            self.apply_gravity()
            self.apply_wind()

        else:
            if self.on_green:
                # check if ball is in hole: slow enough and close enough to the pin (hole):
                if velocity_magnitude_2d < 2 and self.distance_from_pin() < defs.HOLE_RADIUS:
                    self.game.ball_in_hole()
                else:
                    self.apply_green_gradient_roll(velocity_magnitude_2d)

            self.apply_backspin()
            self.apply_rolling_resistance(velocity_magnitude_2d)

        self.check_movement(velocity_magnitude_3d)


    def update_position(self):
        # update position based on velocity
        self.pos_x += self.vel_x / defs.FRAME_RATE
        self.pos_y = max(self.pos_y + self.vel_y / defs.FRAME_RATE, 0)
        self.pos_z += self.vel_z / defs.FRAME_RATE

        self.in_air = self.pos_y > 0.05


    def check_ground_collision(self, vel_mgn_2d):
        surface = self.game.map.get_surface(self.pos_x, self.pos_z)
        if surface != "water":
            self.last_land_pos = [self.pos_x, self.pos_z]

        # ground collision check
        if self.pos_y == 0:
            if surface == "water":
                self.pos_x = self.last_land_pos[0]
                self.pos_z = self.last_land_pos[1]
                self.vel_x = self.vel_y = self.vel_z = 0
            else:
                self.last_surface = surface
                
            # calculate energy loss from bounce
            energy = 1/2 * self.mass * self.vel_y**2
            energy *= defs.SURFACE_HARDNESS[self.last_surface]

            # calculate new y-axis velocity
            self.vel_y = math.sqrt(2 * energy / self.mass)

            if self.vel_y > defs.VELOCITY_THRESHOLD * 10:
                # loss of forward momentum in bounces
                energy = 1/2 * self.mass * vel_mgn_2d**2
                energy *= defs.SURFACE_HARDNESS[self.last_surface]

                self.vel_x = math.sqrt(2 * energy / self.mass) * self.vel_x / vel_mgn_2d if vel_mgn_2d != 0 else 0
                self.vel_z = math.sqrt(2 * energy / self.mass) * self.vel_z / vel_mgn_2d if vel_mgn_2d != 0 else 0
                self.apply_backspin(magnitude=3)
            else:
                # prevent jitter
                self.vel_y = 0


    def apply_drag(self, vel_mgn_3d):
        if vel_mgn_3d < defs.VELOCITY_THRESHOLD:
            return
        
        # Calculate drag force
        drag_acceleration = (defs.BALL_WIND_RESISTANCE * defs.AIR_DENSITY * self.cross_sectional_area * vel_mgn_3d**2) / (2 * self.mass)
        
        # apply drag acceleration
        if (self.vel_x > 0):
            self.vel_x = max(self.vel_x - drag_acceleration * (self.vel_x / vel_mgn_3d) / defs.FRAME_RATE, 0)
        else:
            self.vel_x = min(self.vel_x - drag_acceleration * (self.vel_x / vel_mgn_3d) / defs.FRAME_RATE, 0)
        
        if (self.vel_y > 0):
            self.vel_y = max(self.vel_y - drag_acceleration * (self.vel_y / vel_mgn_3d) / defs.FRAME_RATE, 0)
        else:
            self.vel_y = min(self.vel_y - drag_acceleration * (self.vel_y / vel_mgn_3d) / defs.FRAME_RATE, 0)

        if (self.vel_z > 0):
            self.vel_z = max(self.vel_z - drag_acceleration * (self.vel_z / vel_mgn_3d) / defs.FRAME_RATE, 0)
        else:
            self.vel_z = min(self.vel_z - drag_acceleration * (self.vel_z / vel_mgn_3d) / defs.FRAME_RATE, 0)


    def apply_gravity(self):
        # apply gravity
        self.vel_y -= defs.GRAVITY / defs.FRAME_RATE


    def apply_wind(self):
        # apply wind
        wind_acceleration = (defs.BALL_WIND_RESISTANCE * defs.AIR_DENSITY * self.cross_sectional_area * self.game.map.wind[1]**2) / (2 * self.mass)
        
        self.vel_x += wind_acceleration * math.sin(self.game.map.wind[0]) / defs.FRAME_RATE
        self.vel_x += wind_acceleration * math.cos(self.game.map.wind[0]) / defs.FRAME_RATE


    def apply_green_gradient_roll(self, vel_mgn_2d):
        if vel_mgn_2d < defs.VELOCITY_THRESHOLD * 5:
            return
        
        # apply accel on green
        roll_direction, gradient = self.game.map.get_green_gradient(self.pos_x, self.pos_z)
        roll_acceleration = math.tan(gradient) * defs.GRAVITY

        self.vel_x += math.sin(roll_direction) * roll_acceleration / defs.FRAME_RATE
        self.vel_z += math.cos(roll_direction) * roll_acceleration / defs.FRAME_RATE 

    
    def apply_backspin(self, magnitude=1):
        if self.spin == 0:
            return

        self.vel_x -= math.sin(self.direction + math.pi) * 10 * self.spin * magnitude / defs.FRAME_RATE
        self.vel_z -= math.cos(self.direction + math.pi) * 10 * self.spin * magnitude / defs.FRAME_RATE

        if self.spin < 0:
            self.spin = min(0, self.spin + 5 * magnitude / defs.FRAME_RATE)
        elif self.spin > 0:
            self.spin = max(0, self.spin - 5 * magnitude / defs.FRAME_RATE)


    def apply_rolling_resistance(self, vel_mgn_2d):
        if vel_mgn_2d < defs.VELOCITY_THRESHOLD:
            # prevent jitter
            self.vel_x = 0
            self.vel_z = 0 
            return
        # apply rolling resistance
        if (self.vel_x > 0):
            self.vel_x = max(self.vel_x - (self.vel_x * vel_mgn_2d + 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
        else:
            self.vel_x = min(self.vel_x - (self.vel_x * vel_mgn_2d - 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
        
        if (self.vel_z > 0):
            self.vel_z = max(self.vel_z - (self.vel_z * vel_mgn_2d + 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)
        else:
            self.vel_z = min(self.vel_z - (self.vel_z * vel_mgn_2d - 2) * defs.SURFACE_ROLLING_RESISTANCE[self.last_surface] / defs.FRAME_RATE, 0)

    def check_movement(self, vel_mgn_3d):
        # check if ball is stationary
        if vel_mgn_3d == 0:
            # check OB
            if self.last_surface == "OB":
                self.game.player.strokes += 1
                self.pos_x = self.last_pos[0]
                self.pos_z = self.last_pos[1]
            
            self.is_moving = False
            self.spin = 0
            self.game.player.set_new_direction()

        else:
            self.is_moving = True
            self.game.player.direction_set = False


    def distance_from_pin(self):
        return math.sqrt((-self.pos_x - self.game.map.pin[0]) ** 2 + (-self.pos_z - self.game.map.pin[1]) ** 2)
