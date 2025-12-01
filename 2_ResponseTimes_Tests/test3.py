import cv2
import time
import os
import RPi.GPIO as GPIO
import numpy as np

"""
DIRECTORY
_______________________________
"""

filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory, sub_folder)
images_path = os.path.join(images_tosubpath, filename)

os.makedirs(images_tosubpath, exist_ok=True)


"""
BREAK BEAM SETUP
_______________________________________________________
"""

BEAM_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_beam_break_nonblocking():
    print("Waiting for beam break...")

    while GPIO.input(BEAM_PIN) == 1:
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam broken!")

    print("Waiting for beam restore...")
    while GPIO.input(BEAM_PIN) == 0:
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam unbroken!")


"""
PHOTO CAPTURE
_______________________________________________
"""

def take_picture():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Not inverted for now
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Capture time is three seconds
    time.sleep(3)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("ERROR: Could not capture image.")
        return None

    cv2.imwrite(images_path, frame)
    print("Picture saved:", images_path)

    return frame


"""
FADE IN RAM
_______________________
"""

# cv2.namedWindow("Fade Preview", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Fade Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def fade_to_black_cv(img, level):
    
    faded = cv2.convertScaleAbs(img, alpha=level, beta=0)
    
    cv2.imshow("Fade Preview", faded)
    cv2.waitKey(1)


def increment_fade(img):
    fade_steps = [1.0, 0.7, 0.4, 0.2, 0.0]
    fade_steps = [0.7, 0.4, 0.2, 0.0]
    
    # cv2.namedWindow("Fade Preview", img) for first preview
    # cv2.setWindowProperty("Fade Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    for level in fade_steps:
        wait_for_beam_break_nonblocking()
        print("Applying fade level:", level)
        fade_to_black_cv(img, level)
    
    # time.sleep(10) attempt to hold last image 


"""
PROGRAM START
___________________________

"""


try:
    userInput = input("Please click Enter: ")

    if userInput == "":
        img = take_picture()   

        if img is not None:
            increment_fade(img)
        else:
            print("No image captured.")
    else:
        print("You didn't press Enter.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
    cv2.destroyAllWindows()

    # Needs to loop
