import cv2 
import subprocess
import time
from PIL import Image, ImageEnhance
import os
import RPi.GPIO as GPIO

"""
Photo Directories
"""

# InputPath
filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory, sub_folder)
images_path = os.path.join(images_tosubpath, filename)

# OutputPath
output_sub_folder = "PhotoOutput"
output_current_directory = os.getcwd()
output_images_tosubpath = os.path.join(output_current_directory, output_sub_folder)

# Ensure folders exist
os.makedirs(images_tosubpath, exist_ok=True)
os.makedirs(output_images_tosubpath, exist_ok=True)

"""
Break Beam Sensor Setup
"""

BEAM_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_beam_break():
    """
    Wait for a clean beam break (FALLING) and then beam restore (RISING)
    """
    print("Waiting for beam break to take photo...")
    GPIO.wait_for_edge(BEAM_PIN, GPIO.FALLING)
    print("Beam broken")

    print("Waiting for beam to be unbroken...")
    GPIO.wait_for_edge(BEAM_PIN, GPIO.RISING)
    print("Beam unbroken, ready for next step.")

"""
Image/Fading Functions
"""

def take_picture():
    command = [
        "fswebcam",
        "-d", "/dev/video0",
        "-r", "854x480",
        "-S", "60",
        images_path
    ]
    subprocess.call(command)
    print("Pic Captured:", images_path)


cv2.namedWindow("Fade Preview", cv2.WINDOW_NORMAL)

def fade_to_black(level, index):
    img = Image.open(images_path).convert("RGB")
    enhancer = ImageEnhance.Brightness(img)
    darker = enhancer.enhance(level)

    fade_filename = f"fade_{index}.png"
    fade_path = os.path.join(output_images_tosubpath, fade_filename)
    darker.save(fade_path)

    # Display with OpenCV
    cv_img = cv2.imread(fade_path)
    cv2.imshow("Fade Preview", cv_img)
    cv2.waitKey(1)

    print(f"Saved brightness level {level} -> {fade_path}")


def increment_fade():
    """
    Wait for sensor -> show next fade frame
    """
    fade_steps = [1.0, 0.7, 0.4, 0.2, 0.0]  # Five pages / fades

    for idx, level in enumerate(fade_steps):
        wait_for_beam_break()
        fade_to_black(level, idx)


"""
User Input / Main Flow
"""

try:
    userInput = input("Please click Enter: ")

    if userInput == "":
        take_picture()      # Take original image for fading
        increment_fade()    # Fade based on beam sensor events
    else:
        print("You didn't press Enter.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")

cv2.destroyAllWindows()
