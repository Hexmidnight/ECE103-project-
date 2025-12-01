from PIL import Image

import os
import subprocess
import time

#Input Path
filename = "pic.png"
sub_folder = "PhotoInput"
current_directory = os.getcwd()
images_tosubpath = os.path.join(current_directory,sub_folder)
images_path = os.path.join(images_tosubpath,filename)

#Output Path
output_filename = "pic.png"
output_sub_folder = "PhotoOutput"
output_current_directory = os.getcwd()
output_images_tosubpath = os.path.join(output_current_directory,output_sub_folder)
output_images_path = os.path.join(output_images_tosubpath,output_filename)

def take_picture():
    command = [
        "fswebcam",
        "-d", "/dev/video0",
        "-r", "1280x720",
        "-S", "60", #skip first 60 frames
        # "--no-banner", if we don't want a banner on bottom
        images_path
    ]
    subprocess.call(command)
    print('Pic Captured')

def get_picture():
    images_path

def set_image_opacity(opacity_level):
    img = Image.open(images_path).convert('RGBA') 
    
    #opacity_level = 25
    img.putalpha(opacity_level) #opacity level 0-255
    
    img.save(output_images_path)
    print(f"Image saved with opacity {opacity_level} to {output_images_path}")

def fading():
    set_image_opacity(25)
    time.sleep(0.2)
    set_image_opacity(50)
    time.sleep(0.2)
    set_image_opacity(75)
    time.sleep(0.2)
    set_image_opacity(100)
    time.sleep(0.2)
    set_image_opacity(125)
    time.sleep(0.2)
    set_image_opacity(150)
    time.sleep(0.2)
    set_image_opacity(175)
    time.sleep(0.2)
    set_image_opacity(255)
    time.sleep(0.2)

if __name__=="__main__":
    take_picture()
    fading()

