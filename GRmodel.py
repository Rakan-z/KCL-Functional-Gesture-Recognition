import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import math
import pyautoguiFunctions
import pyautogui
import speech_recognition as sr


#### Inputs

#######################
wCam, hCam = 640, 480  # Set webcam screen size
frameR = 100  # Set frame reduction factor to build rectangle (reduced screen) which represents actual screen for cursor control
wScr, hScr = autopy.screen.size()  # Get actual screen size
smoothening = 5  # Smoothening factor to determine cursor control speed
plocX, plocY = 0, 0  # Initialization of initial cursor location
clocX, clocY = 0, 0  # Initialization of current cursor location
detector = htm.handDetector(detectionCon = 0.7)  # Object of handDetector class from htm module, creates attributes containing MediaPipe model outputs
speech_duration = 3 # Speech detection duration
click_threshold = 40 # Distance between index & middle fingertips to determine wether to click cursor or not
zoom_threshold = 50 # Distance between thumb and index fingertips to determine wether zoom in or out/brighten or darken
#######################


#### Open webcam & set to initialized size

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)



while True: # While webcam is open
    
    #### Find hand landmarks using MediaPipe detection models
    
    success, img = cap.read() # Collect raw image data using OpenCV
    
    img, landmarks = detector.findHands(img) # img is the frame with annotated landmark connections and landmarks contains hand landmarks which will be
                                             # used to determine wether left or right hand is detected
        
    lmList, bbox = detector.findPosition(img) # lmList [landmark ID, x, y] contains MediaPipe multi hand landmark coordinates and bbox contains box coordinates (to draw a 
                                              # box around detected hand)

    
    
    if len(lmList) != 0: # If landmarks are detected        
    
        fingers = detector.fingersUp() # check which fingers are up: 1 if finger up, 0 if down. [bool,bool,bool,bool,bool ]

        #### CURSOR CONTROL

        # Get the (x,y) of the tips of the index and middle fingers
        x1, y1 = lmList[8][1:] 
        x2, y2 = lmList[12][1:]


        # HOVER
        if fingers[1:5] == [1,0,0,0]: # If hover gesture is detected

            # create rectangle to represent screen
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

            # find coordinates of index fingertip
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr)) 
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # smoothen values to ease cursor control
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY) # move mouse relative to fingertip coordinates
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # CLICK
        if fingers[1:5] == [1,1,0,0]: # If click gesture is detected

            length, img, lineInfo = detector.findDistance(8, 12, img) # find distance between index & middle fingertips

            if length < click_threshold:

                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()  # click mouse if distance is below threshold



        #### SLIDESHOW
        if landmarks.left_hand_landmarks and fingers == [0,0,0,0,1]:
            pyautoguiFunctions.previousImg() # click previous button if previous gesture is detected
            time.sleep(1) # to slow down the command invocation
        elif landmarks.right_hand_landmarks and fingers == [1,0,0,0,1]:
            pyautoguiFunctions.nextImg() # click next button if next gesture is detected
            time.sleep(1)



        #### ZOOM 
        if landmarks.right_hand_landmarks and fingers == [1,1,0,0,0]: # If zoom gesture is detected

            length, img, lineInfo = detector.findDistance(4, 8, img) # find distance between index & middle fingertips

            if length > zoom_threshold:
                pyautoguiFunctions.zoomIn() # click zoom in button if distance is above threshold
                time.sleep(1)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            else:
                pyautoguiFunctions.zoomOut() # click zoom out button if distance is below threshold
                time.sleep(1)

        #### BRIGHTNESS
        if landmarks.left_hand_landmarks and fingers == [0,1,0,0,0]: # If brightness gesture is detected

            length, img, lineInfo = detector.findDistance(4, 8, img) # find distance between index & middle fingertips

            if length > zoom_threshold:
                pyautoguiFunctions.Brighten() # click brighten button if distance is above threshold
                time.sleep(1)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            else:
                pyautoguiFunctions.Darken() # click darken button if distance is above threshold
                time.sleep(1)

        #### SCROLL
        down = detector.fingersDown() # variable with number of fingers below wrist

        if fingers[1:5]==[1,1,1,1]: # if scroll up gesture is detected
            pyautoguiFunctions.scrollUp() # automate mouse scrolling upwards
            time.sleep(1)
        elif down == 4: # if scroll down gesture is detected
            pyautoguiFunctions.scrollDown() # automate mouse scrolling downwards
            time.sleep(1)
        elif landmarks.right_hand_landmarks and fingers == [0,1,0,0,1]: # if scroll right gesture is detected
            pyautoguiFunctions.scrollRight() # automate mouse scrolling right
            time.sleep(1)
        elif landmarks.left_hand_landmarks and fingers == [1,1,0,0,1]: # if scroll left gesture is detected
            pyautoguiFunctions.scrollLeft() # automate mouse scrolling left
            time.sleep(1)

        
        #### SPEECH 
        
        if landmarks.right_hand_landmarks and landmarks.left_hand_landmarks: # If both hands are detected in the frame
                            
            if fingers[1:5] == [0,0,0,0]: # and If backspace gesture is detected
                pyautogui.press('backspace') # Backspace on keyboard
                
                
            elif fingers[1:5] == [1,1,1,1]: # else If speech activation gesture is detected 
                
                print('typing') 
                r = sr.Recognizer() # Create object from speech_recognition
                with sr.Microphone() as source: # Input audio data from default microphone
                    
                    audio_data = r.record(source, duration=speech_duration) # read the audio data from the microphone for 3 seconds
                    
                    # Convert speech to text
                    try:
                        text = r.recognize_google(audio_data) # text string variable
                        pyautogui.typewrite(text) # automate keyboard commands to type text
                        pyautogui.press('enter') # enter to search 
                    except:
                        pass # if no speech detected, pass onto CURSOR CONTROL
                
                
    #### Display webcam feed on screen
#     cv2.imshow("OpenCV feed", img)
    
    # Close webcam if 'q' is clicked
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
