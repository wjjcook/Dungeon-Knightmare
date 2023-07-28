import pygame, os
from settings import *

def loadImage(path):
    img = pygame.image.load('graphics/' + path).convert()
    img.set_colorkey((255, 255, 255))
    return img

def loadImages(path):
    images = []
    for img_name in sorted(os.listdir('graphics/' + path)):
        images.append(loadImage(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, imgDur = 5, loop = True):
        self.images = images
        self.loop = loop
        self.imgDur = imgDur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.imgDur, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imgDur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.imgDur * len(self.images) - 1)
            if self.frame >= self.imgDur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.imgDur)]