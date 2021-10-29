import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint):
        super().__init__()

        self.player_stay = pygame.image.load("graphics/player/player_stay.png").convert_alpha()
        self.player_stay = pygame.transform.scale(self.player_stay, (55, 65))
        self.player_fly = pygame.image.load("graphics/player/player_fly.png").convert_alpha()
        self.player_fly = pygame.transform.scale(self.player_fly, (55, 65))
        
        self.image = self.player_stay
        self.rect = self.image.get_rect(midbottom = pos)


        self.speed = 4
        self.max_x_constraint = constraint[0]
        self.max_y_constraint = constraint[1]
        
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.lasers = pygame.sprite.Group()

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        
        if self.rect.top <= 0:
            self.rect.top = 0
        
        if self.rect.bottom >= self.max_y_constraint:
            self.rect.bottom = self.max_y_constraint

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.image = self.player_stay
            self.rect.x -= self.speed

        elif keys[pygame.K_d]:
            self.image = self.player_stay
            self.rect.x += self.speed

        elif keys[pygame.K_w]:
            self.image = self.player_fly
            self.rect.y -= self.speed

        elif keys[pygame.K_s]:
            self.image = self.player_stay
            self.rect.y += self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False

            self.laser_time = pygame.time.get_ticks()
    
    def recharge(self): # recharge the laser
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser("player", self.rect.center, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update("player")