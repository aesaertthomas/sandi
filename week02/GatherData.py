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

df = pd.DataFrame(columns=["button","timestamp","state"])

try:
    while True:

        #Blue button
        current_state_blue = GPIO.input(button_blue)
        if current_state_blue == GPIO.LOW:  #Button pressed
            df.loc[len(df)] = ['blue_button',datetime.now(),'1']


        if current_state_blue == GPIO.HIGH: #Button released
            df.loc[len(df)] = ['blue_button',datetime.now(),'0']

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCtrl+C detected! Exiting...")
finally:

    path = "gather-sensor-data/"

    entries = os.listdir(path)

    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create the new directory path
    new_path_dir = f"{path}/run-{len(directories)}_{timestamp_str}/"
    os.mkdir(new_path_dir)

    # Convert state to integer
    df['state'] = df['state'].astype(int)

    # Create and save plot
    if not df.empty:
        plt.figure(figsize=(12, 6))
        sns.set_theme(style="whitegrid")

        # Create line plot
        ax = sns.lineplot(
            data=df,
            x='timestamp',
            y='state',
            hue='button',
            estimator=None  # Show raw data points
        )

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)
        plt.title('Button State Over Time')
        plt.xlabel('Time')
        plt.ylabel('State (0=Released, 1=Pressed)')
        plt.tight_layout()
        plt.savefig(f"{new_path_dir}/button-state-over-time.png", dpi=300)
        plt.close()


    # Save data and clean up
    df.to_csv(f"{new_path_dir}/{datetime.now()}.csv", index=False)
    GPIO.cleanup()
    print("GPIO cleaned up. Goodbye!")
