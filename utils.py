"""Helpers for loading image assets and playing sprite animations."""

import os

import pygame

# All image paths passed to the loading helpers are relative to this folder.
BASE_IMG_PATH = 'data/images/'


def load_image(path):
    # Load one image, convert it for efficient blitting, and treat black as
    # transparent for the game's sprite assets.
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    # Load every image in a folder in sorted order so animation frames remain
    # consistent between runs.
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        # img_dur is the number of game frames each animation image is shown.
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        # Give an entity independent playback state while reusing the images.
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        # Looping animations wrap around; one-shot animations stop on their
        # final image and mark themselves complete.
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        # Convert the animation frame counter to the index of its current image.
        return self.images[int(self.frame / self.img_duration)]