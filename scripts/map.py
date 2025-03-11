import pygame
import random
import time
import math

import scripts.definitions as defs

from scripts.tree import Tree
from scripts.utils import load_image, load_hole

class Map():

    def __init__(self, game, course, hole_num):
        random.seed(time.time())
        self.game = game

        hole = load_hole(course, hole_num)
        self.img = load_image(f"courses/{hole['number']}.png")
        self.img_size = self.img.get_size()
        self.flag_img = load_image(f"courses/flag/01.png")
        self.hole_img = load_image(f"courses/flag/02.png")
        self.green_img = pygame.transform.scale(load_image(f"courses/greens/{hole['number']}.png"), defs.GAME_RESOLUTION)
        self.length = hole["length"]
        self.par = hole["par"]
        self.tee = hole["tee"]
        self.pin = hole["pin"][random.randint(0, len(hole["pin"]) - 1)]
        self.green = hole["green"]
        self.green_radius = hole["green_radius"]
        self.green_gradient = hole["green_gradient"]

        self.trees = []
        for tree in hole["trees"]:
            self.trees.append(Tree(self.game, tree["x"], tree["z"], tree["type"]))

        self.flag_offset = (-4, -7)
        self.hole_offset = (-3, -4)
        self.wind = [random.random() * 2 * math.pi, random.randint(0, defs.MAX_WINDSPEED)] # (angle, speed)

        self.game.course_pars.append(int(self.par))

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
    
    def check_tree_collisions(self, ball_x, ball_y, ball_z):
        for tree in self.trees:
            if tree.check_collision(ball_x, ball_y, ball_z):
                self.game.player.ball.in_tree = True
                self.game.player.ball.side_spin = 0
                return
            
        self.game.player.ball.in_tree = False
    
    def render(self, surf, offset):
        #if math.sqrt((-self.game.player.ball.pos_x - self.green[0])**2 + (-self.game.player.ball.pos_z - self.green[1])**2) < self.green_radius:
            #(abs(-self.game.ball.pos_x - self.green[0]) <= defs.GREEN_AREA_SIZE and abs(-self.game.ball.pos_z - self.green[1]) <= defs.GREEN_AREA_SIZE):
        if self.game.player.ball.on_green:
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
            for tree in self.trees:
                tree.render(surf, offset)
