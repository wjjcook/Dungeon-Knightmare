import pygame, sys, random
from pygame.locals import *
from utils import *
from settings import *
from tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')

        WINDOW_SIZE = (screenWidth, screenHeight)
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]

        self.assets = {
            'terrain': loadImages('terrain'),
            'decor': loadImages('torch'),
            'spikes': loadImages('spikes'),
            'spawners': loadImages('spawners')
        }

        self.tilemap = Tilemap(self, TILE_SIZE)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tileList = list(self.assets)
        self.tileGroup = 0
        self.tileVariant = 0

        self.clicking = False
        self.rightClicking = False
        self.shift = False
        self.onGrid = True

    def run(self):
        while True:
            
            self.display.fill(('black'))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = renderScroll)

            currentTileImg = self.assets[self.tileList[self.tileGroup]][self.tileVariant].copy()
            currentTileImg.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tilePos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tileSize), int((mpos[1] + self.scroll[1]) // self.tilemap.tileSize))

            if self.onGrid:
                self.display.blit(currentTileImg, (tilePos[0] * self.tilemap.tileSize - self.scroll[0], tilePos[1] * self.tilemap.tileSize - self.scroll[1]))
            else:
                self.display.blit(currentTileImg, mpos)

            if self.clicking and self.onGrid:
                self.tilemap.tilemap[str(tilePos[0]) + ';' + str(tilePos[1])] = {'type': self.tileList[self.tileGroup], 'variant': self.tileVariant, 'pos': tilePos}
            if self.rightClicking:
                tileLoc = str(tilePos[0]) + ';' + str(tilePos[1])
                if tileLoc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tileLoc]
                for tile in self.tilemap.offgridTiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgridTiles.remove(tile)
            self.display.blit(currentTileImg, (5, 5))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.onGrid:
                            self.tilemap.offgridTiles.append({'type': self.tileList[self.tileGroup], 'variant': self.tileVariant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.rightClicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tileVariant = (self.tileVariant - 1) % len(self.assets[self.tileList[self.tileGroup]])
                        if event.button == 5:
                            self.tileVariant = (self.tileVariant + 1) % len(self.assets[self.tileList[self.tileGroup]])
                    else:
                        if event.button == 4:
                            self.tileGroup = (self.tileGroup - 1) % len(self.tileList)
                            self.tileVariant = 0
                        if event.button == 5:
                            self.tileGroup = (self.tileGroup + 1) % len(self.tileList)
                            self.tileVariant = 0
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.rightClicking = False

                if event.type == KEYDOWN:
                    if event.key == K_a:
                        self.movement[0] = True
                    if event.key == K_d:
                        self.movement[1] = True
                    if event.key == K_w:
                        self.movement[2] = True
                    if event.key == K_s:
                        self.movement[3] = True
                    if event.key == K_g:
                        self.onGrid = not self.onGrid
                    if event.key == K_o:
                        self.tilemap.save('map.json')
                    if event.key == K_LSHIFT:
                        self.shift = True
                if event.type == KEYUP:
                    if event.key == K_a:
                        self.movement[0] = False
                    if event.key == K_d:
                        self.movement[1] = False
                    if event.key == K_w:
                        self.movement[2] = False
                    if event.key == K_s:
                        self.movement[3] = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Editor().run()