import pygame, random

class PhysicsEntity:
    def __init__(self, game, eType, pos, size):
        self.game = game
        self.type = eType
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.extraSize = [0, 0]
        self.boss = False

        self.action = ''
        self.animOffset = (0, 0)
        self.flip = False
        self.setAction('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def setAction(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement = (0,0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frameMovement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        if self.boss == True:
            self.pos[0] += frameMovement[0]
            entityRect = self.rect()
            for rect in tilemap.physicsRectsAround(self.pos, [0, 0]):
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x

            for rect in tilemap.physicsRectsAround(self.pos,  [32, 0]):
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x

            for rect in tilemap.physicsRectsAround(self.pos, [0, 32]):
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x
            
            for rect in tilemap.physicsRectsAround(self.pos, [32, 32]):
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x

            self.pos[1] += frameMovement[1]
            entityRect = self.rect()
            for rect in tilemap.physicsRectsAround(self.pos,  [0, 0]):
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y

            for rect in tilemap.physicsRectsAround(self.pos,  [32, 0]):
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y

            for rect in tilemap.physicsRectsAround(self.pos,  [0, 32]):
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y

            for rect in tilemap.physicsRectsAround(self.pos,  [32, 32]):
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y
        elif self.type == 'player':
            self.pos[0] += frameMovement[0]
            entityRect = self.rect()
            rects, spikes = tilemap.spikesAround(self.pos, self.extraSize)
            for rect in rects:
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x
            for spike in spikes:
                if entityRect.colliderect(spike):
                    if self.game.hurtCooldown == 0:
                        self.game.hurtCooldown = 90
                        self.game.lives -= 1
                    if frameMovement[0] > 0:
                        entityRect.right = spike.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = spike.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x

            self.pos[1] += frameMovement[1]
            entityRect = self.rect()
            rects, spikes = tilemap.spikesAround(self.pos, self.extraSize)
            for rect in rects:
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y
            for spike in spikes:
                if entityRect.colliderect(spike):
                    if self.game.hurtCooldown == 0:
                        self.game.hurtCooldown = 90
                        self.game.lives -= 1
                    if frameMovement[1] > 0:
                        entityRect.bottom = spike.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = spike.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y
    
        else:
            self.pos[0] += frameMovement[0]
            entityRect = self.rect()
            for rect in tilemap.physicsRectsAround(self.pos, self.extraSize):
                if entityRect.colliderect(rect):
                    if frameMovement[0] > 0:
                        entityRect.right = rect.left
                        self.collisions['right'] = True
                    if frameMovement[0] < 0:
                        entityRect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entityRect.x

            self.pos[1] += frameMovement[1]
            entityRect = self.rect()
            for rect in tilemap.physicsRectsAround(self.pos, self.extraSize):
                if entityRect.colliderect(rect):
                    if frameMovement[1] > 0:
                        entityRect.bottom = rect.top
                        self.collisions['down'] = True
                    if frameMovement[1] < 0:
                        entityRect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entityRect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.2)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
    

    def render(self, surface, offset = (0, 0)):
        # surface.blit(pygame.transform.flip(self.game.assets['player'], self.flip, False), (self.pos[0] - offset[0] + self.animOffset[0], self.pos[1] - offset[1] + self.animOffset[1]))
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.animOffset[0], self.pos[1] - offset[1] + self.animOffset[1]))

    
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.airTime = 0
        self.jumps = 1
        self.extraSize = [0, 16]
        self.attacking = 0

    def update(self, tilemap, movement = (0, 0)):
        super().update(tilemap, movement = movement)

        self.airTime += 1
        if self.collisions['down']:
            self.airTime = 0
            self.jumps = 1

        if self.airTime > 4:
            self.setAction('jump')
        elif movement[0] != 0:
            self.setAction('run')
        else:
            self.setAction('idle')
    
    def jump(self):
        if self.jumps and self.airTime < 6:
            self.velocity[1] = -4
            self.jumps -= 1
            self.airTime = 5
    
    def attack(self):
        self.attacking = 18


class GreenEnemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'green_enemy', pos, size)
    
    def update(self, tilemap, movement = (0, 0)):

        if self.collisions['right'] or self.collisions['left']:
            self.flip = not self.flip
        if tilemap.solidCheck((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
            movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
        else:
            self.flip = not self.flip

        # if movement[0] != 0:
        #     self.setAction('run')
        # else:
        #     self.setAction('idle')

        super().update(tilemap, movement = movement)


class BlueEnemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'blue_enemy', pos, size)
        # self.setAction('idle')
    
    def update(self, tilemap, movement = (0, 0)):

        super().update(tilemap, movement = movement)


class RedEnemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'red_enemy', pos, size)
    
    def update(self, tilemap, movement = (0, 0)):
        if self.collisions['right'] or self.collisions['left']:
            self.flip = not self.flip
        if tilemap.solidCheck((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
            movement = (movement[0] - 1.5 if self.flip else 1.5, movement[1])
        else:
            self.flip = not self.flip

        # if movement[0] != 0:
        #     self.setAction('run')
        # else:
        #     self.setAction('idle')

        super().update(tilemap, movement = movement)


class BossEnemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'boss', pos, size)
        self.walking = 30
        self.extraSize = [32, 32]
        self.boss = True
        self.lives = 5
    
    def update(self, tilemap, movement = (0, 0)):
        if self.collisions['right'] or self.collisions['left']:
            self.flip = not self.flip
        movement = (movement[0] - 1 if self.flip else 1, movement[1])
    
        
        # if movement[0] != 0:
        #     self.setAction('run')
        # else:
        #     self.setAction('idle')

        super().update(tilemap, movement = movement)