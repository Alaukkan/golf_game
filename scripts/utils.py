import pygame
import os
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
