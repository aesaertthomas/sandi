import time
from datetime import datetime
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

button = 20
buzzer = 12
passivebuzzer = 4
led = 17

GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(passivebuzzer, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

oldvalue = GPIO.input(button)
started_time = None
ledstate = False

def lock_on_sound():
    pwm = GPIO.PWM(passivebuzzer, 800)  # Searching tone
    pwm.start(20)

    # Simulate scanning beeps
    for _ in range(5):
        pwm.ChangeFrequency(800)
        time.sleep(0.2)
        pwm.stop()
        time.sleep(0.1)
        pwm.start(20)

    # Lock-on confirmed, continuous high-pitch tone
    pwm.ChangeFrequency(2000)
    pwm.ChangeDutyCycle(40)
    time.sleep(1.5)

    pwm.stop()

try:
    while True:
        buttonvalue = GPIO.input(button)

        if buttonvalue != oldvalue:
            if buttonvalue == 0:
                started_time = datetime.now()
                ledstate = not ledstate
                GPIO.output(led, ledstate)
                lock_on_sound()
            oldvalue = buttonvalue
            time.sleep(0.01)

        if started_time is not None:
            difference = (datetime.now() - started_time).total_seconds()
            if difference >= 3:
                GPIO.output(led, GPIO.LOW)
                started_time = None

except KeyboardInterrupt:
    print("yoeyoeeeeeee")
finally:
    GPIO.cleanup()
