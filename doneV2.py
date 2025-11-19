import subprocess
import time
from PIL import Image, ImageEnhance
import os

# ------------------------
# PATH SETUP
# ------------------------

filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory, sub_folder)
images_path = os.path.join(images_tosubpath, filename)

output_filename = "pic.png"
output_sub_folder = "PhotoOutput"
output_current_directory = os.getcwd()
output_images_tosubpath = os.path.join(output_current_directory, output_sub_folder)
output_images_path = os.path.join(output_images_tosubpath, output_filename)

# Ensure folders exist
os.makedirs(images_tosubpath, exist_ok=True)
os.makedirs(output_images_tosubpath, exist_ok=True)


# ------------------------
# IMAGE FADE FUNCTIONS
# ------------------------

def take_picture():
    command = [
        "fswebcam",
        "-d", "/dev/video0",
        "-r", "1280x720",
        "-S", "60",
        images_path
    ]
    subprocess.call(command)
    print("Pic Captured")


def fade_to_black(level):
    """
    level:
      1.0 = full brightness
      0.0 = black
    """
    img = Image.open(images_path).convert("RGB")
    enhancer = ImageEnhance.Brightness(img)
    darker = enhancer.enhance(level)
    darker.save(output_images_path)
    print(f"Saved brightness level {level}")


def fading():
    # Smooth fade from full brightness -> black
    fade_steps = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]

    for level in fade_steps:
        fade_to_black(level)
        time.sleep(0.2)


# ------------------------
# PHOTO CLASS FOR 10 SHOTS
# ------------------------

class Photo:
    def __init__(self):
        self.i = 0

    def capture_photos(self):
        try:
            while self.i != 10:
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


# ------------------------
# USER INPUT TRIGGER
# ------------------------

userInput = input("Please click Enter: ")

if userInput == "":
    # 1. Take initial picture
    take_picture()

    # 2. Fade it to black
    fading()

    # 3. Take the 10-photo series
    camera = Photo()
    camera.capture_photos()

else:
    print("You didn't press Enter.")
