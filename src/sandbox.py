import pygame
import sys
from bucket import Bucket
from blocks import SandBlock, WaterBlock, StoneBlock, BucketBlock
from tilemap import TileMap

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
PARTICLE_SIZE = 5

class UserInput():
    def __init__(self):
        self.prev_mouse_point = None
        self.block_type = 1

    def update_block_type(self):
        # 1 - sand, 2 - water, 3 - stone
        if pygame.key.get_pressed()[pygame.K_1]:
            self.block_type = 1
        elif pygame.key.get_pressed()[pygame.K_2]:
            self.block_type = 2
        elif pygame.key.get_pressed()[pygame.K_3]:
            self.block_type = 3
    
    def get_mouse_pos(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            
            new_point = (int(x / PARTICLE_SIZE), int(y / PARTICLE_SIZE))
            old_point = self.prev_mouse_point
            self.prev_mouse_point = new_point
            return (old_point, new_point)
        else:
            self.prev_mouse_point = None
            return None
            # points = [new_point]

            # if (self.prev_mouse_point != None):
            #     points = get_line_points(self.prev_mouse_point, new_point)
                

            # for point in points:
            #     if (particle_map[point[0]][point[1]] == None):
            #         if (self.curr_block_type == 1):
            #             new_block = SandBlock(point[0], point[1])
            #         elif (self.curr_block_type == 2):
            #             new_block = WaterBlock(point[0], point[1])
            #         elif (self.curr_block_type == 3):
            #             new_block = StoneBlock(point[0], point[1])

            #         particle_map[point[0]][point[1]] = new_block
            
            # self.prev_mouse_point = new_point
        # else:
        #     self.prev_mouse_point = None


def game_loop(q):
    pygame.init()
    WINDOW = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("sandbox")
    font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    player_input = UserInput()
    tilemap = TileMap(CANVAS_WIDTH, CANVAS_HEIGHT, PARTICLE_SIZE)
    bucket = Bucket()


    def render():
        # record tiles that have been updated
        # updated_tiles = {}

        # for row, array in reversed(list(enumerate(tilemap.map))):
        #     for column, tile in reversed(list(enumerate(array))):
        #         if tile != None and (row, column) not in updated_tiles:
        #             surface.set_at((row, column), tile.color)
        #             updated_tile = tile.update()
        #             updated_tiles[updated_tile] = True

        surface = pygame.Surface((tilemap.width, tilemap.height))

        for row, array in enumerate(tilemap.map):
            for column, tile in enumerate(array):
                if tile != None:
                    surface.set_at((row, column), tile.color)


        scaled_surface = pygame.transform.scale(surface, (CANVAS_WIDTH, CANVAS_HEIGHT))
        scaled_surface.blit(update_fps(), (10,0))
        WINDOW.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    while True:
        # run at max fps
        clock.tick(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_c]:
                tilemap.clear()

        try:
            # get most recent hand position
            results = q.get()
            while not q.empty():
                results = q.get()
        except IndexError:
            print("index error")
            pass

        player_input.update_block_type()
        block_to_be_drawn = player_input.block_type
        mouse_pos = player_input.get_mouse_pos()
        
        old_bucket_vertices, new_bucket_vertices = bucket.get_vertices(results, tilemap.width, tilemap.height)
        tilemap.update(mouse_pos, block_to_be_drawn, old_bucket_vertices, new_bucket_vertices)

        render()
        update_fps()

        # remove all past hand blocks
        if bucket.vertices != None:
            for point in bucket.vertices:
                if (point[0] < 0 or point[0] > tilemap.width - 1 or point[1] < 0 or point[1] > tilemap.height - 1): continue

                if type(tilemap.map[point[0]][point[1]]).__name__ == "BucketBlock":
                    tilemap.map[point[0]][point[1]] = None                

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
