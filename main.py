import os
import enum
import cv2
from GazeTracking.gaze_tracking import GazeTracking

class Cameras(enum.Enum):
    EXTERNAL = 0
    BUILT_IN = 1

def activateZoom():
    os.system("""osascript -e 'activate application "zoom.us"'""")

def toggleCamera(camera):
    print("Switching Camera to", camera)
    os.system("""osascript -e 'tell application "System Events"' -e 'keystroke "n" using {command down, shift down}' -e 'end tell'""")

def deactivateZoom():
    os.system("""osascript -e 'tell application "System Events"' -e 'keystroke tab using command down' -e 'end tell'""")

def listAllNone(list):
    for item in list:
        if item != (None, None): return False
    return True

def listNotNone(list):
    for item in list:
        if item == (None, None): return False
    return True

def main():
    camera = Cameras.EXTERNAL
    bufferSize = 30 # change this number to increase the time it takes to switch cameras, righnow its around 10 secs
    counter = 0 
    mod = 3 # this one as well

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(Cameras.EXTERNAL.value)

    prev_pupils = [(1.0,1.0) for i in range(bufferSize)]
    curr_pupils = [(1.0,1.0) for i in range(bufferSize)]

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # limits the number of samples taken
        if (counter % mod == 0):
            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()

            prev_pupils.pop(0)
            prev_pupils.append(curr_pupils.pop(0))
            curr_pupils.append((left_pupil,right_pupil))

            if ((listAllNone(curr_pupils) and listNotNone(prev_pupils))
                or (listNotNone(curr_pupils) and listAllNone(prev_pupils))):
                
                activateZoom()
                
                if camera == Cameras.EXTERNAL: camera = Cameras.BUILT_IN
                else: camera = Cameras.EXTERNAL
                
                toggleCamera(camera)
                deactivateZoom()

        counter += 1


if __name__ == "__main__":
    main()