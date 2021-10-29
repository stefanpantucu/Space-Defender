import pygame
from sys import exit
from random import randint, choice
from player import Player
from enemy import Enemy
from laser import Laser

class Game:
    def __init__(self):
        # Player
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10),
                                (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Enemies:
        self.enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()

        self.enemy_setup()

        # Score
        self.score = 0
        self.game_active = False

    def enemy_setup(self):
        enemy_sprite = Enemy(choice(["red", "blue", "red"]), SCREEN_WIDTH)
        self.enemies.add(enemy_sprite)

    def enemy_shoot(self):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                laser_sprite = Laser("enemy", enemy.rect.center, SCREEN_HEIGHT)
                self.enemy_lasers.add(laser_sprite)

    def collision_check(self):
        global curr_score
        curr_score = game.score
        # player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                enemies_hit = pygame.sprite.spritecollide(laser, self.enemies, True)

                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += enemy.score
                    laser.kill()

        # enemy laser
        if self.enemy_lasers:
            for laser in self.enemy_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.enemies.empty()
                    self.enemy_lasers.empty()

                    curr_score = self.score
                    self.score = 0
                    self.game_active = False

        # enemy collision
        if self.enemies:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    self.enemies.empty()
                    self.enemy_lasers.empty()
                    
                    curr_score = self.score
                    self.score = 0
                    self.game_active = False

    def display_score(self):
        score_surface = font.render(f'Score: {self.score}', False, "White")
        score_rect = score_surface.get_rect(topleft = (20, 20))

        screen.blit(score_surface, score_rect)

    def run(self):
        self.player.update()
        self.enemies.update()
        self.enemy_lasers.update("enemy")

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.enemy_lasers.draw(screen)
        
        self.collision_check()
        self.display_score()

if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH = 650
    SCREEN_HEIGHT = 750
    FPS = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    bg_surface = pygame.image.load("graphics/space.png")
    icon_surface = pygame.image.load("graphics/icon.png")

    pygame.display.set_caption("Space Defender")
    pygame.display.set_icon(icon_surface)

    font = pygame.font.Font("font/Pixeltype.ttf", 50)

    clock = pygame.time.Clock()
    enemy_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_timer, 3000)

    laser_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(laser_timer, 1500)

    game = Game()
    curr_score = int(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game.game_active:
                if event.type == enemy_timer:
                    game.enemy_setup()
                
                if event.type == laser_timer:
                    game.enemy_shoot()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game.game_active = True
                    game.player.sprite.rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10)

        

        if game.game_active:
            screen.blit(bg_surface, (0, 0))

            score = game.run()
        
        else:
            screen.blit(bg_surface, (0, 0))
            game_name = font.render("Space Defender", False, "White")
            gamne_name_rect = game_name.get_rect(center = (SCREEN_WIDTH // 2, 100))

            if curr_score == 0:
                message = font.render(f'PRESS SPACE TO START', None, "White")
            else:
                message = font.render(f'Your score: {curr_score}', None, "White")

            message_rect = message.get_rect(center = (SCREEN_WIDTH // 2, 600))
            
            screen.blit(game_name, gamne_name_rect)
            screen.blit(message, message_rect)

        pygame.display.update()
        clock.tick(FPS)

