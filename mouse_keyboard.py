import tkinter as tk
from tkinter.ttk import *
from functools import partial
from utils import activity_utils
import time

root = tk.Tk()

# Global variable
is_active_override = False  # Manual active status override

# Configure window
root.geometry("300x400")
root.title("Activity Preventer")

# Configure styles
style = Style()
activity_utils.configure_styles(style)

# Inactivity threshold entry
inactivity_label = Label(root, text="Inactivity Threshold (minutes):")
inactivity_label.pack()

inactivity_entry = Entry(root)
inactivity_entry.insert(0, "1")
inactivity_entry.pack()

# Status labels
currently_running_label = Label(root, text="", foreground="green")
currently_running_label.pack()

currently_running_label2 = Label(root, text="", foreground="purple")
currently_running_label2.pack()

# Initialize Start/Stop buttons
start_button = activity_utils.initialize_start_button(
    root, inactivity_entry, currently_running_label, currently_running_label2, None
)
stop_button = activity_utils.initialize_stop_button(
    root, currently_running_label, currently_running_label2, None
)

start_button.pack()
stop_button.pack()

# Override button
def toggle_active_status():
    global is_active_override
    is_active_override = not is_active_override
    if is_active_override:
        active_button.config(text="Meeting Mode: ON")
    else:
        active_button.config(text="Meeting Mode: OFF")

active_button = Button(root, text="Meeting Mode: OFF", command=toggle_active_status)
active_button.pack()

# Rebind start/stop with proper references
start_button.config(
    command=partial(
        activity_utils.start_activity_prevention,
        root,
        inactivity_entry,
        currently_running_label,
        currently_running_label2,
        start_button,
        stop_button
    )
)
stop_button.config(
    command=partial(
        activity_utils.stop_activity_prevention,
        currently_running_label,
        currently_running_label2,
        start_button,
        stop_button
    )
)

# Quit button
quit_button = Button(root, text="Quit", command=root.quit)
quit_button.pack()

# Start mouse and keyboard listening
activity_utils.start_listening()

# Updated inactivity checker: reference activity_utils variables directly
def check_inactivity_modified(root, inactivity_threshold):
    global is_active_override
    current_time = time.time()
    if not is_active_override:
        if (current_time - activity_utils.last_mouse_activity) >= (inactivity_threshold * 60) and \
           (current_time - activity_utils.last_keyboard_activity) >= (inactivity_threshold * 60):
            activity_utils.do_stuff_to_stay_awake()
    root.after(29 * 1000, check_inactivity_modified, root, inactivity_threshold)

# Replace activity_utils.check_inactivity with our GUI-aware version
activity_utils.check_inactivity = check_inactivity_modified

root.mainloop()
