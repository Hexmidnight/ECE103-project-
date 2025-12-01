
import cv2
import time
import os
import RPi.GPIO as GPIO
import numpy as np

"""
=========================================================
1. DIRECTORY SETUP
=========================================================
Only save ONE picture: the original. Fades are done in
memory now, not written to disk.
=========================================================
"""

filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory, sub_folder)
images_path = os.path.join(images_tosubpath, filename)

os.makedirs(images_tosubpath, exist_ok=True)


"""
=========================================================
2. BREAK BEAM SETUP (Non-blocking version)
=========================================================
This keeps OpenCV responsive by avoiding wait_for_edge(),
which freezes the GUI. We poll instead.
=========================================================
"""

BEAM_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_beam_break_nonblocking():
    print("Waiting for beam break...")

    # FALLING: beam becomes broken
    while GPIO.input(BEAM_PIN) == 1:
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam broken!")

    # RISING: beam restored
    print("Waiting for beam restore...")
    while GPIO.input(BEAM_PIN) == 0:
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam unbroken!")


"""
=========================================================
3. CAPTURE IMAGE USING OPENCV
=========================================================
This is much faster and more reliable than fswebcam.
We also force MJPEG for speed on Logitech USB cams.
=========================================================
"""

def take_picture():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Logitech fast settings
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # reliable resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Give camera a moment to adjust
    time.sleep(0.5)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("ERROR: Could not capture image.")
        return None

    cv2.imwrite(images_path, frame)
    print("Picture saved:", images_path)

    return frame   # Return image in memory for faster fades


"""
=========================================================
4. FAST FADE USING OPENCV ONLY
=========================================================
This replaces PIL brightness + PNG disk writes + PNG reads.
We multiply the image directly in memory → instant.
=========================================================
"""

cv2.namedWindow("Fade Preview", cv2.WINDOW_NORMAL)

cv2.setWindowProperty("Fade Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def fade_to_black_cv(img, level):
    # Multiply image brightness by level
    faded = (img.astype(np.float32) * level).astype(np.uint8)

    # Show instantly without blocking
    cv2.imshow("Fade Preview", faded)
    cv2.waitKey(1)


def increment_fade(img):
    fade_steps = [1.0, 0.7, 0.4, 0.2, 0.0]

    for level in fade_steps:
        wait_for_beam_break_nonblocking()
        print("Applying fade level:", level)
        fade_to_black_cv(img, level)


"""
=========================================================
5. MAIN FLOW
=========================================================
"""

try:
    userInput = input("Please click Enter: ")

    if userInput == "":
        img = take_picture()   # Capture only once

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
