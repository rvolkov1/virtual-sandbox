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

particle_map = [[None for i in range(int(CANVAS_HEIGHT/PARTICLE_SIZE))] for j in range(int(CANVAS_WIDTH/PARTICLE_SIZE))]
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

class Bucket():
    def __init__(self):
        self.center = (20, 20)
        self.angle = 0
        self.side_length = 10
        self.vertices = ((20, 20),)

    def get_vertices(self):
        a = math.sin(self.angle) * (self.side_length / 2) 
        b = math.cos(self.angle) * (self.side_length / 2)
        
        bot_left = (round(self.center[0] - b), round(self.center[1] + a))
        bot_right = (round(self.center[0] + b), round(self.center[1] - a))

        top_left = (bot_left[0] - self.side_length * math.sin(self.angle), bot_left[1] - self.side_length * math.cos(self.angle))
        top_right = (bot_right[0] - self.side_length * math.sin(self.angle), bot_right[1] - self.side_length * math.cos(self.angle))

        return top_left, bot_left, bot_right, top_right

    def update(self, results):
        if results:
            index_x = results[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
            index_y = results[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

            pinky_x = results[0].landmark[mp_hands.HandLandmark.PINKY_MCP].x
            pinky_y = results[0].landmark[mp_hands.HandLandmark.PINKY_MCP].y

            dx = index_x - pinky_x
            dy = index_y - pinky_y

            new_angle = round(math.atan2(dy, dx), 1)

            if (self.angle == 0 or abs((new_angle - self.angle) / self.angle) > 0.1 ):
                self.angle = new_angle

            buffer = 1/10

            new_x = len(particle_map) - round(((pinky_x + index_x) - buffer) * len(particle_map))
            new_y = round(((pinky_y + index_y)- buffer) * len(particle_map[0]))

            if new_x <= 0: 
                new_x = 1
            elif new_x > len(particle_map):
                new_x = len(particle_map) - 1

            if new_y <= 0: 
                new_y = 1
            elif new_y > len(particle_map[0]):
                new_y = len(particle_map[0]) - 1


            if(abs((new_x - self.center[0]) / self.center[0]) > 0.05):
                self.center = (new_x, self.center[1])

            if(abs((new_y - self.center[1]) / self.center[1]) > 0.05):
                self.center = (self.center[0], new_y)


            vertex_1, vertex_2, vertex_3, vertex_4 = self.get_vertices()

            line = []
            line += get_line_points(vertex_1, vertex_2) + get_line_points(vertex_2, vertex_3) + get_line_points(vertex_3, vertex_4)

            self.vertices = line


        for point in self.vertices:
            if (point[0] < 0 or point[0] > len(particle_map)-1 or point[1] < 0 or point[1] > len(particle_map[0]) -1): continue

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
        elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and particle_map[self.x][self.y + 1] == None ):
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


def game_loop(q):
    pygame.init()
    WINDOW = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("sandbox")
    clock = pygame.time.Clock()

    bucket = Bucket()


    def render():
        surface = pygame.Surface((CANVAS_WIDTH/PARTICLE_SIZE, CANVAS_HEIGHT/PARTICLE_SIZE))

        for row, array in reversed(list(enumerate(particle_map))):
            for column, tile in reversed(list(enumerate(array))):
                if tile != None:
                    surface.set_at((row, column), tile.color)
                    tile.update()

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
                new_block = SandBlock(new_x, new_y)
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
            if (point[0] < 0 or point[0] > len(particle_map)-1 or point[1] < 0 or point[1] > len(particle_map[0]) -1): continue

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
