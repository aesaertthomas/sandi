import time
import threading #using multithreading for both running led action, and button detection simultaniously
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

#Setting up pins
upper_button = 20
lower_button = 21
right_button = 16
left_button = 26
led = 17

led_state = "off"
led_thread = None #will be used to hold the thread

stop_flag = threading.Event() #Apparantly this cn be used for stoppign led thread

#Setting pins up as in/output
GPIO.setup(upper_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #I prefer PUD down instead of UP, cause 1 pressed makes more sense to me, than 0 when pressed
GPIO.setup(lower_button,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)


#defining all possible led actions, blink fast/slow, stop, on
def led_static():
    while not stop_flag.is_set():
        GPIO.output(led, GPIO.HIGH)
