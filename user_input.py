import subprocess
import time


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

# Prompt the user to click Enter to take photo of them 
userInput = input("Please click Enter: ")

# If they actually pressed Enter (empty string)
if userInput == "":
    camera = Photo()
    camera.capture_photos()
else:
    print("You didn't press Enter.")
