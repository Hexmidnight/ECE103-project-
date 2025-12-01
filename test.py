
import cv2
import time
import RPi.GPIO as GPIO
import numpy as np

BEAM_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cv2.namedWindow("TEST Window", cv2.WINDOW_NORMAL)

def wait_for_beam_break_nonblocking():
    print("Waiting for beam break...")

    # FALLING edge wait
    while GPIO.input(BEAM_PIN) == 1:
        frame = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.putText(frame, "Waiting for FALLING", (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        cv2.imshow("TEST Window", frame)
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam broken!")

    # RISING edge wait
    print("Waiting for beam restore...")
    while GPIO.input(BEAM_PIN) == 0:
        frame = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.putText(frame, "Waiting for RISING", (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        cv2.imshow("TEST Window", frame)
        cv2.waitKey(1)
        time.sleep(0.01)

    print("Beam unbroken!")

try:
    while True:
        wait_for_beam_break_nonblocking()

finally:
    GPIO.cleanup()
    cv2.destroyAllWindows()
