import RPi.GPIO as GPIO
import time

def blink (sleep):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24,GPIO.OUT)

        for i in range(20):
                GPIO.output(24,GPIO.HIGH)
                time.sleep(sleep)
                GPIO.output(24,GPIO.LOW)
                time.sleep(sleep)
        GPIO.cleanup()

if __name__=="__main__":
        time.sleep(60)
        blink(0.5)
