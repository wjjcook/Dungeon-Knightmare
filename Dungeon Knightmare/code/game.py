import pygame, sys, time
from pygame.locals import *
from entities import *
from utils import *
from settings import *
from tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Dungeon Knightmare')

        WINDOW_SIZE = (screenWidth * 3, screenHeight * 3)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.display = pygame.Surface((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'terrain': loadImages('terrain'),
            'decor': loadImages('torch'),
            'spikes': loadImages('spikes'),
            'red_enemy': loadImages('red_enemy'),
            'green_enemy': loadImages('green_enemy'),
            'blue_enemy': loadImages('blue_enemy'),
            'boss': loadImages('boss'),
            'player': loadImages('player'),
            'spawners': loadImages('spawners'),
            'attack': loadImage('attack.png'),
            'heart': loadImage('heart.png'),
            'you win': loadImage('you win.png'),
            'you lose': loadImage('you lose.png'),
            'boss heart': loadImage('boss heart.png'),
            'player/idle' : Animation(loadImages('player'), imgDur = 6),
            'player/run' : Animation(loadImages('player'), imgDur = 6),
            'player/jump' : Animation(loadImages('player'), imgDur = 6),
            'player/attack' : Animation(loadImages('player'), imgDur = 6),
            'red_enemy/idle': Animation(loadImages('red_enemy'), imgDur = 6),
            'green_enemy/idle': Animation(loadImages('green_enemy')),
            'blue_enemy/idle': Animation(loadImages('blue_enemy')),
            'red_enemy/run': Animation(loadImages('red_enemy')),
            'green_enemy/run': Animation(loadImages('green_enemy')),
            'blue_enemy/run': Animation(loadImages('blue_enemy')),
            'boss/idle': Animation(loadImages('boss')),
            'boss/run': Animation(loadImages('boss')),
        }
        self.player = Player(self, (64, 64), (16, 32))

        self.tilemap = Tilemap(self, TILE_SIZE)
        self.loadLevel('map.json')


    def loadLevel(self, mapID):
        self.tilemap.load(mapID)

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(RedEnemy(self, spawner['pos'], (16, 16)))
            elif spawner['variant'] == 2:
                self.enemies.append(GreenEnemy(self, spawner['pos'], (16, 16)))
            elif spawner['variant'] == 3:
                self.enemies.append(BlueEnemy(self, spawner['pos'], (16, 16)))
            elif spawner['variant'] == 4:
                self.enemies.append(BossEnemy(self, spawner['pos'], (48, 48)))

        self.scroll = [0, 0]
        self.lives = 3
        self.bossLives = 5
        self.hurtCooldown = 0
        self.bossHurtCooldown = 0
        self.attackCooldown = 0
        self.restartTimer = 0
        self.youWin = False


    def run(self):
        while True:
            
            self.display.fill((50, 61, 109))
            
            # self.display.blit(self.assets['backgound'], (0, 0)) can replace the display fill with a background

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = renderScroll)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset = renderScroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = renderScroll)

            for i in range(self.lives):
                self.display.blit(self.assets['heart'], ((i * 17), screenHeight - 28))

            for i in range(self.bossLives):
                self.display.blit(self.assets['boss heart'], (screenWidth - (i * 17) - 20, screenHeight - 18))

            if self.youWin:
                self.lives == 3
                if self.restartTimer == 0:
                    self.restartTimer = 180
                self.display.blit(self.assets['you win'], (screenWidth // 2 - 30, screenHeight // 2 - 30))
                self.restartTimer = max(1, self.restartTimer - 1)
            if self.restartTimer == 1:
                self.loadLevel('map.json')

            for enemy in self.enemies:
                if self.player.rect().colliderect(enemy.rect()) and self.hurtCooldown == 0:
                    self.hurtCooldown = 90
                    self.lives -= 1
            self.hurtCooldown = max(0, self.hurtCooldown - 1)
            if self.lives < 1:
                if self.restartTimer == 0:
                    self.restartTimer = 180
                self.display.blit(self.assets['you lose'], (screenWidth // 2 - 30, screenHeight // 2 - 30))
                self.restartTimer = max(1, self.restartTimer - 1)
            if self.restartTimer == 1:
                self.loadLevel('map.json')

            if self.player.attacking and self.attackCooldown == 30:
                inFrontRect = self.player.rect()
                if self.player.flip:
                    inFrontRect[0] -= 16
                else:
                    inFrontRect[0] += 16
                for enemy in self.enemies:
                    if inFrontRect.colliderect(enemy.rect()):
                        if enemy.boss == True and self.bossHurtCooldown == 0:
                            self.bossHurtCooldown = 90
                            enemy.lives -= 1
                            if enemy.lives < 1:
                                self.enemies.remove(enemy)
                                self.youWin = True
                            self.bossLives = enemy.lives                        
                        elif not enemy.boss:
                            self.enemies.remove(enemy)
                self.display.blit(pygame.transform.flip(self.assets['attack'] , self.player.flip, False), (inFrontRect[0] - renderScroll[0], inFrontRect[1] + 8 - renderScroll[1]))
                self.player.attacking = max(0, self.player.attacking - 1)
            if self.player.attacking == 0:
                self.attackCooldown = max(0, self.attackCooldown - 1)
            self.bossHurtCooldown = max(0, self.bossHurtCooldown - 1)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.movement[0] = 1.5
                    if event.key == K_RIGHT:
                        self.movement[1] = 1.5
                    if event.key == K_UP:
                        self.player.jump()
                    if event.key == K_x:
                        if self.attackCooldown == 0:
                            self.player.attacking = 18
                            self.attackCooldown = 30
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.movement[0] = 0
                        self.player.velocity[0] = 0
                    if event.key == K_RIGHT:
                        self.movement[1] = 0
                        self.player.velocity[0] = 0
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()