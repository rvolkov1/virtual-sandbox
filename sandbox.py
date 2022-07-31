import pygame
import sys
import time
from datetime import datetime
import mediapipe as mp
import random
import math

mp_hands  = mp.solutions.hands

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
PARTICLE_SIZE = 5

GRID_HEIGHT = int(CANVAS_HEIGHT/PARTICLE_SIZE)
GRID_WIDTH = int(CANVAS_WIDTH/PARTICLE_SIZE)

particle_map = [[None for i in range(GRID_HEIGHT)] for j in range(GRID_WIDTH)]
mousedown = False

def get_line_points(naught, final):
    # 20, 20, 20, 10
    distance = math.dist(naught, final)

    if distance == 0: return []

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

def resolve_forces(point, block_type, fx, fy):
    if (fx == fy == 0): return

    x = point[0]
    y = point[1]

    while (particle_map[x][y] != None):
        if (x + fx <= 0 or x + fx >= GRID_WIDTH):
            if (y > 1):
                y -= 1
            else:
                y += 1
        elif (y + fy >= GRID_HEIGHT or y + fy <= 0):
            if (x > 1):
                x -= 1
            else:
                x += 1
        else:
            x += fx
            y += fy
            
    particle_map[x][y] = SandBlock(x, y) if block_type == "sand" else WaterBlock(x, y)

class Bucket():
    def __init__(self):
        self.center = (20, 20)
        self.angle = 0
        self.side_length = 10
        self.vertices = ((-1, -1),)

    def get_vertices(self):
        a = math.sin(self.angle) * (self.side_length / 2) 
        b = math.cos(self.angle) * (self.side_length / 2)
        
        bot_left = (round(self.center[0] - b), round(self.center[1] + a))
        bot_right = (round(self.center[0] + b), round(self.center[1] - a))

        top_left = (bot_left[0] - self.side_length * math.sin(self.angle), bot_left[1] - self.side_length * math.cos(self.angle))
        top_right = (bot_right[0] - self.side_length * math.sin(self.angle), bot_right[1] - self.side_length * math.cos(self.angle))

        return top_left, bot_left, bot_right, top_right

    def update(self, results):
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

            if (self.angle == 0 or abs((new_angle - self.angle) / self.angle) > 0.1 ):
                self.angle = new_angle

            buffer = 1/10

            new_x = GRID_WIDTH - round(((pinky_x + index_x) - buffer) * GRID_WIDTH)
            new_y = round(((pinky_y + index_y)- buffer) * GRID_HEIGHT)

            if new_x <= 0: 
                new_x = 1
            elif new_x > GRID_WIDTH:
                new_x = GRID_WIDTH - 1

            if new_y <= 0: 
                new_y = 1
            elif new_y > GRID_HEIGHT:
                new_y = GRID_HEIGHT - 1

            old_point = self.center

            if(abs((new_x - self.center[0]) / self.center[0]) > 0.05):
                self.center = (new_x, self.center[1])

            if(abs((new_y - self.center[1]) / self.center[1]) > 0.05):
                self.center = (self.center[0], new_y)


            vertex_1, vertex_2, vertex_3, vertex_4 = self.get_vertices()

            line = []
            line += get_line_points(vertex_1, vertex_2) + get_line_points(vertex_2, vertex_3) + get_line_points(vertex_3, vertex_4)

            self.vertices = line

            for index, point in enumerate(self.vertices):
                if (point[0] < 0 or point[0] > GRID_WIDTH-1 or point[1] < 0 or point[1] > GRID_HEIGHT -1): continue
                block_type = type(particle_map[point[0]][point[1]]).__name__

                if (block_type != "StoneBlock"):
                    fx = 0
                    fy = 0

                    dx = new_x - old_point[0]
                    dy = new_y - old_point[1]

                    sign = lambda x: x and (1, -1)[x<0]

                    resolve_forces(point, block_type, sign(dx), 0)

                new_block = StoneBlock(point[0], point[1])
                particle_map[point[0]][point[1]] = new_block

class StoneBlock():
    def __init__(self, posX, posY): 
        self.x = posX
        self.y = posY
        self.color = (167,173,186)

    def update(self):
        pass

class SandBlock():
    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.color = (194, 178, 128)
       
    def update(self):
        if ((self.y + 1) * PARTICLE_SIZE >= CANVAS_HEIGHT):
            return
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and particle_map[self.x][self.y + 1] == None):
            particle_map[self.x][self.y] = None
            self.y += 1
            particle_map[self.x][self.y] = self
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x < CANVAS_WIDTH/PARTICLE_SIZE-1 and particle_map[self.x + 1][self.y + 1] == None and particle_map[self.x + 1][self.y] == None):
            particle_map[self.x][self.y] = None
            self.y += 1
            self.x += 1
            particle_map[self.x][self.y] = self
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x > 0 and particle_map[self.x - 1][self.y + 1] == None and particle_map[self.x - 1][self.y] == None):
            particle_map[self.x][self.y] = None
            self.y += 1
            self.x -= 1
            particle_map[self.x][self.y] = self

        return (self.x, self.y)


