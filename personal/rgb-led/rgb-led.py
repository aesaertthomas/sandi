import RPi.GPIO as GPIO
import time
import random

# Set up GPIO pins
red = 5
green = 6
blue = 13

GPIO.setmode(GPIO.BCM)


GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# Set up PWM for each color
red_pwm = GPIO.PWM(red, 1000)  # Frequency is set to 1 kHz
green_pwm = GPIO.PWM(green, 1000)
blue_pwm = GPIO.PWM(blue, 1000)

# Start PWM with 0 duty cycle (LED off initially)
red_pwm.start(0) #PWM = pulse width modulation?
green_pwm.start(0)
blue_pwm.start(0)

def setColor(r_val, g_val, b_val):
    red_pwm.ChangeDutyCycle(r_val)
    green_pwm.ChangeDutyCycle(g_val)
    blue_pwm.ChangeDutyCycle(b_val)

try:
    # previous_r = -1 #initial value
    while True:
    #     if previous_r == 100:
    #         current_r = 0
    #     else:
    #         current_r = previous_r + 1

        # Get a random value between 0 and 100
        setColor(100, 0, 0)  # Set random values as duty cycle for PWM
        time.sleep(2)
        setColor(0, 100, 0)  # Set random values as duty cycle for PWM
        time.sleep(2)
        setColor(0, 0, 100)  # Set random values as duty cycle for PWM
        time.sleep(2)
        # previous_r = current_r

except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:
    #Stopping all colors channels

    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
