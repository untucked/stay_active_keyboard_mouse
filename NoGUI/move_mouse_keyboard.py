import pyautogui
import time
from pynput import mouse, keyboard

# Set the inactivity duration threshold (in seconds)
inactivity_threshold = 60 * 2  # 1 minutes

# Variables to track the last activity times
last_mouse_activity = time.time()
last_keyboard_activity = time.time()

# Move the mouse cursor a little bit
def move_mouse():
    # You can adjust the values to control the mouse movement distance
    pyautogui.move(10, 10, duration=0.25)
    pyautogui.move(-10, -10, duration=0.25)

# Callback function for mouse activity
def on_mouse_activity(x, y): # , button, pressed):
    global last_mouse_activity
    last_mouse_activity = time.time()

# Callback function for keyboard activity
def on_keyboard_activity(key):
    global last_keyboard_activity
    last_keyboard_activity = time.time()

# Type something on the keyboard
def press_alt_tab():
    pyautogui.hotkey('alt', 'tab')  

# Set up mouse listener
mouse_listener = mouse.Listener(on_move=on_mouse_activity)
mouse_listener.start()

# Set up keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_keyboard_activity)
keyboard_listener.start()

while True:
    current_time = time.time()

    # Check for mouse inactivity
    if (current_time - last_mouse_activity) >= inactivity_threshold:
        print('mouse inactive')
        move_mouse()
        press_alt_tab()
        last_mouse_activity = current_time
    else:
        continue
    # Check for keyboard inactivity
    if (current_time - last_keyboard_activity) >= inactivity_threshold:
        print('keyboard inactive')
        move_mouse()
        press_alt_tab()
        last_keyboard_activity = current_time

    time.sleep(59)  # Check every 30 seconds
