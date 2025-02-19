import RPi.GPIO as GPIO
import time

button_blue = 20
button_yellow = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)



led_one = 9
led_two = 10
led_three = 11


leds_without_green = {
    9 : 1,
    11 : 4
}
GPIO.setup(10, GPIO.OUT)
for led in leds_without_green:
    GPIO.setup(led, GPIO.OUT)


previous_state_blue = GPIO.input(button_blue)
previous_state_yellow = GPIO.input(button_yellow)
GPIO.output(10, GPIO.HIGH)

blue_button_state_in_cycle = 0
led_flash_cycle = False


try:
    while True:

        #Blue button
        current_state_blue = GPIO.input(button_blue)
        if current_state_blue != previous_state_blue:
            if current_state_blue == GPIO.LOW:  #Button pressed
                GPIO.output(10, GPIO.LOW)
                for led, delay in leds_without_green.items():
                    GPIO.output(led, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(led, GPIO.LOW)

            if current_state_blue == GPIO.HIGH: #Button released
                pass
            previous_state_blue = current_state_blue



except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
