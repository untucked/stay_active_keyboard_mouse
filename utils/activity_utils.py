# utils/activity_utils.py
import time
import pyautogui
from pynput import mouse, keyboard
import datetime as dt
import pytz
from tkinter.ttk import Button
from functools import partial

# Local import
from utils.open_doc_write import write_a_long_text  # Import from open_doc_write.py

pyautogui.FAILSAFE = False

# Variables
inactivity_threshold = 1  # Default inactivity threshold in minutes
last_mouse_activity = time.time()
last_keyboard_activity = time.time()
tz = pytz.timezone('America/Los_Angeles')

# Styles
def configure_styles(style):
    style.configure("Green.TButton", background="lightgray")
    style.configure("Bold.TLabel", font=("calibri", 12, "bold"))
    style.configure("Green.TButton", font=('calibri', 10, 'bold', 'underline'), foreground='green')

# Mouse and Keyboard Activity Tracking
def move_mouse():
    pyautogui.move(10, 10, duration=1.0)
    pyautogui.move(-10, -10, duration=1.0)

# Callback function for mouse movement
def on_move_activity(x, y):
    global last_mouse_activity
    last_mouse_activity = time.time()

# Callback function for mouse click
def on_click_activity(x, y, button, pressed):
    global last_mouse_activity
    last_mouse_activity = time.time()

# Callback function for keyboard activity
def on_keyboard_activity(key):
    global last_keyboard_activity
    last_keyboard_activity = time.time()

def start_listening():
    mouse_listener = mouse.Listener(on_move=on_move_activity, on_click=on_click_activity)
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(on_press=on_keyboard_activity, on_release=on_keyboard_activity)
    keyboard_listener.start()
    return mouse_listener, keyboard_listener

# Helper Functions
def do_stuff_to_stay_awake():
    date_format = '%m/%d/%Y %H:%M:%S %Z'
    s = dt.datetime.now(tz=pytz.utc)
    s = s.astimezone(pytz.timezone('US/Pacific'))
    current_time_pretty = s.strftime(date_format)
    move_mouse()
    press_alt_tab()
    time.sleep(0.25)
    press_alt_tab()
    print('Pressed keys at %s' % (current_time_pretty))

def press_alt_tab():
    pyautogui.hotkey('alt', 'tab')

# Activity Prevention Logic
def check_inactivity(root, inactivity_threshold):
    global last_mouse_activity, last_keyboard_activity, is_active_override
    current_time = time.time()
    if not is_active_override:
        if (current_time - last_mouse_activity) >= (inactivity_threshold * 60) and \
           (current_time - last_keyboard_activity) >= (inactivity_threshold * 60):
            do_stuff_to_stay_awake()
    root.after(29 * 1000, check_inactivity, root, inactivity_threshold)
  
def start_activity_prevention(root, inactivity_entry, currently_running_label, currently_running_label2, start_button, stop_button):
    global inactivity_threshold, is_active_override
    try:
        inactivity_threshold = int(inactivity_entry.get())
    except ValueError:
        inactivity_threshold = 1
    if inactivity_threshold < 1:
        inactivity_threshold = 1

    check_inactivity(root, inactivity_threshold)
    currently_running_label.config(text="Currently Running", style="Bold.TLabel")
    currently_running_label2.config(text=f"Time Waiting: {inactivity_threshold} minutes")
    try:
        start_button.config(state="disabled")
        stop_button.config(state="normal")
    except AttributeError:
        pass

def stop_activity_prevention(currently_running_label, currently_running_label2, start_button, stop_button):
    currently_running_label.config(text="")
    currently_running_label2.config(text="")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

# Button Initialization
def initialize_start_button(root, inactivity_entry, currently_running_label, currently_running_label2, stop_button):
    return Button(
        root,
        text="Start",
        style="Green.TButton",
        command=partial(
            start_activity_prevention,
            root,
            inactivity_entry,
            currently_running_label,
            currently_running_label2,
            None,  # This will be dynamically replaced
            stop_button
        )
    )

def initialize_stop_button(root, currently_running_label, currently_running_label2, start_button):
    return Button(
        root,
        text="Stop",
        state="disabled",
        style="Green.TButton",
        command=partial(
            stop_activity_prevention,
            currently_running_label,
            currently_running_label2,
            start_button,
            None  # This will be dynamically replaced
        )
    )