import RPi.GPIO as GPIO
import time
import os

import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns

button_blue = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = pd.DataFrame(columns=["button", "time_pressed"])

previous_state = GPIO.input(button_blue)

def plot_button_press_duration(df : pd.DataFrame):
    #I mean I am not going to lie, but ChatGPT helped me with this piece, I was almost ready to pull my hair out from converting the formats 😅
    def time_to_seconds(time_str):
        time_part = time_str.split(' ')[1]  # Get HH:MM:SS part
        h, m, s = map(int, time_part.split(':'))
        return h * 3600 + m * 60 + s

    #Apply the conversion function to 'time_pressed' column
    df['time_pressed_seconds'] = df['time_pressed'].apply(time_to_seconds)

    #Plotting
    plt.figure(figsize=(12, 6))
    sns.histplot(df['time_pressed_seconds'], bins=10, kde=False, color='blue')
    plt.title('Button Press Duration (in seconds)')
    plt.xlabel('Time Pressed (seconds)')
    plt.ylabel('Frequency')
    plt.savefig("figure.png")

    print("YUPPPPP saved the figure to a file. (its at figure.png)")


try:
    while True:
        current_state_blue = GPIO.input(button_blue)

        if previous_state != current_state_blue:
            if current_state_blue == GPIO.LOW:  #Button pressed
                start_time = datetime.now()
                print("pressed")
            if current_state_blue == GPIO.HIGH:  #Button released
                print("released")
                button_press_duration = (datetime.now() - start_time).total_seconds()  #Convert timedelta to seconds

                #Convert the duration (in seconds) to HH:MM:SS format
                hours, remainder = divmod(button_press_duration, 3600)
                minutes, seconds = divmod(remainder, 60)

                #Format as "YYYY-MM-DD HH:MM:SS" with the date set to "00-00-00"
                time_format = f"00-00-00 {int(hours):02}:{int(minutes):02}:{int(seconds):02}"

                df.loc[len(df)] = ["blue_button", time_format]

        previous_state = current_state_blue
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCtrl + C detected! Exiting...")

finally:
    # Saving data to .csv
    print(df.head())
    df.to_csv("data.csv", index=False)

    plot_button_press_duration(df=df)

    # Safely closing off pins
    GPIO.cleanup()
    print("GPIO cleaned up. Goodby")


#The datetime formatting was helped by ChatGPT, because It was making me more confused than a penguin walking in a sauna
