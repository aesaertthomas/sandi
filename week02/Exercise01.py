import RPi.GPIO as GPIO
import time

button = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_state = GPIO.input(button)

try:
    while True:
        current_state = GPIO.input(button)
        if current_state != previous_state:
            if current_state == GPIO.LOW:  #Button pressed
                print("Button pressed")
            if current_state == GPIO.HIGH: #Button released
                print("Button released")
            previous_state = current_state
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
