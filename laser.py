import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, type, pos, screen_height):
        super().__init__()
        if type == "player":
            self.image = pygame.image.load("graphics/player/laser.png").convert_alpha()
        else:
            self.image = pygame.image.load("graphics/enemies/laser.png").convert_alpha()

        self.rect = self.image.get_rect(center = pos)
        self.speed = 7
        self.height_y_constraint = screen_height
    
    def destroy(self, type):
        if type == "player":
            if self.rect.y <= -10 or self.rect.y >= self.height_y_constraint:
                self.kill()
        else:
            if self.rect.y >= 800 or self.rect.y <= -10:
                self.kill() 

    def update(self, type):
        if type == "player":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        
        self.destroy(type)