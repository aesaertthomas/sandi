import time
import threading
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

# Button pins
upper_button = 20
lower_button = 21
left_button = 26
right_button = 16
led = 17

# LED state management
led_state = "off"  # Can be "off", "on", "blink_slow", or "blink_fast"
blink_thread = None  # To hold the current blinking thread

# Stop flag
stop_flag = threading.Event()  # This is used to stop the blinking threads

# Setup GPIO pins
GPIO.setup(upper_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(lower_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

# Function to turn LED on/off based on state
def set_led(state):
    global led_state, blink_thread, stop_flag
    led_state = state
    stop_flag.clear()  # Clear the stop flag when setting a new LED state

    if state == "off":
        GPIO.output(led, GPIO.LOW)
        stop_flag.set()  # Stop blinking if the LED is turned off
        if blink_thread:
            blink_thread.join()  # Wait for the blinking thread to finish
        blink_thread = None  # Clear the blinking thread reference

    elif state == "on":
        GPIO.output(led, GPIO.HIGH)
        stop_flag.set()  # Stop blinking if the LED is turned on
        if blink_thread:
            blink_thread.join()  # Wait for the blinking thread to finish
        blink_thread = None  # Clear the blinking thread reference

# Slow blink function
def blink_slow():
    while not stop_flag.is_set():  # Check the stop flag
        GPIO.output(led, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led, GPIO.LOW)
        time.sleep(1)

# Fast blink function
def blink_fast():
    while not stop_flag.is_set():  # Check the stop flag
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.2)

# Function to stop the currently running blink thread
def stop_blink_thread():
    global blink_thread
    if blink_thread:  # If there is a running blink thread
        stop_flag.set()  # Set the stop flag to stop the thread immediately
        blink_thread.join()  # Wait for the thread to finish and clean up
        blink_thread = None  # Clear the thread reference

# Functions for button press actions
def button_pressed_upper(channel):
    set_led('off')
    set_led("on")

    #Logging
    print("Upper button pressed: LED On")

def button_pressed_lower(channel):
    set_led("off")

    #Logging
    print("Lower button pressed: LED Off")


def button_pressed_left(channel):
    set_led('off')
    set_led("blink_slow")
    global blink_thread
    stop_blink_thread()  # Stop any currently running blink thread first
    blink_thread = threading.Thread(target=blink_slow)
    blink_thread.start()

    #Logging
    print("Left button pressed: LED Blink Slow")


def button_pressed_right(channel):
    set_led('off')
    set_led("blink_fast")
    global blink_thread
    stop_blink_thread()  # Stop any currently running blink thread first
    blink_thread = threading.Thread(target=blink_fast)
    blink_thread.start()

    #Logging
    print("Right button pressed: LED Blink Fast")


# Add event detection for buttons
GPIO.add_event_detect(upper_button, GPIO.RISING, callback=button_pressed_upper, bouncetime=300)
GPIO.add_event_detect(lower_button, GPIO.RISING, callback=button_pressed_lower, bouncetime=300)
GPIO.add_event_detect(left_button, GPIO.RISING, callback=button_pressed_left, bouncetime=300)
GPIO.add_event_detect(right_button, GPIO.RISING, callback=button_pressed_right, bouncetime=300)

# Run the program indefinitely
try:
    while True:
        time.sleep(0.05)  # Main loop does nothing, just keeps program running

except KeyboardInterrupt:
    print("Program stopped by user.")
    GPIO.cleanup()  # Clean up GPIO on exit
    stop_blink_thread()  # Make sure the thread is stopped when exiting
