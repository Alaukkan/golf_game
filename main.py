import pygame
import sys
import math

import scripts.definitions as defs
from scripts.entities import Player
from scripts.entities import Ball
from scripts.map import Map
from scripts.clubs import clubs
from scripts.courses import courses
from scripts.utils import load_image


class Game():

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Golf game")
        self.screen = pygame.display.set_mode((defs.RESOLUTION[0] * defs.PIXEL_SIZE, defs.RESOLUTION[1] * defs.PIXEL_SIZE))
        self.display = pygame.Surface(defs.GAME_RESOLUTION, pygame.SRCALPHA)
        self.ui_display = pygame.Surface(defs.UI_RESOLUTION, pygame.SRCALPHA)


        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("graphics/fonts/PressStart2P-vaV7.ttf", defs.FONT_SIZE)

        self.assets = {
            "state" : defs.MAP,
            "choosing" : defs.SWINGSPEED,
            "pointer" : 0,
            "images" : {
                "sprites/ball/00" : load_image("sprites/ball/00.png"),
                "sprites/ball/01" : load_image("sprites/ball/01.png"),
                "sprites/ball/02" : load_image("sprites/ball/02.png"),
                "sprites/ball/03" : load_image("sprites/ball/03.png"),
                "sprites/ball/04" : load_image("sprites/ball/04.png"),
                "sprites/crosshair/00" : load_image("sprites/crosshair/00.png"),
                "sprites/UI/background" : load_image("sprites/UI/background.png"),
                "sprites/UI/ball" : load_image("sprites/UI/ball.png"),
                "sprites/UI/spin_marker" : load_image("sprites/UI/spin_marker.png"),
                "sprites/UI/PT" : load_image("sprites/UI/PT.png"),
                "sprites/UI/SW" : load_image("sprites/UI/SW.png"),
                "sprites/UI/9I" : load_image("sprites/UI/SW.png"),
                "sprites/UI/1W" : load_image("sprites/UI/1W.png"),
            }
        }

        for i in range(8):
            for j in range(1,5):
                self.assets["images"][f"green_arrows/{i}{j}"] = load_image(f"sprites/courses/green_arrows/{i}{j}.png")

        self.map = Map(self, courses["01"])
        self.player = Player(self, ["PT", "SW", "9I", "3I", "1W"])
        self.players = []
        self.players.append(self.player)

    
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.assets["state"] == defs.MAP:
                self.check_input_map(event)
            if self.assets["state"] == defs.HITTING:
                self.check_input_hitting(event)

    def check_input_map(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.turn_left = True
            if event.key == pygame.K_RIGHT:
                self.player.turn_right = True
            if event.key == pygame.K_UP:
                if self.assets["choosing"] == defs.SWINGSPEED:
                    self.assets["pointer"] = min(self.assets["pointer"] + 1, len(defs.SWINGSPEED_OPTIONS) - 1)
                    self.player.swingspeed = defs.SWINGSPEED_OPTIONS[self.assets["pointer"]][1]
                elif self.assets["choosing"] == defs.CLUB:
                    if not self.player.ball.on_green:
                        self.player.club = min(self.player.club + 1, len(self.player.clubs) - 1)

            if event.key == pygame.K_DOWN:
                if self.assets["choosing"] == defs.SWINGSPEED:
                    self.assets["pointer"] = max(self.assets["pointer"] - 1, 0)
                    self.player.swingspeed = defs.SWINGSPEED_OPTIONS[self.assets["pointer"]][1]
                elif self.assets["choosing"] == defs.CLUB:
                    if not self.player.ball.on_green:
                        self.player.club = max(self.player.club - 1, 0)

            if event.key == pygame.K_x:
                self.assets["choosing"] = max(self.assets["choosing"] - 1, 0)

            if event.key == pygame.K_c:
                if self.assets["choosing"] == defs.SPIN:
                    self.assets["choosing"] = 0
                    self.player.hit_ball()
                else:
                    self.assets["choosing"] += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.turn_left = False
            if event.key == pygame.K_RIGHT:
                self.player.turn_right = False

    def check_input_hitting(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.assets["choosing"] = 0
                self.assets["pointer"] = 0
                self.assets["state"] = defs.MAP
                pass
            if event.key == pygame.K_c:
                self.player.hit_ball()
                pass
    
    def render_ui(self):
        #for i in range(2):
            #self.ui_display.blit(self.assets["images"]["sprites/UI/background"], (defs.ICON_BACKGROUND_POS[0], defs.ICON_BACKGROUND_POS[1] + int(defs.ICON_BACKGROUND_POS[1] * 3.2 * i)))

        text = (f"{int(self.player.ball.distance_from_pin())}m")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.ui_display.blit(distance, defs.DISTANCE_LEFT_TEXT_POS)

        if self.assets["choosing"] == defs.SWINGSPEED:
            for i in range(len(defs.SWINGSPEED_OPTIONS)):
                option = self.font.render(defs.SWINGSPEED_OPTIONS[i][0], False, (255, 255, 255)) 
                self.ui_display.blit(option, (defs.SWINGSPEED_OPTIONS_POS[0], defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * i))
            pointer = self.font.render(">", False, (255, 255, 255))
            self.ui_display.blit(pointer, (defs.SWINGSPEED_OPTIONS_POS[0] - defs.FONT_SIZE, defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * self.assets["pointer"]))

        elif self.assets["choosing"] == defs.CLUB:
            text = (f"{'<' if self.player.club != 0 else ' '}{self.player.clubs[self.player.club]}"
                    f"{'>' if self.player.club < len(self.player.clubs) - 1 and not self.player.ball.on_green else ' '}")
            club = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(club, defs.CLUB_TEXT_POS)

            club = clubs[self.player.clubs[self.player.club]]
            text = (f"{int(club['distance'] * self.player.swingspeed)}m")
            club_distance = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(club_distance, defs.CLUB_DISTANCE_POS)
        
        elif self.assets["choosing"] == defs.SPIN:
            pass



    def run(self):
        counter = 0
        while True:
            self.display.fill((0, 0, 0))
            self.ui_display.fill((0, 0, 0))

            counter = (counter + 1)
            if counter // 30 == 1:
                counter = 0
                print(  f"player direction:  {math.degrees(self.player.direction):.2f}\n"
                        f"ball position:     {self.player.ball.pos_x:.2f} {self.player.ball.pos_y:.2f} {self.player.ball.pos_z:.2f}\n"
                        f"ball velocity:     {self.player.ball.vel_x:.2f} {self.player.ball.vel_y:.2f} {self.player.ball.vel_z:.2f}\n"
                        f"distance from pin: {self.player.ball.distance_from_pin():.2f}\n"
                        f"wind: {self.map.wind[0]}   {self.map.wind[1]} m/s\n")

            self.offset = (self.player.ball.pos_x + defs.GAME_RESOLUTION[0] / 2, self.player.ball.pos_z + defs.GAME_RESOLUTION[1] / 2)

            self.map.render(self.display, self.offset, self.assets["state"])

            self.player.update()
            self.player.ball.update()

            self.map.render_map_objects(self.display, self.offset)

            self.player.ball.render(self.display, (defs.GAME_RESOLUTION[0] / 2, defs.GAME_RESOLUTION[1] / 2))

            self.player.render(self.display, (defs.GAME_RESOLUTION[0] / 2, defs.GAME_RESOLUTION[1] / 2))

            self.render_ui()

            self.check_input()

            self.screen.blit(pygame.transform.scale(self.display, (defs.GAME_RESOLUTION[0] * defs.PIXEL_SIZE, defs.GAME_RESOLUTION[1] * defs.PIXEL_SIZE)), (defs.UI_RESOLUTION[0] * defs.PIXEL_SIZE, 0))
            self.screen.blit(pygame.transform.scale(self.ui_display, (defs.UI_RESOLUTION[0] * defs.PIXEL_SIZE, defs.UI_RESOLUTION[1] * defs.PIXEL_SIZE)), (0, 0))

            pygame.display.update()
            self.clock.tick(defs.FRAME_RATE)

Game().run()
    
            