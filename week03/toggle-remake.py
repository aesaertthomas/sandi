import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM) #So you can use GPIO numbers instead of phyiscal


button = 20
led = 17
buzzer = 12

#States
led_state = GPIO.LOW
button_previous_state = GPIO.LOW


GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #I personally like PUD_DOWN more than UP, because 0 = off and 1 = on, not opposite ways 😅
GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(led, led_state)

def toggle_led():
    global led_state
    led_state = not led_state
    GPIO.output(led, led_state)

    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzer, GPIO.LOW)

    print(f"LED toggled to: {led_state}")
try:
    while True:
        button_current_state = GPIO.input(button)

        if button_current_state == GPIO.HIGH and button_previous_state == GPIO.LOW: #Check if change in button state
            toggle_led()
            time.sleep(0.1)

        button_previous_state = button_current_state
        time.sleep(0.05)


except KeyboardInterrupt:
    print("yoeyoe")

finally:
    GPIO.cleanup()
