import cv2
import time
import os
from PIL import Image, ImageEnhance
import numpy as np
import RPi.GPIO as GPIO

"""
DIRECTORIES
_______________________
"""

filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory, sub_folder)
images_path = os.path.join(images_tosubpath, filename)

output_sub_folder = "PhotoOutput"
output_current_directory = os.getcwd()
output_images_tosubpath = os.path.join(output_current_directory, output_sub_folder)

os.makedirs(images_tosubpath, exist_ok=True)
os.makedirs(output_images_tosubpath, exist_ok=True)


"""
BREAK BEAM SENSOR SETUP
_____________________________________
"""

BEAM_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_beam_break():
    print("Waiting for beam break...")
    GPIO.wait_for_edge(BEAM_PIN, GPIO.FALLING)
    print("Beam broken!")

    print("Waiting for beam restore...")
    GPIO.wait_for_edge(BEAM_PIN, GPIO.RISING)
    print("Beam restored.")


"""
PHOTO CAPTURE
__________________________________________

CHANGES:
1. REMOVED fswebcam.
   - fswebcam is slowwwww and has a 20–80 success rate.

2. Replaced with OpenCV VideoCapture 

3. Captures directly into RAM AND writes once to disk.
"""

def take_picture():
    global original_cv_image

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # Warmup
    time.sleep(0.2)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("ERROR: Could not capture image.")
        return False

    # Saves
    cv2.imwrite(images_path, frame)

    # Saves to RAM copy for faster performance
    original_cv_image = frame.copy()

    print("Picture captured:", images_path)
    return True


"""
============================================
FADE HANDLING — SECOND BIGGEST CHANGE
============================================

CHANGES:
1. Implements fade function in RAM:
      - Convert the original captured frame
      - Fades using PIL
      - Convert directly back to OpenCVs
      - Shows

2. Saves final fades to disk AFTER showing them
"""

cv2.namedWindow("Fade Preview", cv2.WINDOW_NORMAL)

def fade_frame(level):
    """
    Apply brightness fade in RAM
    """

    # Convert OpenCV (BGR) -> PIL (RGB)
    img_pil = Image.fromarray(cv2.cvtColor(original_cv_image, cv2.COLOR_BGR2RGB))

    enhancer = ImageEnhance.Brightness(img_pil)
    darker = enhancer.enhance(level)

    # Convert back to OpenCV (RGB -> BGR)
    result = cv2.cvtColor(np.array(darker), cv2.COLOR_RGB2BGR)

    return result


def increment_fade():
    """
    Now previews instantly and saves output afterward.
    """

    fade_steps = [1.0, 0.7, 0.4, 0.2, 0.0]

    for idx, level in enumerate(fade_steps):
        wait_for_beam_break()

        # Generate faded image FAST (RAM only)
        faded = fade_frame(level)

        # Preview instantly
        cv2.imshow("Fade Preview", faded)
        cv2.waitKey(1)

        # Save output PNG
        fade_filename = f"fade_{idx}.png"
        fade_path = os.path.join(output_images_tosubpath, fade_filename)
        cv2.imwrite(fade_path, faded)

        print(f"Saved brightness level {level} → {fade_path}")


"""
APP START
____________________________________________
"""

try:
    userInput = input("Press Enter to start: ")

    if userInput == "":
        if take_picture():      # Fast, reliable capture
            increment_fade()    # Fast in-RAM fades
    else:
        print("You didn't press Enter.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")

cv2.destroyAllWindows()
