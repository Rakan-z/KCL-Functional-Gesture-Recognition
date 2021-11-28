I verify that I am the sole author of the programs contained in this folder, except where explicitly stated to the contrary - Rakan Zabian.



1---- Before running ensure that the following libraries are pip installed:

cv2
mediapipe
numpy
time
autopy
math
pyautogui
speech_recognition 
io
pathlib
PIL
PySimpleGUI
os


Once the libraries are installed, run the system by following the steps below.

2---- Using an IDE, run GUI_init.py and as you click on each button, its coordinates will be output


3---- Modify pyautoguiFunctions.py to include these coordinates, no need to pass the last 2 coordinates for the scroll function, unless you want the cursor to move to specific position before scrolling


4---- Using terminal (bash):

cd ~/folderPath---->python GRmodel.py & python GUI.py &


5---- Use the gestures to control the system. Make sure that you, your arm and your wrist are facing the webcam directly. I would advise you to keep your non active hand behind your back, this avoids detection errors. Make sure the webcam is closed if you are to rerun the program. If an error with cv2.cvtcolor appears, force quit python to close the webcam and restart the kernel. This should not occur if you run using terminal only.