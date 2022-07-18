import pygame
import sys
import time
from datetime import datetime
import mediapipe as mp
import random

mp_hands  = mp.solutions.hands

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
PARTICLE_SIZE = 5

blocks=[]

class SandBlock(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.x = posX
        self.y = posY
        self.size = PARTICLE_SIZE
    
    def update(self):
        screen.set_at(self.x, self.y, (0,0,0))

        if (self.y * self.size + self.size >= CANVAS_HEIGHT):
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
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("sandbox")


def game_loop(q):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();

        try:
            results = q.get()
            while not q.empty():
                results = q.get()
        except IndexError:
            print("index error")
            pass

        #draw hands
        # if not results:
        #     continue
        for i in range(20):
            new_x = random.randint(0, CANVAS_WIDTH/PARTICLE_SIZE-1)
            new_y = 5

            new_block = SandBlock(new_x, new_y)
            particle_map[new_x][new_y] = 1
            blocks.append(new_block)



        # for hand_no, hand_landmarks in enumerate(results):
        #     wrist_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * CANVAS_WIDTH
        #     wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * CANVAS_HEIGHT

        #     thumb_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * CANVAS_WIDTH
        #     thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * CANVAS_HEIGHT

        #     thumb_to_index_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x) / 2 * CANVAS_WIDTH
        #     thumb_to_index_y = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y + hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

        #     index_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * CANVAS_WIDTH
        #     index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * CANVAS_HEIGHT

        #     index_to_middle_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
        #     index_to_middle_y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

        #     middle_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * CANVAS_WIDTH
        #     middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * CANVAS_HEIGHT

        #     middle_to_ring_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2 * CANVAS_WIDTH
        #     middle_to_ring_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2 * CANVAS_HEIGHT

        #     ring_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * CANVAS_WIDTH
        #     ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * CANVAS_HEIGHT

        #     ring_to_pinky_x = CANVAS_WIDTH - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x) / 2 * CANVAS_WIDTH
        #     ring_to_pinky_y = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y + hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y) / 2 * CANVAS_HEIGHT

        #     pinky_x = CANVAS_WIDTH - hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * CANVAS_WIDTH
        #     pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * CANVAS_HEIGHT

        #     canvas.create_polygon(wrist_x, wrist_y, thumb_x, thumb_y, thumb_to_index_x, thumb_to_index_y, index_x, index_y, index_to_middle_x, index_to_middle_y, middle_x, middle_y, middle_to_ring_x, middle_to_ring_y, ring_x, ring_y, ring_to_pinky_x, ring_to_pinky_y, pinky_x, pinky_y, fill="red")

        for block in blocks:
            block.updatePos()
            print(block.x)
            pygame.draw.rect(screen, (194, 178, 128), (block.x * block.size, block.y * block.size, block.size, block.size))
        pygame.display.update()


    root.mainloop()
