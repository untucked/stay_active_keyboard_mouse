import tkinter as tk
from pynput import mouse, keyboard
import time
import pyautogui
from tkinter.ttk import *
import pytz
import datetime as dt
pyautogui.FAILSAFE = False

root = tk.Tk()
# Create style Object
style = Style() 

# Set Geometry(widthxheight)
root.geometry('300x300')
root.title("Activity Preventer")

# Add a custom style for the button
style.configure("Green.TButton", 
                background="lightgray")
style.configure("Bold.TLabel", 
                font=("calibri", 12, "bold"))
style.configure("Green.TButton", 
                font = ('calibri', 10, 'bold', 'underline'),
                foreground = 'green')
# Set the inactivity duration threshold (in seconds)
inactivity_threshold = 1  # 1 minutes

# Variables to track the last activity times
last_mouse_activity = time.time()
last_keyboard_activity = time.time()
tz = pytz.timezone('America/Los_Angeles')
# Move the mouse cursor a little bit
def move_mouse():
    # You can adjust the values to control the mouse movement distance
    pyautogui.move(10, 10, duration=1.0)
    pyautogui.move(-10, -10, duration=1.0)

# Callback function for mouse movement
def on_mouse_activity(x, y):
    global last_mouse_activity
    last_mouse_activity = time.time()

def on_keyboard_activity(key):
    global last_keyboard_activity
    last_keyboard_activity = time.time()

# Type something on the keyboard
def press_alt_tab():
    pyautogui.hotkey('alt', 'tab')  
def press_alt_ctrl():
    pyautogui.hotkey('alt', 'ctrl')

# Set up mouse listener for mouse movement only
mouse_listener = mouse.Listener(on_move=on_mouse_activity)
mouse_listener.start()
# Set up keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_keyboard_activity)
keyboard_listener.start()

def do_stuff_to_stay_awake( ):
    date_format='%m/%d/%Y %H:%M:%S %Z'
    s = dt.datetime.now(tz=pytz.utc)
    s = s.astimezone(pytz.timezone('US/Pacific'))
    current_time_pretty = s.strftime(date_format)
    move_mouse()
    press_alt_tab()
    time.sleep(0.25)
    press_alt_tab()
    print('Pressed keys at %s'%(current_time_pretty))
    log_time_recent_inactivity.config(text=f"inactive: {current_time_pretty}")

def check_inactivity():
    global last_mouse_activity  # Make sure to use the global variable
    current_time = time.time()
    # Check for mouse inactivity
    Q_mouse_not_move = (current_time - last_mouse_activity) >= (inactivity_threshold*60)
    Q_keyboard_not_press = (current_time - last_keyboard_activity) >= (inactivity_threshold*60)
    if Q_mouse_not_move and Q_keyboard_not_press:
        do_stuff_to_stay_awake( )

    root.after(29*1000, check_inactivity)  # Check every 29 seconds
        
# Function to start the activity prevention
def start_activity_prevention():
    global last_mouse_activity, inactivity_threshold   
    try:
        inactivity_threshold = int(inactivity_entry.get()) 
    except:
        inactivity_threshold=1
    if inactivity_threshold < 1:
        inactivity_threshold=1
    # last_mouse_activity = time.time()
    
    check_inactivity()
    currently_running_label.config( text="Currently Running", style="Bold.TLabel")
    currently_running_label2.config( text="Time Waiting: %d"%(inactivity_threshold))
    start_button.config(state="disabled")  # Disable the "Start" button
    stop_button.config(state="normal")     # Enable the "Stop" button

# Function to stop the activity prevention
def stop_activity_prevention():
    currently_running_label.config(text="")  # Clear the label text
    currently_running_label2.config(text="")  # Clear the label text
    start_button.config(state="normal")      # Enable the "Start" button
    stop_button.config(state="disabled")     # Disable the "Stop" button
    root.after(29*1000, stop_activity_prevention)  # Check every 29 seconds


# Function to change the button style when pressed
def highlight_button(event):    
    currently_running_label.config( text="Currently Running", style="Bold.TLabel")
    currently_running_label2.config( text="Time Waiting: %d"%(inactivity_threshold))


# Create a label and Entry widget for entering the inactivity threshold
inactivity_label = Label(root, text="Inactivity Threshold (minutes):")
inactivity_label.pack()
inactivity_entry = Entry(root)
inactivity_entry.pack()
# Set the default value in the Entry widget
inactivity_entry.insert(1, str(inactivity_threshold))

# Create and configure the Start button
start_button = Button(root, 
                      text="Start", 
                      style="Green.TButton", 
                      command=start_activity_prevention)
start_button.pack()

# Create a label for displaying "Currently Running" text
currently_running_label = Label(root, text="", foreground="green")
currently_running_label.pack()
currently_running_label2 = Label(root, text="", foreground="purple")
currently_running_label2.pack()

# Create and configure the Stop button
stop_button = Button(root, 
                     text="Stop", 
                     state="disabled", 
                     command=stop_activity_prevention)
stop_button.pack()

# Bind the button press event to the highlight_button function
start_button.bind("<ButtonPress-1>", highlight_button)

# Create and configure the Quit button
quit_button = Button(root, text="Quit", command=root.quit)
quit_button.pack()

# Create a label for displaying "Currently Running" text
log_time_recent_inactivity = Label(root, text="", foreground="black")
log_time_recent_inactivity.pack()

# Run the main loop
root.mainloop()