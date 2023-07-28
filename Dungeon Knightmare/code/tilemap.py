import pygame, json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'terrain', 'spikes'}

class Tilemap:
    def __init__(self, game, tileSize):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offgridTiles = []

    def extract(self, idPairs, keep = False):
        matches = []
        for tile in self.offgridTiles.copy():
            if (tile['type'], tile['variant']) in idPairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgridTiles.remove(tile)
        temp = []
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in idPairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tileSize
                matches[-1]['pos'][1] *= self.tileSize
                if not keep:
                    temp.append(loc)
        for loc in temp:
            del self.tilemap[loc]
        temp.clear()
        return matches

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tileSize': self.tileSize, 'offgrid': self.offgridTiles}, f)

    def load(self, path):
        f = open(path, 'r')
        mapData = json.load(f)

        self.tilemap = mapData['tilemap']
        self.tileSize = mapData['tileSize']
        self.offgridTiles = mapData['offgrid']

    def solidCheck(self, pos):
        tileLoc = str(int(pos[0] // self.tileSize)) + ';' + str(int(pos[1] // self.tileSize))
        if tileLoc in self.tilemap:
            if self.tilemap[tileLoc]['type'] in PHYSICS_TILES:
                return self.tilemap[tileLoc]

    def tilesAround(self, pos, size): # FIX BIG BOSS
        tiles = []
        tileLoc = (int((pos[0] + size[0])// self.tileSize), int((pos[1] + size[1])// self.tileSize))
        for offset in NEIGHBOR_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ';' + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])
        return tiles
    
    def physicsRectsAround(self, pos, size):
        rects = []
        for tile in self.tilesAround(pos, size):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects
    
    def spikesAround(self, pos, size):
        rects = []
        spikes = []
        for tile in self.tilesAround(pos, size):
            if tile['type'] in PHYSICS_TILES:
                if tile['type'] == 'spikes':
                    spikes.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))
                else:
                    rects.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects, spikes

    def render(self, surface, offset = (0, 0)):
        for tile in self.offgridTiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for x in range(offset[0] // self.tileSize, (offset[0] + surface.get_width()) // self.tileSize + 1):
            for y in range(offset[1] // self.tileSize, (offset[1] + surface.get_height()) // self.tileSize + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))

            
