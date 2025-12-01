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

def break_beam_callback(channel):
    if GPIO.input(BEAM_PIN):
        print("beam unbroken")
    else:
        print("beam broken")

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)

def wait_for_beam_break():
    """
    Block until the beam 
    is broken (input goes LOW), 
    then wait for it to reset.
    """
    print("Waiting for beam break to take photo...")
    # Wait until beam goes low (broken)
    while GPIO.input(BEAM_PIN):  # HIGH = unbroken
        time.sleep(0.01)
    print("Beam broken → taking photo")

"""

Image/Fading Function

"""

def take_picture():
    command = [
        "fswebcam",
        "-d", "/dev/video0",  # With no other webcam devices, this is default
        "-r", "1920x1080", 
        "-S", "60",  # 60 Frames Skipped
        images_path
    ]
    subprocess.call(command)
    print("Pic Captured:", images_path)


def fade_to_black(level, index):
    """
    level:
      1.0 = full brightness
      0.0 = black
    index:
      which fade step (0,1,2,...)
    """
    img = Image.open(images_path).convert("RGB")
    enhancer = ImageEnhance.Brightness(img)
    darker = enhancer.enhance(level)

    fade_filename = f"fade_{index}.png"
    fade_path = os.path.join(output_images_tosubpath, fade_filename)     
    darker.save(fade_path)

     try:
        to_preview = Image.open(fade_path)
        time.sleep(0.5)
    except FileNotFoundError:
        print("File Not Found")


    print(f"Saved brightness level {level} -> {fade_path}")


def increment_fade_og():
    # Smooth fade from full brightness -> black
    fade_steps = [1.0, 0.7, 0.4, 0.2, 0.0] # For five pages

    for idx, level in enumerate(fade_steps):
        fade_to_black(level, idx)
        time.sleep(0.2)


# def on_time():
    #
    #Prompt: button combo to restart
    #show binder opens: picture taken 100
    #show Page turn to 2: 70
    #show Page turn to 3: 40
    #show Page turn to 4: 20
    #show Page turn to 0: 0
    #Bug: If page turns back it too is detected as a turn
    #   
"""
class Photo:
    def __init__(self):
        self.i = 0
        self.to_continue = True

    def capture_photos(self):
        wait_for_beam_break()
        

        try:
            while self.to_continue != True:
                # Wait for sensor event before each photo
                wait_for_beam_break()

                filename = f"{self.i}pic.jpg"

                subprocess.run(
                    f"fswebcam -d /dev/video0 -r 1280x720 -S0 {filename}",
                    shell=True
                )

                print("Pic Captured:", filename)

                self.i += 1
                time.sleep(0.2)

        except KeyboardInterrupt:
            print("lol")

"""

"""

User Input
--In current state, break beam fades altogether, make it fade per
turn

"""

try:
    userInput = input("Please click Enter: ")

    if userInput == "":

        # 
        wait_for_beam_break()

        #
        take_picture()

        # 2. Fade it to black (multiple files: fade_0.png ... fade_6.png)
        fading()

        """
        # 3. Take the 10-photo series, each triggered by the beam
        camera = Photo()
        camera.capture_photos()
        """


    else:
        print("You didn't press Enter.")

finally:
    # Always clean up GPIO when exiting
    GPIO.cleanup()
    print("GPIO cleaned up.")
