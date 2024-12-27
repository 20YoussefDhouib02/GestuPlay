import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed
import time

detector = HandDetector(detectionCon=0.85, maxHands=1)

space_key_pressed = space_pressed

time.sleep(2.0)

current_key_pressed = set()

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1360)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1040)

overlay_image = cv2.imread("./cs-logo.png") 
overlay_image_resized = cv2.resize(overlay_image, (324, 100))

hand_color = (255, 0, 255)
text_color = (255, 255, 255)

while True:
    ret, frame = video.read()
    keyPressed = False
    spacePressed = False
    key_count = 0
    key_pressed = 0   
    hands, img = detector.findHands(frame)

    cv2.rectangle(img, (0, 665), (300, 1282), (26, 164, 250), -2) 
    cv2.rectangle(img, (1060, 665), (1282, 720), (26, 164, 250), -2)  

    frame_height, frame_width, _ = frame.shape
    x_offset = frame_width - overlay_image_resized.shape[1]
    y_offset = 0 
    frame[y_offset:y_offset + overlay_image_resized.shape[0], x_offset:x_offset + overlay_image_resized.shape[1]] = overlay_image_resized
    
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            fingerUp = detector.fingersUp(hand)
            print(fingerUp)
            
            for lm in lmList:
                cv2.circle(frame, (int(lm[0]), int(lm[1])), 4, hand_color, cv2.FILLED)
            
            total=sum(fingerUp)
            if total == 0:
                cv2.putText(frame, 'Finger Count: 0', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, '  STOP', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                PressKey(space_key_pressed)
                spacePressed = True
                current_key_pressed.add(space_key_pressed)
                key_pressed = space_key_pressed
                keyPressed = True
                key_count = key_count + 1
            if total == 1:
                cv2.putText(frame, 'Finger Count: 1', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, 'Moving...', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
            if total == 2:
                cv2.putText(frame, 'Finger Count: 2', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, 'Moving...', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
            if total == 3:
                cv2.putText(frame, 'Finger Count: 3', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, 'Moving...', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
            if total == 4:
                cv2.putText(frame, 'Finger Count: 4', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, 'Moving...', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
            if total == 5:
                cv2.putText(frame, 'Finger Count: 5', (10, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
                cv2.putText(frame, 'Moving...', (1100, 700), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 1, cv2.LINE_AA)
            
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
            elif key_count == 1 and len(current_key_pressed) == 2:    
                for key in current_key_pressed:             
                    if key_pressed != key:
                        ReleaseKey(key)
                current_key_pressed = set()
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
