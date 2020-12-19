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

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(Cameras.EXTERNAL.value)

    prev_pupils = [(1.0,1.0) for i in range(5)]
    curr_pupils = [(1.0,1.0) for i in range(5)]

    counter = 0

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        if (counter % 2 == 0):
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