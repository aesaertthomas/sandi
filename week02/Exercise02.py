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

leds = [10, 9, 11]
for led in leds:
    GPIO.setup(led, GPIO.OUT)


previous_state_blue = GPIO.input(button_blue)
previous_state_yellow = GPIO.input(button_yellow)


blue_button_state_in_cycle = 0
led_flash_cycle = False

try:
    while True:

        #Blue button
        current_state_blue = GPIO.input(button_blue)
        if current_state_blue != previous_state_blue:
            if current_state_blue == GPIO.LOW:  #Button pressed

                if blue_button_state_in_cycle >= 1 and blue_button_state_in_cycle < 3:
                    GPIO.output(leds[blue_button_state_in_cycle-1], GPIO.LOW) #Turnoff old leds
                    GPIO.output(leds[blue_button_state_in_cycle], GPIO.HIGH) #Turnon new leds
                    blue_button_state_in_cycle += 1

                elif blue_button_state_in_cycle == 3:
                    GPIO.output(leds[blue_button_state_in_cycle-1], GPIO.LOW) #Turnoff old leds
                    blue_button_state_in_cycle = 0

                else:
                    GPIO.output(leds[blue_button_state_in_cycle], GPIO.HIGH)
                    blue_button_state_in_cycle += 1
            if current_state_blue == GPIO.HIGH: #Button released
                pass
            previous_state_blue = current_state_blue



        #Yellow button
        current_state_yellow = GPIO.input(button_yellow)
        if current_state_yellow != previous_state_yellow:
            if current_state_yellow == GPIO.LOW:  #Button pressed
                led_flash_cycle = True #XOR (more effiecnet eh)

            if current_state_yellow == GPIO.HIGH: #Button released
                led_flash_cycle = False
            previous_state_yellow = current_state_yellow
        time.sleep(0.01)

        if led_flash_cycle:
            for led in leds:
                GPIO.output(led, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(led, GPIO.LOW)






except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
