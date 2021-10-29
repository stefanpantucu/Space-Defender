import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, screen_width):
        super().__init__()

        file_path = "graphics/enemies/enemy_" + color + ".png"
        if color == "red":
            self.score = 1
        else:
            self.score = 2
        
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect(topleft = (randint(0, screen_width - 50), -50))

        self.speed = 2
    
    def destroy(self):
        if self.rect.top > 750:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()