# mouse_keyboard_wEssay.py
import tkinter as tk
from tkinter.ttk import *
from functools import partial

from utils import activity_utils_essay

root = tk.Tk()

# Configure window
root.geometry("300x350")
root.title("Activity Preventer")

file_path = "./utils/something_to_read.txt"  # Replace with your file's path


# Configure styles
style = Style()
activity_utils_essay.configure_styles(style)

# Add inactivity threshold entry
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

# First Step: Initialize the buttons without references to each other
start_button = activity_utils_essay.initialize_start_button(
    root, inactivity_entry, currently_running_label, currently_running_label2, None  # Placeholder
)
stop_button = activity_utils_essay.initialize_stop_button(
    root, currently_running_label, currently_running_label2, None  # Placeholder
)
# Pack buttons for the first time
start_button.pack()
stop_button.pack()
# Second Step: Reinitialize the buttons with proper references to each other
start_button.config(
    command=partial(
        activity_utils_essay.start_activity_prevention,
        root,
        inactivity_entry,
        currently_running_label,
        currently_running_label2,
        start_button,
        stop_button,
        file_path
    )
)
stop_button.config(
    command=partial(
        activity_utils_essay.stop_activity_prevention,
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
activity_utils_essay.start_listening()

# Main loop
root.mainloop()
