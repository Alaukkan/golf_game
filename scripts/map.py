import pygame
import random
import time
import math

import scripts.definitions as defs

from scripts.utils import load_image

class Map():

    def __init__(self, game, course):
        random.seed(time.time())

        self.game = game
        self.img = load_image(f"courses/{course['number']}.png")
        self.img_size = self.img.get_size()
        self.flag_img = load_image(f"courses/flag/01.png")
        self.hole_img = load_image(f"courses/flag/02.png")
        self.green_img = pygame.transform.scale(load_image(f"courses/greens/{course['number']}.png"), defs.GAME_RESOLUTION)
        self.length = course["length"]
        self.par = course["par"]
        self.tee = course["tee"]
        self.pin = course["pin"][random.randint(0, len(course["pin"]) - 1)]
        self.green = course["green"]
        self.green_radius = course["green_radius"]
        self.green_gradient = course["green_gradient"]
        self.flag_offset = (-4, -7)
        self.hole_offset = (-3, -4)
        self.wind = [random.random() * 2 * math.pi, random.randint(0, defs.MAX_WINDSPEED)] # (angle, speed)

    def get_surface(self, x, y):
        surface_color = tuple(self.img.get_at((int(-x), int(-y))))[:3] if (-x > 0 and -x < self.img_size[0] and -y > 0 and -y < self.img_size[1]) else (0, 0, 0)
        # print(defs.COLOR_TO_SURFACE[surface_color])
        return defs.COLOR_TO_SURFACE[surface_color]
    
    def get_green_gradient(self, x, y):
        x = int((-x - self.green[0] + defs.GREEN_CAM_SIZE) / 8 * defs.GREEN_CAM_SCALE)
        y = int((-y - self.green[1] + defs.GREEN_CAM_SIZE) / 8 * defs.GREEN_CAM_SCALE)

        #print(x, y)
        #print(int(self.green_gradient[y][x][0]), int(self.green_gradient[y][x][1]))

        direction = int(self.green_gradient[y][x][0]) * math.pi / 4
        gradient = math.radians(defs.GREEN_GRADIENT[int(self.green_gradient[y][x][1])])
        return direction, gradient
    
    def render(self, surf, offset):
        if math.sqrt((-self.game.player.ball.pos_x - self.green[0])**2 + (-self.game.player.ball.pos_z - self.green[1])**2) < self.green_radius:
            #(abs(-self.game.ball.pos_x - self.green[0]) <= defs.GREEN_AREA_SIZE and abs(-self.game.ball.pos_z - self.green[1]) <= defs.GREEN_AREA_SIZE):
            self.game.player.ball.on_green = True
            surf.blit(self.green_img, (0, 0))
            self.render_green_arrows(surf)
        else:
            if -self.game.player.ball.pos_x < defs.GAME_RESOLUTION[0] / 2:
                offset[0] = 0
            if -self.game.player.ball.pos_x > self.game.map.img_size[0] - defs.GAME_RESOLUTION[0] / 2:
                offset[0] = defs.GAME_RESOLUTION[0] - self.game.map.img_size[0]
            if -self.game.player.ball.pos_z < defs.GAME_RESOLUTION[1] / 2:
                offset[1] = 0
            if -self.game.player.ball.pos_z > self.game.map.img_size[1] - defs.GAME_RESOLUTION[1] / 2:
                offset[1] = defs.GAME_RESOLUTION[1] - self.game.map.img_size[1]
            self.game.player.ball.on_green = False
            surf.blit(self.img, offset)

    def render_green_arrows(self, surf):
        for z_offset in range(len(self.green_gradient)):
            for x_offset in range(len(self.green_gradient[0])):
                if self.green_gradient[z_offset][x_offset] != '00':
                    surf.blit(self.game.images[f"green_arrows/{self.green_gradient[z_offset][x_offset]}"], (x_offset * 8, (defs.GAME_RESOLUTION[1] - defs.GAME_RESOLUTION[0]) / 2 +  z_offset * 8))


    def render_map_objects(self, surf, offset):
        if self.game.player.ball.on_green:
            render_offset = (int(round(defs.GAME_RESOLUTION[0] / 2 + defs.GREEN_CAM_SCALE * (self.pin[0] - self.green[0]) + self.hole_offset[0])), 
                             int(round(defs.GAME_RESOLUTION[1] / 2 + defs.GREEN_CAM_SCALE * (self.pin[1] - self.green[1]) + self.hole_offset[1])))
            surf.blit(self.hole_img, render_offset)
        else:
            render_offset = (offset[0] + int(round(self.pin[0])) + self.flag_offset[0], offset[1] + int(round(self.pin[1])) + self.flag_offset[1])
            surf.blit(self.flag_img, render_offset)
