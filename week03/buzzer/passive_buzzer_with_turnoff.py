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

def dying_sound():
    pwm = GPIO.PWM(passivebuzzer, 1000)
    pwm.start(30)
    for freq in range(1000, 400, -200):
        pwm.ChangeFrequency(freq)
        time.sleep(0.1)
    pwm.ChangeDutyCycle(0)
    pwm.stop()


try:
    while True:
        buttonvalue = GPIO.input(button)

        if buttonvalue != oldvalue:
            if buttonvalue == 0:
                started_time = datetime.now()
                ledstate = not ledstate
                GPIO.output(led, ledstate)
                for _ in range(200):
                    GPIO.output(passivebuzzer, GPIO.HIGH)
                    time.sleep(0.001)
                    GPIO.output(passivebuzzer, GPIO.LOW)
                    time.sleep(0.001)
            oldvalue = buttonvalue
            time.sleep(0.01)

        if started_time is not None:
            difference = (datetime.now() - started_time).total_seconds()
            if difference >= 3:
                GPIO.output(led, GPIO.LOW)
                dying_sound()
                started_time = None

except KeyboardInterrupt:
    print("yoeyoeeeeeee")
finally:
    GPIO.cleanup()
