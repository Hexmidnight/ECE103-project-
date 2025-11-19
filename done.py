import subprocess
import time
from PIL import Image
import os

# ------------------------
# FADING / OPACITY FUNCTIONS
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


def set_image_opacity(opacity_level):
    img = Image.open(images_path).convert("RGBA")
    img.putalpha(opacity_level)
    img.save(output_images_path)
    print(f"Image saved with opacity {opacity_level}")


def fading():
    for opacity in [25, 50, 75, 100, 125, 150, 175, 255]:
        set_image_opacity(opacity)
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
    # 1. Take 1 main picture
    take_picture()

    # 2. Fade it
    fading()

    # 3. Take the 10-photo series
    camera = Photo()
    camera.capture_photos()

else:
    print("You didn't press Enter.")
