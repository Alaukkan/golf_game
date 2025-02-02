GAME_RESOLUTION = (200, 300)
HUD_RESOLUTION = (56, 200)
RESOLUTION = (HUD_RESOLUTION[0] + GAME_RESOLUTION[0] * GAME_RESOLUTION[0] / GAME_RESOLUTION[1], HUD_RESOLUTION[1])

PIXEL_SIZE = 3
FRAME_RATE = 30
FONT_SIZE = 8
GAME_SPEED = 1

BASE_IMG_PATH = "graphics/sprites/"
VIEWING_ANGLE = 70
CROSSHAIR_DISTANCE = 25

ICON_BACKGROUND_POS = (2, 4)

HOLE_NUMBER_POS = (int(HUD_RESOLUTION[0] * 0.2), int(HUD_RESOLUTION[1] * 0.05))
HOLE_INFO_POS = (int(HUD_RESOLUTION[0] * 0.2), int(HUD_RESOLUTION[1] * 0.12))

DISTANCE_IMG_POS = (int(HUD_RESOLUTION[0] * 0.2), int(HUD_RESOLUTION[1] * 0.22))
DISTANCE_TEXT_POS = (int(HUD_RESOLUTION[0] * 0.2), int(HUD_RESOLUTION[1] * 0.3))

WIND_DIRECTION_POS = (int(HUD_RESOLUTION[0] * 0.3) + 4, int(HUD_RESOLUTION[1] * 0.37) + 6)
WIND_TEXT_POS = (int(HUD_RESOLUTION[0] * 0.18), int(HUD_RESOLUTION[1] * 0.47))

PLAYER_STROKES_POS = (int(HUD_RESOLUTION[0] * 0.18), int(HUD_RESOLUTION[1] * 0.58))

SWINGSPEED_OPTIONS_POS = (int(HUD_RESOLUTION[0] * 0.3), int(HUD_RESOLUTION[1] * 0.9))

CLUB_IMG_POS = (int(HUD_RESOLUTION[0] * 0.01), int(HUD_RESOLUTION[1] * 0.68))
CLUB_TEXT_POS = (int(HUD_RESOLUTION[0] * 0.22), int(HUD_RESOLUTION[1] * 0.85))
CLUB_DISTANCE_POS = (CLUB_TEXT_POS[0], CLUB_TEXT_POS[1] + FONT_SIZE + 2)

SPIN_TEXT_POS = (int(HUD_RESOLUTION[0] * 0.22), int(HUD_RESOLUTION[1] * 0.75))
SPIN_MARKER_POS = (int(HUD_RESOLUTION[0] * 0.2), int(HUD_RESOLUTION[1] * 0.75))
                # 0,    1,    2,   -2,   -1
SPIN_OPTIONS = ["NO", "F1", "F2", "B2", "B1"]

COLOR_TO_SURFACE = {
    (52, 107, 191) : "water", # [346bbf]
    (199, 192, 58) : "sand", # [c7c03a]
    (34, 191, 77) : "green", # [22bf4d]
    (50, 168, 82) : "fairway", # [32a852]
    (25, 69, 37) : "rough", # [194525]
    (0, 0, 0) : "OB"
}

MAP = 0
HITTING = 1 
GREEN = 2

SWINGSPEED = 0
CLUB = 1
SPIN = 2

SWINGSPEED_OPTIONS = [("FAST", 1), ("MED.", 0.8), ("SLOW", 0.6)]
MAX_BACKSWING = 100
HITTING_METER_COLOR = (0, 150, 255)
HITTING_METER_POS = (int(GAME_RESOLUTION[0] * 0.65), int(GAME_RESOLUTION[1] * 0.9))
HITTING_METER_HEIGHT = 6

GREEN_CAM_SIZE = 20
GREEN_CAM_SCALE = GAME_RESOLUTION[0] / (2 * GREEN_CAM_SIZE)
HOLE_RADIUS = 0.25

MAX_WINDSPEED = 12
WIND_AFFECT = 5
GRAVITY = 9.81
BALL_ROLLING_RESISTANCE = 1
BALL_WIND_RESISTANCE = 0.5
AIR_DENSITY = 1.3
VELOCITY_THRESHOLD = 0.05

SURFACE_HARDNESS = {
    "water" : 0,
    "sand" : 0.01,
    "green" : 0.3,
    "fairway" : 0.25,
    "rough" : 0.15,
    "OB" : 0.1
}
SURFACE_ROLLING_RESISTANCE = {
    "water" : 1,
    "sand" : 0.8,
    "green" : 0.1,
    "fairway" : 0.2,
    "rough" : 0.3,
    "OB" : 0.5
}
SURFACE_SWING_AFFECT = {
    "rough" : {
        "wedge" : 1.00,
        "iron" : 0.75,
        "wood" : 0.50,
        "putter" : 0.3
    },
    "sand" : {
        "wedge" : 0.75,
        "iron" : 0.50,
        "wood" : 0.25,
        "putter" : 0.25
    },
    "green" : {
        "wedge" : 1,
        "iron" : 1,
        "wood" : 1,
        "putter" : 1
    },
    "fairway" : {
        "wedge" : 1,
        "iron" : 1,
        "wood" : 1,
        "putter" : 1
    }
}

GREEN_GRADIENT = [0, 0.05, 0.09, 0.12, 0.14]
