import pygame
import sys
import math

import scripts.definitions as defs
from scripts.entities import Player
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
            "hole" : 1,
            "state" : defs.MAP,
            "choosing" : defs.SWINGSPEED,
            "pointer" : 0,
            "hitting" : 0,
            "hitting_meter" : 0,
            "images" : {
                "ball/00" : load_image("ball/00.png"),
                "ball/01" : load_image("ball/01.png"),
                "ball/02" : load_image("ball/02.png"),
                "ball/03" : load_image("ball/03.png"),
                "ball/04" : load_image("ball/04.png"),
                "crosshair/00" : load_image("crosshair/00.png"),
                "UI/hit_indicator": load_image("UI/hit_indicator.png"),
                "UI/hit_bar" : load_image("UI/hit_bar.png"),
                "UI/background" : load_image("UI/background.png"),
                "UI/distance_left" : load_image("UI/distance_left.png"),
                "UI/shot_distance" : load_image("UI/shot_distance.png"),
                "UI/wind_direction" : load_image("UI/wind_direction.png"),
                "UI/ball" : load_image("UI/ball.png"),
                "UI/spin_marker" : load_image("UI/spin_marker.png"),
                "UI/PT" : load_image("UI/PT.png"),
                "UI/SW" : load_image("UI/SW.png"),
                "UI/9I" : load_image("UI/SW.png"),
                "UI/3I" : load_image("UI/SW.png"),
                "UI/1W" : load_image("UI/1W.png"),
                
            }
        }
        for i in range(8):
            for j in range(1,5):
                self.assets["images"][f"green_arrows/{i}{j}"] = load_image(f"courses/green_arrows/{i}{j}.png")

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
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
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
                if self.assets["choosing"] == defs.SPIN or (self.assets["choosing"] == defs.CLUB and self.player.ball.on_green):
                    self.assets["choosing"] = 0
                    self.assets["state"] = defs.HITTING
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

            if event.key == pygame.K_c:
                self.assets["hitting"] += 1
                if self.assets["hitting"] == 2:
                    self.player.backswing = self.assets["hitting_meter"] / defs.MAX_BACKSWING
                elif self.assets["hitting"] == 3:
                    self.player.ball.spin = -math.radians(self.assets["hitting_meter"])
                    self.player.hit_ball()
                    self.assets["state"] = defs.MAP
                
    def render_ui(self):
        # render background "boxes"
        pos = list(defs.ICON_BACKGROUND_POS)    
        img = pygame.transform.scale(self.assets["images"]["UI/background"], (defs.UI_RESOLUTION[0] - 4, (defs.UI_RESOLUTION[0] - 4) * 0.65))
        for i in range(4):
            self.ui_display.blit(img, pos)
            pos[1] += (defs.UI_RESOLUTION[0] - 4) * 0.65 + 1
        img = pygame.transform.scale(self.assets["images"]["UI/background"], (defs.UI_RESOLUTION[0] - 4, defs.UI_RESOLUTION[0] - 4))
        self.ui_display.blit(img, pos)

        # render hole info
        text = (f"H:{self.assets['hole']:02}")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.ui_display.blit(distance, defs.HOLE_NUMBER_POS)
        text = (f"{self.map.length:3}m")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.ui_display.blit(distance, defs.HOLE_INFO_POS)

        # render shot distance
        if self.player.ball.is_moving:
            self.ui_display.blit(self.assets["images"]["UI/shot_distance"], defs.DISTANCE_IMG_POS)

            text = (f"{int(math.sqrt((self.player.ball.pos_x - self.player.ball.last_pos[0]) ** 2 + (self.player.ball.pos_z - self.player.ball.last_pos[1]) ** 2)):3}m")
            distance = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(distance, defs.DISTANCE_TEXT_POS)

        # render distance to pin
        else:
            self.ui_display.blit(self.assets["images"]["UI/distance_left"], defs.DISTANCE_IMG_POS)

            text = (f"{int(self.player.ball.distance_from_pin()):3}m")
            distance = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(distance, defs.DISTANCE_TEXT_POS)

        # render wind direction
        if self.map.wind[1] > 0:
            wind_direction = pygame.transform.rotate(self.assets["images"]["UI/wind_direction"], math.degrees(self.map.wind[0]))
            self.ui_display.blit(wind_direction, defs.WIND_DIRECTION_POS)

        # render windspeed
        text = (f"{int(self.map.wind[1])}m/s")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.ui_display.blit(distance, defs.WIND_TEXT_POS)

        # render player stroke count
        for i in range(len(self.players)):
            text = (f"P{i + 1}:{self.players[i].strokes:2}")
            strokes = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(strokes, (defs.PLAYER_STROKES_POS[0], defs.PLAYER_STROKES_POS[1] + 10 * i))

        # render swingspeed options
        if self.assets["choosing"] == defs.SWINGSPEED:
            for i in range(len(defs.SWINGSPEED_OPTIONS)):
                option = self.font.render(defs.SWINGSPEED_OPTIONS[i][0], False, (255, 255, 255)) 
                self.ui_display.blit(option, (defs.SWINGSPEED_OPTIONS_POS[0], defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * i))
            
            club_distance = self.font.render("SWING", False, (255, 255, 255)) 
            self.ui_display.blit(club_distance, (defs.SWINGSPEED_OPTIONS_POS[0] - defs.FONT_SIZE, defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 2) * (i + 1)))

            pointer = self.font.render(">", False, (255, 255, 255))
            self.ui_display.blit(pointer, (defs.SWINGSPEED_OPTIONS_POS[0] - defs.FONT_SIZE, defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * self.assets["pointer"]))
        
        # render club options
        elif self.assets["choosing"] == defs.CLUB:
            img = self.assets["images"][f"UI/{self.player.clubs[self.player.club]}"]
            self.ui_display.blit(img, defs.CLUB_IMG_POS)

            text = (f"{'<' if self.player.club != 0 else ' '}{self.player.clubs[self.player.club]}"
                    f"{'>' if self.player.club < len(self.player.clubs) - 1 and not self.player.ball.on_green else ' '}")
            club = self.font.render(text, False, (255, 255, 255))
            self.ui_display.blit(club, defs.CLUB_TEXT_POS)

            club = clubs[self.player.clubs[self.player.club]]
            text = (f"{int(club['distance'] * self.player.swingspeed):3}m")
            club_distance = self.font.render(text, False, (255, 255, 255)) 
            self.ui_display.blit(club_distance, defs.CLUB_DISTANCE_POS)
        
        elif self.assets["choosing"] == defs.SPIN:
            pass

    def ball_in_hole(self):
        self.player.total_strokes = 0
        self.player.strokes = 0

        self.assets["hole"] += 1
        self.map = Map(self, courses[f"{self.assets['hole']:2}"])
        self.player.new_ball()
        

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

            self.offset = [self.player.ball.pos_x + defs.GAME_RESOLUTION[0] / 2, self.player.ball.pos_z + defs.GAME_RESOLUTION[1] / 2]

            self.map.render(self.display, self.offset)

            self.player.update()
            self.player.ball.update()

            self.map.render_map_objects(self.display, self.offset)

            self.player.ball.render(self.display, [defs.GAME_RESOLUTION[0] / 2, defs.GAME_RESOLUTION[1] / 2])

            self.player.render(self.display, self.offset)

            self.render_ui()

            self.check_input()

            self.screen.blit(pygame.transform.scale(self.display, (defs.GAME_RESOLUTION[0] * defs.PIXEL_SIZE * defs.GAME_RESOLUTION[0] / defs.GAME_RESOLUTION[1], defs.GAME_RESOLUTION[1] * defs.PIXEL_SIZE * defs.GAME_RESOLUTION[0] / defs.GAME_RESOLUTION[1])), (defs.UI_RESOLUTION[0] * defs.PIXEL_SIZE, 0))
            self.screen.blit(pygame.transform.scale(self.ui_display, (defs.UI_RESOLUTION[0] * defs.PIXEL_SIZE, defs.UI_RESOLUTION[1] * defs.PIXEL_SIZE)), (0, 0))

            pygame.display.update()
            self.clock.tick(defs.FRAME_RATE)

Game().run()
    