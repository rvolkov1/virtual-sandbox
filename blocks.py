CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
PARTICLE_SIZE = 5

GRID_WIDTH = int(CANVAS_WIDTH/PARTICLE_SIZE)
GRID_HEIGHT = int(CANVAS_HEIGHT/PARTICLE_SIZE)

class StoneBlock():
    def __init__(self, posX, posY): 
        self.x = posX
        self.y = posY
        self.color = (167,173,186)
        self.density = 10

    def get_move(self, tilemap):
        return None

class BucketBlock():
    def __init__(self, posX, posY): 
        self.x = posX
        self.y = posY
        self.color = (1,115,92)
        self.density = 10

    def get_move(self, tilemap):
        return None

class SandBlock():
    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.color = (194, 178, 128)
        self.density = 1
       
    # def update_tilemap(self, dx, dy):
    #     if (tilemap[self.x + dx][self.y + dy] == None):
    #         tilemap[self.x][self.y] = None
    #         self.x += dx
    #         self.y += dy
    #         tilemap[self.x][self.y] = self
    #         return (self.x, self.y)
    #     else:
    #         other_block = tilemap[self.x + dx][self.y + dy]
    #         self.x += dx
    #         self.y += dy
    #         tilemap[self.x - dx][self.y - dy] = other_block
    #         other_block.x = self.x - dx
    #         other_block.y = self.y - dy
    #         tilemap[self.x][self.y] = self
    #         return (self.x, self.y)

    def update_position(self, point):
        self.x = point[0]
        self.y = point[1]

    def get_move(self, tilemap):
        if ((self.y + 1) * PARTICLE_SIZE >= CANVAS_HEIGHT):
            return (self.x, self.y)
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and (tilemap[self.x][self.y + 1] == None or tilemap[self.x][self.y + 1].density < self.density)):
            return (self.x, self.y + 1)
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x < CANVAS_WIDTH/PARTICLE_SIZE-1 and tilemap[self.x + 1][self.y] == None and (tilemap[self.x + 1][self.y + 1] == None or tilemap[self.x + 1][self.y + 1].density < self.density)):
            return (self.x + 1, self.y + 1)
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x > 0 and tilemap[self.x - 1][self.y] == None and (tilemap[self.x - 1][self.y + 1] == None or tilemap[self.x - 1][self.y + 1].density < self.density)):
            return (self.x - 1, self.y + 1)
        
        return (self.x, self.y)


class WaterBlock():
    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.dx = 0
        self.density = 0.2
        self.friction = 8
        self.color = (156, 211, 219)

    # def update_tilemap(self, dx, dy):
    #     if (tilemap[self.x + dx][self.y + dy] == None):
    #         tilemap[self.x][self.y] = None
    #         self.x += dx
    #         self.y += dy
    #         tilemap[self.x][self.y] = self
    #         return (self.x, self.y)
    #     else:
    #         other_block = tilemap[self.x + dx][self.y + dy]
    #         self.x += dx
    #         self.y += dy
    #         tilemap[self.x - dx][self.y - dy] = other_block
    #         other_block.x = self.x - dx
    #         other_block.y = self.y - dy
    #         tilemap[self.x][self.y] = self
    #         return (self.x, self.y)

    def update_position(self, point):
        self.x = point[0]
        self.y = point[1]

    def get_move(self, tilemap):
        if (self.y < GRID_HEIGHT-1 and tilemap[self.x][self.y + 1] == None):
            return (self.x, self.y + 1)
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1):
            for i in range(1, self.friction + 1):
                if (self.x + i < GRID_WIDTH - 1 and self.y < GRID_HEIGHT-1 and tilemap[self.x + i][self.y] != None):
                    break
                if (self.x + i < GRID_WIDTH-1 and self.y + 1 < GRID_HEIGHT-1 and tilemap[self.x + i][self.y + 1] == None):
                    return (self.x + i, self.y + 1)
            
            for i in range(1, self.friction+1):
                if (self.x - i > 0 and self.y < GRID_HEIGHT-1 and tilemap[self.x - i][self.y] != None):
                    break
                elif (self.x - i > 0 and self.y + 1 < GRID_HEIGHT-1 and tilemap[self.x - i][self.y + 1] == None):
                    return (self.x - i, self.y + 1)
        
        if (self.dx == 0):
            self.dx = -1
            return (self.x, self.y)
            # self.dx = 1 if random.random() > 0.5 else -1
        elif (self.x + self.dx < GRID_WIDTH-1 and self.x + self.dx > 0 and tilemap[self.x + self.dx][self.y] == None):
            return (self.x + self.dx, self.y)
        else: 
            self.dx *= -1
            return (self.x, self.y)
