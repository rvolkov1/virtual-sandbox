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

particle_map = [[0 for i in range(int(CANVAS_HEIGHT/PARTICLE_SIZE))] for j in range(int(CANVAS_WIDTH/PARTICLE_SIZE))]
blocks=[]
mousedown = False


def game_loop(q):
    class StoneBlock():
        def __init__(self, posX, posY):
            self.x = posX
            self.y = posY

        def update(self):
            pass

    class SandBlock():
        def __init__(self, posX, posY):
            self.x = posX
            self.y = posY
        
        def update(self):
            if ((self.y + 1) * PARTICLE_SIZE >= CANVAS_HEIGHT):
                return
            elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and particle_map[self.x][self.y + 1] <= 0 ):
                particle_map[self.x][self.y] = -1
                self.y += 1
                particle_map[self.x][self.y] = 1
            elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x < CANVAS_WIDTH/PARTICLE_SIZE-1 and particle_map[self.x + 1][self.y + 1] <= 0 ):
                particle_map[self.x][self.y] = -1
                self.y += 1
                self.x += 1
                particle_map[self.x][self.y] = 1
            elif (self.y < CANVAS_HEIGHT/PARTICLE_SIZE-1 and self.x > 0 and particle_map[self.x - 1][self.y + 1] <= 0 ):
                particle_map[self.x][self.y] = -1
                self.y += 1
                self.x -= 1
                particle_map[self.x][self.y] = 1

    pygame.init()
    WINDOW = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("sandbox")
    clock = pygame.time.Clock()


    def render():
        surface = pygame.Surface((CANVAS_WIDTH/PARTICLE_SIZE, CANVAS_HEIGHT/PARTICLE_SIZE))

        for block in blocks:
            surface.set_at((block.x, block.y), (194, 178, 128))
            block.update()

        scaled_surface = pygame.transform.scale(surface, (CANVAS_WIDTH, CANVAS_HEIGHT))
        WINDOW.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def update_fps():
        fps = str(int(clock.get_fps()))

    def get_line_points(x0, y0, xf, yf):
        # 20, 20, 20, 10
        distance = math.dist((x0,y0), (xf,yf))

        dx = (xf - x0) / distance
        dy = (yf - y0) / distance

        points = []

        start_x, end_x = (x0, xf)
        start_y, end_y = (y0, yf)

        for i in range(math.ceil(distance)):
            points.append((round(start_x), round(start_y)))
            start_x += dx
            start_y += dy
        
        return points

    def draw_bucket():
        line = []
        line += get_line_points(15, 10, 10, 15) + get_line_points(10, 15, 15, 20) + get_line_points(15, 20, 20, 15)


        for point in line:
            new_block = StoneBlock(point[0], point[1])
            particle_map[point[0]][point[1]] = 1
            blocks.append(new_block)



    def draw_hands(results):
        for hand_no, hand_landmarks in enumerate(results):
            wrist_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * CANVAS_WIDTH
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * CANVAS_HEIGHT

            thumb_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * CANVAS_WIDTH
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * CANVAS_HEIGHT

            thumb_to_index_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x) / 2 * CANVAS_WIDTH
            thumb_to_index_y = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

            index_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * CANVAS_WIDTH
            index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * CANVAS_HEIGHT

            index_to_middle_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
            index_to_middle_y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

            middle_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * CANVAS_WIDTH
            middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * CANVAS_HEIGHT

            middle_to_ring_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
            middle_to_ring_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

            ring_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * CANVAS_WIDTH
            ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * CANVAS_HEIGHT

            ring_to_pinky_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x) / 2 * CANVAS_WIDTH
            ring_to_pinky_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y) / 2 * CANVAS_HEIGHT

            pinky_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * CANVAS_WIDTH
            pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * CANVAS_HEIGHT

            pygame.draw.polygon(screen, (255, 0, 0), ((wrist_x, wrist_y), (thumb_x, thumb_y), (thumb_to_index_x, thumb_to_index_y), (index_x, index_y), (index_to_middle_x, index_to_middle_y), (middle_x, middle_y), (middle_to_ring_x, middle_to_ring_y), (ring_x, ring_y), (ring_to_pinky_x, ring_to_pinky_y), (pinky_x, pinky_y)))


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

            if (particle_map[new_x][new_y] != 1):
                new_block = SandBlock(new_x, new_y)
                particle_map[new_x][new_y] = 1
                blocks.append(new_block)


        draw_bucket()
        render()
        update_fps()



    root.mainloop()