class WaterBlock():
    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.dx = 0
        self.color = (156, 211, 219)

    def update(self):
        if (self.y < GRID_HEIGHT-1 and particle_map[self.x][self.y + 1] == None):
            particle_map[self.x][self.y] = None
            self.y += 1
            particle_map[self.x][self.y] = self
            return (self.x, self.y)
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1):

            # and self.x > 0 and particle_map[self.x - 1][self.y + 1] == None and particle_map[self.x - 1][self.y] == None   
            # and self.x < CANVAS_WIDTH/PARTICLE_SIZE-1 and particle_map[self.x + 1][self.y + 1] == None and particle_map[self.x + 1][self.y] == None 

            i = 1
            while (i <= 8):
                if (self.x + i < GRID_WIDTH and self.y + 1 < GRID_HEIGHT and particle_map[self.x + i][self.y + 1] == None):
                    particle_map[self.x][self.y] = None
                    self.y += 1
                    self.x += i
                    particle_map[self.x][self.y] = self
                    return (self.x, self.y)
                elif (self.x - i > 0 and self.y + 1 < GRID_HEIGHT and particle_map[self.x - i][self.y + 1] == None):
                    particle_map[self.x][self.y] = None
                    self.y += 1
                    self.x -= i
                    particle_map[self.x][self.y] = self
                    return (self.x, self.y)

                i += 1

        
        if (self.dx == 0):
            self.dx = -1
            # self.dx = 1 if random.random() > 0.5 else -1
        elif (self.x + self.dx < GRID_WIDTH-1 and self.x + self.dx > 0 and particle_map[self.x + self.dx][self.y] == None):
            particle_map[self.x][self.y] = None
            self.x += self.dx
            particle_map[self.x][self.y] = self
        else: self.dx *= -1

        return (self.x, self.y)

def game_loop(q):
    pygame.init()
    WINDOW = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("sandbox")
    clock = pygame.time.Clock()

    bucket = Bucket()


    def render():
        surface = pygame.Surface((CANVAS_WIDTH/PARTICLE_SIZE, CANVAS_HEIGHT/PARTICLE_SIZE))

        # record tiles that have been updated
        updated_tiles = {}

        for row, array in reversed(list(enumerate(particle_map))):
            for column, tile in reversed(list(enumerate(array))):
                if tile != None and (row, column) not in updated_tiles:
                    surface.set_at((row, column), tile.color)
                    updated_tile = tile.update()
                    updated_tiles[updated_tile] = True

        scaled_surface = pygame.transform.scale(surface, (CANVAS_WIDTH, CANVAS_HEIGHT))
        WINDOW.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def update_fps():
        fps = str(int(clock.get_fps()))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
            if pygame.mouse.get_pressed()[0]:
                mousedown = True
            else:
                mousedown = False

        if mousedown:
            x, y = pygame.mouse.get_pos()
            
            new_x = int(x / PARTICLE_SIZE)
            new_y = int(y / PARTICLE_SIZE)

            if (particle_map[new_x][new_y] == None):
                new_block = WaterBlock(new_x, new_y)
                particle_map[new_x][new_y] = new_block

        try:
            results = q.get()
            while not q.empty():
                results = q.get()
        except IndexError:
            print("index error")
            pass

        bucket.update(results)
        render()
        update_fps()

        # remove all past hand blocks

        for point in bucket.vertices:
            if (point[0] < 0 or point[0] > GRID_WIDTH-1 or point[1] < 0 or point[1] > GRID_HEIGHT -1): continue

            if type(particle_map[point[0]][point[1]]).__name__ == "StoneBlock":
                particle_map[point[0]][point[1]] = None                

    root.mainloop()


# def draw_hands(results):
#     for hand_no, hand_landmarks in enumerate(results):
#         wrist_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * CANVAS_WIDTH
#         wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * CANVAS_HEIGHT

#         thumb_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * CANVAS_WIDTH
#         thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * CANVAS_HEIGHT

#         thumb_to_index_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x) / 2 * CANVAS_WIDTH
#         thumb_to_index_y = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

#         index_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * CANVAS_WIDTH
#         index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * CANVAS_HEIGHT

#         index_to_middle_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
#         index_to_middle_y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

#         middle_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * CANVAS_WIDTH
#         middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * CANVAS_HEIGHT

#         middle_to_ring_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
#         middle_to_ring_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

#         ring_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * CANVAS_WIDTH
#         ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * CANVAS_HEIGHT

#         ring_to_pinky_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x) / 2 * CANVAS_WIDTH
#         ring_to_pinky_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y) / 2 * CANVAS_HEIGHT

#         pinky_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * CANVAS_WIDTH
#         pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * CANVAS_HEIGHT

#         pygame.draw.polygon(screen, (255, 0, 0), ((wrist_x, wrist_y), (thumb_x, thumb_y), (thumb_to_index_x, thumb_to_index_y), (index_x, index_y), (index_to_middle_x, index_to_middle_y), (middle_x, middle_y), (middle_to_ring_x, middle_to_ring_y), (ring_x, ring_y), (ring_to_pinky_x, ring_to_pinky_y), (pinky_x, pinky_y)))
