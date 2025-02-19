import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


leds = {
    10 : 5,
    9 : 1,
    11 : 4
}
for led in leds:
    GPIO.setup(led, GPIO.OUT)
try:
    while True:
        for led, delay in leds.items():
            GPIO.output(led, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(led, GPIO.LOW)


except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
