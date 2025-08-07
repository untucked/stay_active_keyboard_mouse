import os
import platform
import pyautogui
import time
from pywinauto.application import Application

# Determine the path to Notepad depending on the OS
if platform.system() == "Windows":
    notepad_path = "C:\\Windows\\System32\\notepad.exe"
else:
    raise EnvironmentError("This script is only supported on Windows.")


def read_doc(file_loc='something_to_read.txt'):
    """
    Reads a text file and splits it into words.
    """
    try:
        with open(file_loc, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            words = content.split()
        return words
    except FileNotFoundError:
        print(f"Error: File '{file_loc}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file '{file_loc}': {e}")
        return []


def open_notepad():
    """
    Opens Notepad using pywinauto.
    """
    try:
        return Application().start(notepad_path)
    except Exception as e:
        print(f"Error: Failed to open Notepad. {e}")
        return None


def close_notepad(app):
    """
    Closes Notepad gracefully.
    """
    try:
        app.UntitledNotepad.menu_select("File->Exit")
    except Exception as e:
        print(f"Error: Failed to close Notepad gracefully. {e}")
        app.kill()


def open_notepad_and_write(words):
    """
    Opens Notepad and writes text from a list of words.
    """
    app = open_notepad()
    if not app:
        return 0

    # Wait for Notepad to be ready
    time.sleep(2)

    try:
        for idx, word in enumerate(words):
            pyautogui.write(word)  # Use write instead of typewrite
            pyautogui.write(' ')  # Add a space between words
            if (idx + 1) % 10 == 0:
                pyautogui.press('enter')  # Press Enter after every 10 words
        time.sleep(1)  # Decreased final delay
    except Exception as e:
        print(f"Error during typing: {e}")
        close_notepad(app)
        return 0

    close_notepad(app)
    return 1


def open_notepad_and_write_check(words):
    """
    Opens Notepad and writes text with user presence check using mouse position.
    """
    initial_mouse_position = pyautogui.position()
    app = open_notepad()
    if not app:
        return 0

    # Wait for Notepad to be ready
    time.sleep(2)

    try:
        for idx, word in enumerate(words):
            # Check mouse position at specified intervals
            if idx % 10 == 0:
                current_mouse_position = pyautogui.position()
                if current_mouse_position != initial_mouse_position:
                    print("Mouse moved. Closing Notepad.")
                    close_notepad(app)
                    return 0

            pyautogui.write(word)
            pyautogui.write(' ')  # Add a space between words
            if (idx + 1) % 10 == 0:
                pyautogui.press('enter')
        time.sleep(1)  # Decreased final delay
    except Exception as e:
        print(f"Error during typing: {e}")
        close_notepad(app)
        return 0

    close_notepad(app)
    return 1


def write_a_long_text(file_loc='something_to_read.txt'):
    """
    Main function to read a document and write its content in Notepad.
    """
    doc_words = read_doc(file_loc)
    if not doc_words:
        return 0
    return open_notepad_and_write_check(doc_words)


if __name__ == "__main__":
    file_path = 'something_to_read.txt'  # Replace with your file path
    result = write_a_long_text(file_path)
    if result:
        print("Text written successfully.")
    else:
        print("Failed to write text.")
