import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time
import threading
import pygame
import os
from datetime import datetime, timedelta


def main():
    global root
    root = tk.Tk()
    root.title("Alarm Project")

    # Input for time (hours, minutes)
    hour_var = tk.StringVar()
    minute_var = tk.StringVar()

    # Timer input labels and entry fields
    tk.Label(root, text="Hours:").pack(pady=5)
    tk.Entry(root, textvariable=hour_var).pack(pady=30)

    tk.Label(root, text="Minutes:").pack(pady=5)
    tk.Entry(root, textvariable=minute_var).pack(pady=30)

    # AM/PM selection
    am_pm_var = tk.StringVar(value="AM")
    tk.Radiobutton(root, text="AM", variable=am_pm_var, value="AM").pack(pady=10)
    tk.Radiobutton(root, text="PM", variable=am_pm_var, value="PM").pack(pady=30)

    # Choose alarm sound button
    tk.Button(root, text="Choose Alarm Sound", command=lambda: choose_alarm_sound()).pack(pady=30)

    # Start button
    tk.Button(root, text="Start", command=lambda: start_timer(hour_var, minute_var, am_pm_var)).pack(pady=30)

    root.mainloop()


def choose_alarm_sound():
    global alarm_sound
    # File dialog to choose sound file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        alarm_sound = file_path


def start_timer(hours, minutes, am_pm):
    try:
        hr = int(hours.get())
        min = int(minutes.get())
        if am_pm.get() == "PM" and hr != 12:
            hr += 12
        elif am_pm.get() == "AM" and hr == 12:
            hr = 0

        alarm_time = datetime.now().replace(hour=hr, minute=min, second=0, microsecond=0)
        if alarm_time < datetime.now():
            alarm_time += timedelta(days=1)  # Set for the next day if time has already passed

        # Open new window to display remaining time
        open_timer_window(alarm_time)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid time")


def open_timer_window(alarm_time):
    global timer_window, stop_button
    timer_window = tk.Toplevel(root)
    timer_window.title("Timer Countdown")

    # Label to display remaining time
    remaining_time_label = tk.Label(timer_window, text="", font=("Helvetica", 24))
    remaining_time_label.pack(pady=20)

    # Stop button
    stop_button = tk.Button(timer_window, text="Stop", command=lambda: stop_timer_and_close(remaining_time_label))
    stop_button.pack(pady=20)

    # Update countdown every second
    def update_time():
        remaining = alarm_time - datetime.now()
        if remaining.total_seconds() <= 0:
            play_alarm()
            remaining_time_label.config(text="Time's up!")
            return
        remaining_time_label.config(text=str(remaining).split('.')[0])  # Display as HH:MM:SS
        timer_window.after(1000, update_time)

    update_time()


def play_alarm():
    if alarm_sound:
        pygame.mixer.init()
        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play()


def stop_timer():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def stop_timer_and_close(label):
    stop_timer()
    timer_window.destroy()  # Close the countdown window


if __name__ == "__main__":
    main()
