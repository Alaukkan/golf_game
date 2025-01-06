import pygame
import sys
import math

import scripts.definitions as defs
from scripts.entities import Player
from scripts.entities import Ball
from scripts.map import Map
from scripts.clubs import clubs


MAP = 0
HITTING = 1

class Game():

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Golf game")
        self.screen = pygame.display.set_mode((defs.RESOLUTION[0] * defs.PIXEL_SIZE, defs.RESOLUTION[1] * defs.PIXEL_SIZE))
        self.display = pygame.Surface((defs.RESOLUTION[0], defs.RESOLUTION[1]), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = {

        }

        self.player = Player(self, ["1W", "PT"])
        self.ball = Ball(self, 0, 0)
        self.map = Map(self)
    
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == MAP:
                self.check_input_map(event)
            if self.state == HITTING:
                self.check_input_map(event)
                self.check_input_hitting(event)

    def check_input_map(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.turn_left = True
            if event.key == pygame.K_RIGHT:
                self.player.turn_right = True
            if event.key == pygame.K_UP:
                self.player.club = min(self.player.club + 1, len(self.player.clubs) - 1)
            if event.key == pygame.K_DOWN:
                self.player.club = max(self.player.club - 1, 0)
            if event.key == pygame.K_x:
                # back
                pass
            if event.key == pygame.K_c:
                # select
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.turn_left = False
            if event.key == pygame.K_RIGHT:
                self.player.turn_right = False

    def check_input_hitting(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                # back
                pass
            if event.key == pygame.K_c:
                self.player.hit_ball()
                pass

    def run(self):
        counter = 0
        self.state = HITTING
        while True:
            counter = (counter + 1)
            if counter // 30 == 1:
                counter = 0
                print(  f"player direction: {self.player.direction:.2f}\n"
                        f"ball position:    {self.ball.pos_x:.2f} {self.ball.pos_y:.2f} {self.ball.pos_z:.2f}\n"
                        f"ball velocity:    {self.ball.vel_x:.2f} {self.ball.vel_y:.2f} {self.ball.vel_z:.2f}\n"
                        f"distance: {math.sqrt(self.ball.pos_x ** 2 + self.ball.pos_y ** 2 + self.ball.pos_z ** 2):.2f}")

            self.player.update()
            self.ball.update()

            self.ball.render(self.display, (-40, 0))

            self.check_input()


            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_size())), (0, 0))
            pygame.display.update()
            self.clock.tick(defs.FRAME_RATE)

Game().run()
    
            