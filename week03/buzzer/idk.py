import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

# Define GPIO pins
passivebuzzer = 4

# Setup GPIO pin
GPIO.setup(passivebuzzer, GPIO.OUT)

# Notes and their corresponding frequencies (in Hz)
notes = {
    "C4": 261,
    "D4": 294,
    "E4": 329,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 493,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
    "G5": 784
}

# Harry Potter theme melody (simplified)
melody = [
    "E5", "E5", "F5", "G5", "G5", "F5", "E5", "D5", "C5", "D5", "E5",
    "E5", "E5", "E5", "D5", "D5", "E5", "E5", "E5", "F5", "F5", "E5",
    "D5", "C5", "D5", "E5", "E5", "F5", "G5", "G5", "F5", "E5", "D5",
    "C5", "D5", "E5"
]

# Duration for each note (in seconds)
note_duration = 0.4

# Function to play a single note
def play_note(note, duration):
    if note in notes:
        GPIO.output(passivebuzzer, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(passivebuzzer, GPIO.LOW)
        time.sleep(0.05)  # Brief pause between notes

# Play the melody
try:
    while True:
        for note in melody:
            play_note(note, note_duration)
except KeyboardInterrupt:
    print("Music stopped.")
finally:
    GPIO.cleanup()
