import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands  = mp.solutions.hands

def trackHands(q):
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity = 0,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("ignoring empty camera frame")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # draw hand annotations on image
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            q.put(results.multi_hand_landmarks)

            # if results.multi_hand_landmarks:
            #     for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):

            #         print(f'HAND NUMBER: {hand_no+1}')
            #         print('-----------------------')
                    
            #         for i in range(21):    
            #             print(f'{mp_hands.HandLandmark(i).name}:') 
            #             print(f'x: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].x}')
            #             print(f'y: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].y}')
            #             print(f'z: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].z}n')


            #         mp_drawing.draw_landmarks(
            #             image,
            #             hand_landmarks,
            #             mp_hands.HAND_CONNECTIONS,
            #             mp_drawing_styles.get_default_hand_landmarks_style(),
            #             mp_drawing_styles.get_default_hand_connections_style())
            #     # Flip the image horizontally for a selfie-view display.
            #     cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            #     if cv2.waitKey(5) & 0xFF == 27:
            #         break
    cap.release()
