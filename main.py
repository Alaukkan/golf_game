import pygame
import sys
import math

import scripts.definitions as defs
from scripts.entities import Player
from scripts.map import Map
from scripts.clubs import clubs
from scripts.courses import courses
from scripts.utils import load_image, load_images, Animation

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.display = pygame.Surface(defs.RESOLUTION, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("graphics/fonts/PressStart2P-vaV7.ttf", defs.FONT_SIZE)

        self.options = ["1 Player game", "2 Player game"]
        self.pointer = 0

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.pointer = max(self.pointer - 1, 0)
                if event.key == pygame.K_DOWN:
                    self.pointer = min(self.pointer + 1, len(self.options) - 1)
                if event.key == pygame.K_c:
                    self.select()

    def render(self):
        for i, option in enumerate(self.options):
            text = self.font.render(option, False, (255, 255, 255)) 
            self.display.blit(text, (defs.MENU_TEXT_POS[0], defs.MENU_TEXT_POS[1] + (defs.FONT_SIZE + 2) * i))

        pointer = self.font.render(">", False, (255, 255, 255))
        self.display.blit(pointer, (defs.MENU_TEXT_POS[0] - (defs.FONT_SIZE + 2), defs.MENU_TEXT_POS[1] + (defs.FONT_SIZE + 2) * self.pointer))

    def select(self):
        self.running = False
        Game(screen, self.pointer + 1).run()

    def run(self):
        self.running = True

        while self.running:

            self.display.fill((0, 0, 0))

            self.render()

            self.check_input()

            self.screen.blit(pygame.transform.scale(self.display, (defs.RESOLUTION[0] * defs.PIXEL_SIZE, defs.RESOLUTION[1] * defs.PIXEL_SIZE)), (0, 0))

            pygame.display.update()
            self.clock.tick(defs.FRAME_RATE)

            

class Game():

    def __init__(self, screen, no_players):
        
        self.screen = screen
        self.display = pygame.Surface(defs.GAME_RESOLUTION, pygame.SRCALPHA)
        self.hud_display = pygame.Surface(defs.HUD_RESOLUTION, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("graphics/fonts/PressStart2P-vaV7.ttf", defs.FONT_SIZE)

        self.images = {
            "ball/00" : load_image("ball/00.png"),
            "ball/01" : load_image("ball/01.png"),
            "ball/02" : load_image("ball/02.png"),
            "ball/03" : load_image("ball/03.png"),
            "ball/04" : load_image("ball/04.png"),
            "ball/05" : load_image("ball/05.png"),
            "ball/06" : load_image("ball/06.png"),
            "ball/10" : load_image("ball/10.png"),
            "trees/01" : load_image("trees/01.png"),
            "trees/02" : load_image("trees/02.png"),
            "crosshair/00" : load_image("crosshair/00.png"),
            "HUD/hit_indicator": load_image("HUD/hit_indicator.png"),
            "HUD/hit_bar" : load_image("HUD/hit_bar.png"),
            "HUD/background" : load_image("HUD/background.png"),
            "HUD/distance_left" : load_image("HUD/distance_left.png"),
            "HUD/shot_distance" : load_image("HUD/shot_distance.png"),
            "HUD/wind_direction" : load_image("HUD/wind_direction.png"),
            "HUD/ball" : load_image("HUD/ball.png"),
            "HUD/spin_marker" : load_image("HUD/spin_marker.png"),
            "HUD/PT" : load_image("HUD/PT.png"),
            "HUD/SW" : load_image("HUD/SW.png"),
            "HUD/9I" : load_image("HUD/SW.png"),
            "HUD/7I" : load_image("HUD/SW.png"),
            "HUD/5I" : load_image("HUD/SW.png"),
            "HUD/3I" : load_image("HUD/SW.png"),
            "HUD/3W" : load_image("HUD/1W.png"),
            "HUD/1W" : load_image("HUD/1W.png"),
            "surface/fairway" : load_image("surface/fairway.png"),
            "surface/tee" : load_image("surface/tee.png"),
            "surface/sand" : load_image("surface/sand.png"),
            "surface/rough" : load_image("surface/rough.png"),
            "birdie" : Animation(load_images("animations/birdie"), img_dur=3, loop=False),
            "par" : Animation(load_images("animations/par"), img_dur=3, loop=False),
            "bogey" : Animation(load_images("animations/bogey"), img_dur=3, loop=False),
            "double_bogey" : Animation(load_images("animations/double_bogey"), img_dur=3, loop=False)
        }

        for i in range(8):
            for j in range(1,5):
                self.images[f"green_arrows/{i}{j}"] = load_image(f"courses/green_arrows/{i}{j}.png")

        self.sfx = {
            "hit_ball" : pygame.mixer.Sound("sfx/hit.wav"),
            "green" : pygame.mixer.Sound("sfx/green.wav"),
            "sand" : pygame.mixer.Sound("sfx/sand.wav"),
            "fairway" : pygame.mixer.Sound("sfx/fairway.wav"),
            "rough" : pygame.mixer.Sound("sfx/rough.wav"),
            "OB" : pygame.mixer.Sound("sfx/rough.wav"),
            "hole" : pygame.mixer.Sound("sfx/in_hole.wav")
        }

        self.pointer = 0
        self.curr_animation = None

        self.assets = {
            "hitting_meter" : 0
        }

        self.sfx["hole"].set_volume(1)
        
        self.hole = 1
        self.map = Map(self, courses[f"{self.hole:02}"])

        self.players = []
        for i in range(no_players):
            self.players.append(Player(self, ["PT", "SW", "9I", "7I", "5I", "3I", "3W", "1W"]))
        
        self.player = self.players[0]
        self.state = defs.CHOOSE_PLAYER
        self.surface_check_timer = 0

    
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if not self.player.ball.is_moving:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.turn_left = True
                    if event.key == pygame.K_RIGHT:
                        self.player.turn_right = True
                        
                    if event.key == pygame.K_UP:
                        if self.state == defs.CHOOSING_SWINGSPEED:
                            self.pointer = min(self.pointer + 1, len(defs.SWINGSPEED_OPTIONS) - 1)

                        elif self.state == defs.CHOOSING_CLUB:
                            if not self.player.ball.on_green:
                                self.player.club = min(self.player.club + 1, len(self.player.clubs) - 1)

                        elif self.state == defs.CHOOSING_BACKSPIN:
                            self.pointer = min(self.pointer + 1, 2)

                    if event.key == pygame.K_DOWN:
                        if self.state == defs.CHOOSING_SWINGSPEED:
                            self.pointer = max(self.pointer - 1, 0)

                        elif self.state == defs.CHOOSING_CLUB:
                            if not self.player.ball.on_green:
                                self.player.club = max(self.player.club - 1, 0)

                        elif self.state == defs.CHOOSING_BACKSPIN:
                            self.pointer = max(self.pointer - 1, -2)

                    if event.key == pygame.K_x:
                        if not self.player.ball.on_green and self.state == defs.CHOOSING_SWINGSPEED:
                            self.state = defs.CHECKING_SURFACE
                            self.surface_check_timer = defs.CHECKING_SURFACE_TIMER

                        elif self.state < defs.CHOOSING_BACKSWING:
                            self.state = max(self.state - 1, 1)

                    if event.key == pygame.K_c:
                        if self.state == defs.CHOOSING_SWINGSPEED:
                            self.player.swingspeed = defs.SWINGSPEED_OPTIONS[self.pointer][1]
                            self.player.choose_club()
                            self.pointer = 0

                        elif self.state == defs.CHOOSING_CLUB:
                            if self.player.ball.on_green:
                                self.state += 1

                        elif self.state == defs.CHOOSING_BACKSPIN:
                            self.player.spin = self.pointer
                            self.pointer = 0

                        elif self.state == defs.CHOOSING_BACKSWING:
                            self.player.backswing = self.assets["hitting_meter"] / defs.MAX_BACKSWING
                            if self.player.club == 0:
                                self.player.hit_ball()
                                self.state += 1

                        elif self.state == defs.CHOOSING_SIDESPIN:
                            self.player.hit_ball()
                        
                        self.state += 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.turn_left = False
                    if event.key == pygame.K_RIGHT:
                        self.player.turn_right = False
                
    def render_hud(self):
        # render background "boxes"
        pos = list(defs.ICON_BACKGROUND_POS)    
        img = pygame.transform.scale(self.images["HUD/background"], (defs.HUD_RESOLUTION[0] - 4, (defs.HUD_RESOLUTION[0] - 4) * 0.65))
        for i in range(4):
            self.hud_display.blit(img, pos)
            pos[1] += (defs.HUD_RESOLUTION[0] - 4) * 0.65 + 1
        img = pygame.transform.scale(self.images["HUD/background"], (defs.HUD_RESOLUTION[0] - 4, defs.HUD_RESOLUTION[0] - 4))
        self.hud_display.blit(img, pos)

        # render hole info
        text = (f"HOLE{self.hole}")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.hud_display.blit(distance, defs.HOLE_NUMBER_POS)
        text = (f"PAR {self.map.par}")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.hud_display.blit(distance, (defs.HOLE_NUMBER_POS[0], defs.HOLE_NUMBER_POS[1] + 9))
        text = (f"{self.map.length:3}m")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.hud_display.blit(distance, (defs.HOLE_NUMBER_POS[0], defs.HOLE_NUMBER_POS[1] + 18))

        # render shot distance
        if self.player.ball.is_moving:
            self.hud_display.blit(self.images["HUD/shot_distance"], defs.DISTANCE_IMG_POS)

            text = (f"{int(math.sqrt((self.player.ball.pos_x - self.player.ball.last_pos[0]) ** 2 + (self.player.ball.pos_z - self.player.ball.last_pos[1]) ** 2)):3}m")
            distance = self.font.render(text, False, (255, 255, 255)) 
            self.hud_display.blit(distance, defs.DISTANCE_TEXT_POS)

        # render distance to pin
        else:
            self.hud_display.blit(self.images["HUD/distance_left"], defs.DISTANCE_IMG_POS)

            text = (f"{int(self.player.ball.distance_from_pin()):3}m")
            distance = self.font.render(text, False, (255, 255, 255)) 
            self.hud_display.blit(distance, defs.DISTANCE_TEXT_POS)

        # render wind direction
        if self.map.wind[1] > 0:
            wind_direction = pygame.transform.rotate(self.images["HUD/wind_direction"], math.degrees(self.map.wind[0]))
            self.hud_display.blit(wind_direction, defs.WIND_DIRECTION_POS)

        # render windspeed
        text = (f"{int(self.map.wind[1])}m/s")
        distance = self.font.render(text, False, (255, 255, 255)) 
        self.hud_display.blit(distance, defs.WIND_TEXT_POS)

        # render player stroke count
        distance = self.font.render("SHOTS", False, (255, 255, 255)) 
        self.hud_display.blit(distance, (defs.PLAYER_STROKES_POS[0], defs.PLAYER_STROKES_POS[1] - (defs.FONT_SIZE + 2)))
        for i, player in enumerate(self.players):
            text = (f"P{i + 1}:{player.strokes:2}")
            if player == self.player:
                color = (255, 255, 152)
            else:
                color = (255, 255, 255)
            strokes = self.font.render(text, False, color) 
            self.hud_display.blit(strokes, (defs.PLAYER_STROKES_POS[0], defs.PLAYER_STROKES_POS[1] + 10 * i))

        if not self.player.ball.is_moving:
            # render swingspeed options
            if self.state == defs.CHOOSING_SWINGSPEED:
                for i in range(len(defs.SWINGSPEED_OPTIONS)):
                    option = self.font.render(defs.SWINGSPEED_OPTIONS[i][0], False, (255, 255, 255)) 
                    self.hud_display.blit(option, (defs.SWINGSPEED_OPTIONS_POS[0], defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * i))
                
                club_distance = self.font.render("SWING", False, (255, 255, 255)) 
                self.hud_display.blit(club_distance, (defs.SWINGSPEED_OPTIONS_POS[0] - defs.FONT_SIZE, defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 2) * (i + 1)))

                pointer = self.font.render(">", False, (255, 255, 255))
                self.hud_display.blit(pointer, (defs.SWINGSPEED_OPTIONS_POS[0] - defs.FONT_SIZE, defs.SWINGSPEED_OPTIONS_POS[1] - (defs.FONT_SIZE + 1) * self.pointer))
            
            # render club options
            elif self.state == defs.CHOOSING_CLUB:
                img = self.images[f"HUD/{self.player.clubs[self.player.club]}"]
                self.hud_display.blit(img, defs.CLUB_IMG_POS)

                text = (f"{'<' if self.player.club != 0 else ' '}{self.player.clubs[self.player.club]}"
                        f"{'>' if self.player.club < len(self.player.clubs) - 1 and not self.player.ball.on_green else ' '}")
                club = self.font.render(text, False, (255, 255, 255))
                self.hud_display.blit(club, defs.CLUB_TEXT_POS)

                club = clubs[self.player.clubs[self.player.club]]
                text = (f"{int(club['distance'] * self.player.swingspeed):3}m")
                club_distance = self.font.render(text, False, (255, 255, 255)) 
                self.hud_display.blit(club_distance, defs.CLUB_DISTANCE_POS)
            
            # Render spin choosing
            elif self.state == defs.CHOOSING_BACKSPIN:
                text = ("SPIN")
                spin = self.font.render(text, False, (255, 255, 255)) 
                self.hud_display.blit(spin, defs.SPIN_TEXT_POS)

                img = self.images["HUD/ball"]
                self.hud_display.blit(img, defs.SPIN_MARKER_POS)

                img = self.images["HUD/spin_marker"]
                self.hud_display.blit(img, (defs.SPIN_MARKER_POS[0], defs.SPIN_MARKER_POS[1] - self.pointer * 4))

                text = defs.SPIN_OPTIONS[self.pointer]
                spin = self.font.render(text, False, (255, 255, 255)) 
                self.hud_display.blit(spin, (defs.SPIN_TEXT_POS[0] - 4, defs.SPIN_TEXT_POS[1] + 20))


    def choose_player(self):
        self.assets["hitting_meter"] = 0
        self.player = max(self.players, key=lambda x:(x.ball.distance_from_pin()))

        if self.player.ball.in_hole:
            self.player = min(self.players, key=lambda x:(x.strokes))
            self.next_map()

        self.player.set_new_direction()


    def ball_in_hole(self):

        self.sfx["hole"].play()
        result = self.player.strokes - int(self.map.par)

        if self.player.strokes == 1:
            self.curr_animation = self.images["birdie"].copy()
        elif result == -2:
            self.curr_animation = self.images["birdie"].copy()
        elif result == -1:
            self.curr_animation = self.images["birdie"].copy()
        elif result == 0:
            self.curr_animation = self.images["par"].copy()
        elif result == 1:
            self.curr_animation = self.images["bogey"].copy()
        elif result == 2:
            self.curr_animation = self.images["double_bogey"].copy()
        elif result == 3:
            self.curr_animation = self.images["double_bogey"].copy()
        elif result >= 4:
            self.curr_animation = self.images["double_bogey"].copy()
        
        self.state = defs.PLAYING_ANIMATION

        self.player.scorecard.append(self.player.strokes)

    def next_map(self):
        self.hole += 1
        self.map = Map(self, courses[f"{self.hole:02}"])
        for player in self.players:
            player.new_ball()
            player.strokes = 0

    def run(self):
        pygame.mixer.music.load('music/01.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.music_playing = True

        counter = 0
        while True:
            self.display.fill((0, 0, 0))
            self.hud_display.fill((0, 0, 0))

            counter = (counter + 1)
            if counter // defs.FRAME_RATE == 1:# or True:
                counter = 0
                print(  f"player direction:  {math.degrees(self.player.direction):.2f}\n"
                        f"ball position:     {self.player.ball.pos_x:.2f} {self.player.ball.pos_y:.2f} {self.player.ball.pos_z:.2f}\n"
                        f"ball velocity:     {self.player.ball.vel_x:.2f} {self.player.ball.vel_y:.2f} {self.player.ball.vel_z:.2f}\n"
                        f"distance from pin: {self.player.ball.distance_from_pin():.2f}\n"
                        f"wind: {self.map.wind[0]}   {self.map.wind[1]} m/s\n"
                        f"state: {self.state}\n"
                        f"Timer: {self.surface_check_timer}\n")

            if self.state == defs.CHOOSE_PLAYER:
                self.choose_player()
                self.state += 1

            self.offset = [self.player.ball.pos_x + defs.GAME_RESOLUTION[0] / 2, self.player.ball.pos_z + defs.GAME_RESOLUTION[1] / 2]

            self.map.render(self.display, self.offset)

            self.player.update()
            self.player.ball.update()


            self.map.render_map_objects(self.display, self.offset)

            render_order = sorted(self.players, key=lambda x:(x.ball.distance_from_pin()))
            for player in render_order:
                player.ball.render(self.display, [defs.GAME_RESOLUTION[0] / 2, defs.GAME_RESOLUTION[1] / 2])

            self.player.render(self.display, self.offset)

            self.render_hud()
            
            if self.state == defs.PLAYING_ANIMATION:
                self.display.blit(self.curr_animation.img(), defs.ANIMATION_POS)
                self.curr_animation.update()

                if self.curr_animation.done:
                    self.state = defs.CHOOSE_PLAYER

            if defs.BALL_MOVING > self.state > defs.CHOOSING_BACKSPIN:
                if self.music_playing:
                    pygame.mixer.music.pause()
                    self.music_playing = False
            else:
                if not self.music_playing:
                    pygame.mixer.music.unpause()
                    self.music_playing = True

            self.check_input()

            self.screen.blit(pygame.transform.scale(self.display, (defs.GAME_RESOLUTION[0] * defs.PIXEL_SIZE * defs.GAME_RESOLUTION[0] / defs.GAME_RESOLUTION[1], 
                                                                   defs.GAME_RESOLUTION[1] * defs.PIXEL_SIZE * defs.GAME_RESOLUTION[0] / defs.GAME_RESOLUTION[1])), 
                                                                   (defs.HUD_RESOLUTION[0] * defs.PIXEL_SIZE, 0))
            self.screen.blit(pygame.transform.scale(self.hud_display, (defs.HUD_RESOLUTION[0] * defs.PIXEL_SIZE, defs.HUD_RESOLUTION[1] * defs.PIXEL_SIZE)), (0, 0))

            pygame.display.update()
            self.clock.tick(defs.FRAME_RATE)

if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("Golf game")
    screen = pygame.display.set_mode((defs.RESOLUTION[0] * defs.PIXEL_SIZE, defs.RESOLUTION[1] * defs.PIXEL_SIZE))
    
    Menu(screen).run()
    