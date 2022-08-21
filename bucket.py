import math
import mediapipe as mp
from tilemap import TileMap

mp_hands  = mp.solutions.hands

class Bucket():
    def __init__(self):
        self.center = (20, 20)
        self.angle = 0
        self.side_length = 10
        self.vertices = None
        self.points = []

    @staticmethod
    def get_pos_change(old_pos, new_pos):
        return len(TileMap.get_line_points(old_pos, new_pos))

    def calculate_vertices(self):
        a = math.sin(self.angle) * (self.side_length / 2) 
        b = math.cos(self.angle) * (self.side_length / 2)
        
        bot_left = (round(self.center[0] - b), round(self.center[1] + a))
        bot_right = (round(self.center[0] + b), round(self.center[1] - a))

        top_left = (round(bot_left[0] - self.side_length * math.sin(self.angle)), round(bot_left[1] - self.side_length * math.cos(self.angle)))
        top_right = (round(bot_right[0] - self.side_length * math.sin(self.angle)), round(bot_right[1] - self.side_length * math.cos(self.angle)))

        return (top_left, bot_left, bot_right, top_right)

    def get_vertices(self, results, GRID_WIDTH, GRID_HEIGHT):
        if results[0]:
            handedness_index = results[1][0].classification[0].index

            index_x = results[0][0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
            index_y = results[0][0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

            pinky_x = results[0][0].landmark[mp_hands.HandLandmark.PINKY_MCP].x
            pinky_y = results[0][0].landmark[mp_hands.HandLandmark.PINKY_MCP].y

            if (handedness_index == 0):
                dx = index_x - pinky_x
                dy = index_y - pinky_y
            else: 
                dx = pinky_x - index_x
                dy = pinky_y - index_y

            new_angle = round(math.atan2(dy, dx), 1)

            buffer = 1/10

            new_x = GRID_WIDTH - round(((pinky_x + index_x) - buffer) * GRID_WIDTH)
            new_y = round(((pinky_y + index_y)- buffer) * GRID_HEIGHT)

            # don't change if hand is outside of bounds
            if (self.angle == 0 or abs((new_angle - self.angle) / self.angle) > 0.1 and new_x > 0 and new_x < GRID_WIDTH - 1 and new_y > 0 and new_y < GRID_HEIGHT - 1):
                self.angle = new_angle

            # patchhhh
            self.angle = 0

            if new_x <= 0: 
                new_x = 1
            elif new_x > GRID_WIDTH:
                new_x = GRID_WIDTH - 1

            if new_y <= 0: 
                new_y = 1
            elif new_y > GRID_HEIGHT:
                new_y = GRID_HEIGHT - 1

            if(abs((new_x - self.center[0]) / self.center[0]) > 0.05):
                self.center = (new_x, self.center[1])

            if(abs((new_y - self.center[1]) / self.center[1]) > 0.05):
                self.center = (self.center[0], new_y)
            
            old_vertices = self.vertices
            self.vertices = self.calculate_vertices()
            return old_vertices, self.vertices
        else:
            return self.vertices, None

        
        # else:
        #     old_point = self.center
        #     new_x = self.center[0]
        #     new_y = self.center[1]

        # vertex_1, vertex_2, vertex_3, vertex_4 = self.get_vertices()


        # line = []
        # line += get_line_points(vertex_1, vertex_2) + get_line_points(vertex_2, vertex_3) + get_line_points(vertex_3, vertex_4)

        # new_vertices = line[:29]


        # for index, endpoint in enumerate(new_vertices):
        #     if (self.vertices != None):
        #         startpoint = self.vertices[index]
        #         point_line = get_line_points(endpoint, startpoint)
        #     else:
        #         point_line = [endpoint]

        #     for i, point in enumerate(point_line):
        #         if (point[0] < 0 or point[0] > GRID_WIDTH-1 or point[1] < 0 or point[1] > GRID_HEIGHT -1): continue
        #         block_type = type(particle_map[point[0]][point[1]]).__name__

        #         if (block_type != "StoneBlock" and block_type != "BucketBlock" and block_type != "NoneType"):
        #             dx = new_x - old_point[0]
        #             dy = new_y - old_point[1]

        #             # print(dx, dy)

        #             sign = lambda x: x and (1, -1)[x<0]

        #             # if (i != 0): 
        #             #     particle_map[point[0]][point[1]] = None

        #             resolve_forces(point, block_type, dx, dy)

                
        #         if (i == 0):
        #             self.points.append(point)
        #             new_block = BucketBlock(point[0], point[1])
        #             particle_map[point[0]][point[1]] = new_block                        
        
        # self.vertices = new_vertices
