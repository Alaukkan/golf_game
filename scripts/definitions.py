import math

RESOLUTION = [144, 144]
PIXEL_SIZE = 2
FRAME_RATE = 30

BASE_IMG_PATH = "graphics/sprites/"


MAX_WINDSPEED = 12
GRAVITY = 9.81
BALL_ROLLING_RESISTANCE = 1
BALL_WIND_RESISTANCE = 0.9
AIR_DENSITY = 1.3
VELOCITY_THRESHOLD = 0.05
SURFACE_HARDNESS = {
    "water" : 0,
    "sand" : 0.1,
    "green" : 0.5,
    "fairway" : 0.35,
    "rough" : 0.2
}
SURFACE_ROLLING_RESISTANCE = {
    "water" : 0,
    "sand" : 0.1,
    "green" : 0.95,
    "fairway" : 0.9,
    "rough" : 0.7
}
SURFACE_GRADIENT = [0, 0.035, 0.070, 0.105]
SURFACE_GRADIENT_ANGLE = {
    "N" : 0,
    "NE" : -math.pi / 4,
    "E" : -math.pi / 2,
    "SE" : -3 * math.pi / 4,
    "S" : math.pi,
    "SW" : 3 * math.pi / 4,
    "W" : math.pi / 2,
    "NW" : math.pi / 4,
}