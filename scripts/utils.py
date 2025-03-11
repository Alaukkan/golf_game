import json
import pygame
import os
from datetime import datetime
import scripts.definitions as defs

def load_image(path):
    img = pygame.image.load(defs.BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(defs.BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_hole(course, hole):
    with open("resources/courses.json") as f:
        courses = json.load(f)
    return courses[course][hole - 1]

def save_scores(game):
    gametime = datetime.now().strftime("%d.%m.%Y, %H.%M")
    with open("resources/highscores.json", "r") as f:
        highscores = json.load(f)

        for player in game.players:
            highscores.append({"time" : gametime, "scorecard" : player.scorecard, "score" : sum(game.course_pars) - sum(player.scorecard)})

    with open("resources/highscores.json", "w") as f:
        formatted_json = json.dumps(highscores, indent=4)
        formatted_json = formatted_json.replace("\n            ", "").replace("\n        ]", "]")

        f.write(formatted_json)


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

