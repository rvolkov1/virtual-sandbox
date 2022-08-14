import math
from blocks import BucketBlock, SandBlock, WaterBlock, StoneBlock

class TileMap():
    def __init__(self, screen_width, screen_height, particle_size):
        self.width = int(screen_width/particle_size)
        self.height = int(screen_height/particle_size)
        self.map = [[None for i in range(self.height)] for j in range(self.width)]
        self.moves = None

    def update(self, mouse_pos, block_to_be_drawn, old_bucket_vertices, new_bucket_vertices):
        # apply forces on blocks and move them
        # draw bucket
        # add new blocks
        # calculate possible changes for blocks
        # update blocks

        if (new_bucket_vertices):
            new_bucket_tiles = self.get_line_points(new_bucket_vertices[0], new_bucket_vertices[1]) + self.get_line_points(new_bucket_vertices[1], new_bucket_vertices[2]) + self.get_line_points(new_bucket_vertices[2], new_bucket_vertices[3])
        else:
            new_bucket_tiles = None
        
        if (old_bucket_vertices):
            old_bucket_tiles = self.get_line_points(old_bucket_vertices[0], old_bucket_vertices[1]) + self.get_line_points(old_bucket_vertices[1], old_bucket_vertices[2]) + self.get_line_points(old_bucket_vertices[2], old_bucket_vertices[3])

            # remove old bucket tiles from map
            for tile in old_bucket_tiles:
                if not self.point_in_bounds(tile): continue
                self.map[tile[0]][tile[1]] = None
        else:
            old_bucket_tiles = None

        moved_tiles = self.get_moved_tiles(old_bucket_tiles, new_bucket_tiles)

        if (old_bucket_vertices != None and new_bucket_vertices != None):
            fx, fy = self.get_point_change(old_bucket_vertices[0], new_bucket_vertices[0])
        else:
            fx, fy = 0, 0

        # apply forces to tiles moved by bucket
        if moved_tiles:
            for point in moved_tiles:
                self.resolve_forces(point, fx, fy)
        
        if (new_bucket_tiles):
            # add bucket blocks to tilemap
            for point in new_bucket_tiles:
                if (not self.point_in_bounds(point)): continue
                self.map[point[0]][point[1]] = BucketBlock(point[0], point[1])

        if (mouse_pos != None):
            line_points = [mouse_pos[1]] if mouse_pos[0] == None else self.get_line_points(mouse_pos[0], mouse_pos[1])

            for point in line_points:
                if self.map[point[0]][point[1]] == None:
                    if (block_to_be_drawn == 1):
                        self.map[point[0]][point[1]] = SandBlock(point[0], point[1])
                    elif (block_to_be_drawn == 2):
                        self.map[point[0]][point[1]] = WaterBlock(point[0], point[1])
                    elif (block_to_be_drawn == 3):
                        self.map[point[0]][point[1]] = StoneBlock(point[0], point[1])

        # clear array
        self.moves = []

        # calculate desired move for each tile
        for row, array in enumerate(self.map):
            for column, tile in enumerate(array):
                if tile != None: 
                    new_point = tile.get_move(self.map)
                    
                    # if immovable object
                    if new_point == None: continue
                    self.moves.append(((row, column), new_point),)

        # sort moves list by destination; shuffle results
        if self.moves:
            # random.shuffle(self.moves.sort(key = lambda x: x[1]))
            self.moves.sort(key = lambda x: x[1])

            curr_move = None

            for move in self.moves:
                # skip if position is filled
                if (move[1] == curr_move): continue

                old_point = move[0]
                new_point = move[1]

                old_tile = self.map[old_point[0]][old_point[1]]

                if self.map[new_point[0]][new_point[1]] == None:
                    old_tile.update_position((new_point[0], new_point[1]))
                    self.map[new_point[0]][new_point[1]] = old_tile
                    self.map[old_point[0]][old_point[1]] = None
                    curr_move = new_point
                elif self.map[new_point[0]][new_point[1]].density < old_tile.density:
                    # density physics
                    less_dense_block = self.map[new_point[0]][new_point[1]]
                    self.map[new_point[0]][new_point[1]] = old_tile
                    self.map[new_point[0]][new_point[1] - 1] = less_dense_block
                    
                    old_tile.update_position((new_point[0], new_point[1]))
                    less_dense_block.update_position((new_point[0], new_point[1] - 1))

    def point_in_bounds(self, point):
        return point[0] >= 0 and point[0] < self.width and point[1] >= 0 and point[1] < self.height

    @staticmethod
    def get_line_points(naught, final):
        # 20, 20, 20, 10
        distance = math.dist(naught, final)
        
        if distance == 0: return [final]

        dx = (final[0] - naught[0]) / distance
        dy = (final[1] - naught[1]) / distance

        points = []

        start_x, end_x = (naught[0], final[0])
        start_y, end_y = (naught[1], final[1])

        for i in range(math.ceil(distance)):
            points.append((math.floor(start_x), math.floor(start_y)))
            start_x += dx
            start_y += dy
        
        return points

    @staticmethod
    def get_point_change(naught, final):
        fx = final[0] - naught[0]
        fy = final[1] - naught[1]
        return fx, fy

    def get_moved_tiles(self, old_bucket_tiles, new_bucket_tiles):
        if new_bucket_tiles == None: return

        moved_tiles = []

        # bucket tiles can be between 27 and 28 tiles for some reason
        for i in range(28):
            if old_bucket_tiles == None:
                line = new_bucket_tiles
            else:
                line = self.get_line_points(old_bucket_tiles[i], new_bucket_tiles[i])

            for point in line:
                if (self.point_in_bounds(point) and self.map[point[0]][point[1]] != None): 
                    moved_tiles.append(point)
        
        return moved_tiles

    def add_new_block(self, mouse_pos, block_type):
        pass

    def resolve_forces(self, point, fx, fy):
        if (fx == fy == 0): return
        x = point[0]
        y = point[1]

        x += fx + 1 if fx > 0 else fx - 1
        y += fy + 1 if fy > 0 else fy - 1

        # while (particle_map[x][y] != None):
        #     if (x + fx <= 0 or x + fx >= GRID_WIDTH):
        #         if (y > 1):
        #             y -= 1
        #         else:
        #             y += 1
        #     elif (y + fy >= GRID_HEIGHT or y + fy <= 0):
        #         if (x > 1):
        #             x -= 1
        #         else:
        #             x += 1
        #     else:
        #         x += fx
        #         y += fy

        return(x,y)
                
        self.particle_map[x][y] = SandBlock(x, y)
