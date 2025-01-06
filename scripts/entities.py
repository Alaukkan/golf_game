import math
import pygame

import scripts.definitions as defs
from scripts.clubs import clubs
from scripts.utils import load_image

class Player():
    clubs = []
    club = 0
    direction = 0
    turn_right = False
    turn_left = False

    def __init__(self, game, clubs=["PT"]):
        self.game = game
        self.clubs = clubs
        self.club = 0
        self.direction = 0

    def update(self):
        self.direction -= 0.25 if self.turn_right else 0
        self.direction += 0.25 if self.turn_left else 0

    def hit_ball(self):
        club = clubs[self.clubs[self.club]]
        self.game.ball.vel_x = math.cos(self.direction) * math.cos(club["angle"]) * club["power"]
        self.game.ball.vel_y = math.sin(club["angle"]) * club["power"]
        self.game.ball.vel_z = math.sin(self.direction) * math.cos(club["angle"]) * club["power"]

class Ball():
    mass = 0.046 # kilograms
    radius = 0.0213 # metres
    inertia = 2 / 5 * mass * radius ** 2
    pos_x = 0
    pos_y = 0
    pos_z = 0
    vel_x = 0
    vel_y = 0
    vel_z = 0
    image = ""
    img_offset = (4, 4)

    def __init__(self, game, x, z):
        self.game = game
        self.pos_x = x
        self.pos_z = z

    def render(self, surf, offset):
        path = f"ball/0{int(self.pos_y // 5)}.png"
        surf.blit(load_image(path), (self.pos_x - offset[0] + self.img_offset[0], self.pos_z - offset[1] + self.img_offset[1]))

    def update(self):

        # update position based on velocity
        self.pos_x += self.vel_x / defs.FRAME_RATE
        self.pos_y += self.vel_y / defs.FRAME_RATE
        self.pos_z += self.vel_z / defs.FRAME_RATE

        surface = self.game.map.get_surface(self.pos_x, self.pos_z)
        # ground collision check
        if self.pos_y < 0:
            self.pos_y = 0
            if (abs(self.vel_y) > defs.VELOCITY_THRESHOLD):
                self.vel_y *= -defs.SURFACE_HARDNESS[surface] # ball bounces
            else: 
                self.vel_y = 0

        # update ball velocity

        # Calculate drag force
        velocity_magnitude_2d = math.sqrt(self.vel_x**2 + self.vel_z**2)
        if velocity_magnitude_2d > defs.VELOCITY_THRESHOLD:
            cross_sectional_area = math.pi * self.radius**2
            drag_acceleration = (defs.BALL_WIND_RESISTANCE * defs.AIR_DENSITY * cross_sectional_area * velocity_magnitude_2d**2) / (2 * self.mass)
            
            # apply drag acceleration
            self.vel_x = max(self.vel_x - drag_acceleration * (self.vel_x / velocity_magnitude_2d) / defs.FRAME_RATE, 0)
            #self.vel_y = max(self.vel_y - drag_acceleration * (self.vel_y / velocity_magnitude) / defs.FRAME_RATE, 0)
            self.vel_z = max(self.vel_z - drag_acceleration * (self.vel_z / velocity_magnitude_2d) / defs.FRAME_RATE, 0)

        # apply gravity
        if self.pos_y > 0:
            self.vel_y -= defs.GRAVITY / defs.FRAME_RATE
        elif velocity_magnitude_2d > defs.VELOCITY_THRESHOLD: # apply rolling resistance
            self.vel_x *= max((defs.SURFACE_ROLLING_RESISTANCE[surface] - (1 - defs.SURFACE_ROLLING_RESISTANCE[surface])) / defs.FRAME_RATE, 0)
            self.vel_z *= max((defs.SURFACE_ROLLING_RESISTANCE[surface] - (1 - defs.SURFACE_ROLLING_RESISTANCE[surface])) / defs.FRAME_RATE, 0)
            pass
        else:
            self.vel_x = 0
            self.vel_z = 0 


        # apply accel on green
        #if surface == "green":
        #    angle, gradient = self.game.map.get_surface_gradient(self.pos_x, self.pos_z)





