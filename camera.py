import picamera
import time

camera = picamera.PiCamera()


timestr = time.strftime("%Y%m%d-%H%M%S")
camera.capture('/pictures/test.jpeg')
