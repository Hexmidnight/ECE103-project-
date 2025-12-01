import subprocess
import time

i = 0


# Takes 10 photos in succession in 720p, stores them as [i]pic.jpg

try:
    while i != 10:
        subprocess.call("fswebcam -d /dev/video0 -r 1280x720 -S0 " + str(i) + "pic.jpg", shell=True)
        print('Pic Captured')
        
        i+=1
        
        time.sleep(0.2)

except KeyboardInterupt:
    print('lol')