# utils/open_doc_write.py
import os
import platform
import time
from typing import List, Optional

from pywinauto.application import Application
from pywinauto import timings

# NOTE: This module now routes all keystrokes DIRECTLY to Notepad's Edit control
# via pywinauto (edit.type_keys), so it does NOT depend on global focus.
# pyautogui is no longer used for typing.

# -------- Platform Gate --------
if platform.system() != "Windows":
    raise EnvironmentError("This script only supports Windows (uses Notepad + pywinauto).")

NOTEPAD_EXE = r"C:\Windows\System32\notepad.exe"


# -------- File IO --------
def read_doc(file_loc: str = "something_to_read.txt") -> List[str]:
    """Reads a text file and splits it into words."""
    try:
        file_loc = os.path.abspath(file_loc)
        with open(file_loc, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return content.split()
    except FileNotFoundError:
        print(f"[open_doc_write] File not found: {file_loc}")
        return []
    except Exception as e:
        print(f"[open_doc_write] Error reading {file_loc}: {e}")
        return []


# -------- Notepad Helpers --------
def open_notepad() -> Optional[Application]:
    """Launch Notepad and return a pywinauto Application handle."""
    try:
        app = Application(backend="uia").start(NOTEPAD_EXE)
        return app
    except Exception as e:
        print(f"[open_doc_write] Failed to start Notepad: {e}")
        return None


def _get_notepad_edit(app: Application):
    """Return the Notepad main window and Edit control."""
    try:
        # Wait for top window to appear
        dlg = app.window(title_re=".* - Notepad|.*Notepad")
        dlg.wait("exists enabled visible ready", timeout=10)
        # Get the edit box (the text area)
        edit = dlg.child_window(class_name="Edit")
        edit.wait("exists enabled visible ready", timeout=10)
        return dlg, edit
    except Exception as e:
        print(f"[open_doc_write] Could not get Notepad Edit control: {e}")
        return None, None


def close_notepad(app: Application):
    """Close Notepad, auto-dismiss 'Save' prompt if it appears."""
    try:
        dlg = app.window(title_re=".* - Notepad|.*Notepad")
        # Try menu close
        try:
            dlg.menu_select("File->Exit")
        except Exception:
            # Fallback: close button
            dlg.close()
        # Handle potential Save prompt
        try:
            prompt = app.window(class_name="#32770")  # Generic dialog class
            # Wait briefly to see if it pops
            timings.wait_until_passes(2, 0.2, lambda: prompt.wait("exists ready"))
            # Try common button labels
            for btn_text in ["Don't Save", "&Dont Save", "&Don't Save", "Don’t Save", "No", "&No", "Cancel"]:
                if prompt.child_window(title=btn_text).exists(timeout=0.5):
                    # Prefer "Don't Save"/"No" over "Cancel"
                    if "Cancel" in btn_text:
                        continue
                    prompt.child_window(title=btn_text).click_input()
                    break
        except Exception:
            pass
    except Exception as e:
        print(f"[open_doc_write] Failed to close Notepad gracefully: {e}")
        try:
            app.kill()
        except Exception:
            pass


# -------- Typing (Focus-Independent) --------
def _type_words_into_edit(edit, words: List[str], words_per_line: int = 10, pause: float = 0.02):
    """
    Types text into the Notepad Edit control using type_keys (with_spaces=True).
    This targets the control directly; it does not require the window to be foreground.
    """
    count_in_line = 0
    for word in words:
        # Send the word + trailing space
        edit.type_keys(word, with_spaces=True, pause=pause)
        edit.type_keys(" ", with_spaces=True, pause=pause)
        count_in_line += 1
        if count_in_line >= words_per_line:
            edit.type_keys("{ENTER}", pause=pause)
            count_in_line = 0


def open_notepad_and_write(words: List[str]) -> int:
    """Open Notepad and write the provided words. Returns 1 on success, 0 on failure."""
    app = open_notepad()
    if not app:
        return 0

    # Allow Notepad to initialize
    time.sleep(0.8)
    dlg, edit = _get_notepad_edit(app)
    if edit is None:
        close_notepad(app)
        return 0

    try:
        _type_words_into_edit(edit, words)
        time.sleep(0.3)
    except Exception as e:
        print(f"[open_doc_write] Error while typing: {e}")
        close_notepad(app)
        return 0

    close_notepad(app)
    return 1


def open_notepad_and_write_check(words: List[str]) -> int:
    """
    Same as open_notepad_and_write but aborts if user moves the mouse.
    Focus-independent typing via pywinauto is still used.
    """
    # Snapshot initial pointer position using pywinauto (fallback to no-check if not available)
    try:
        from pywinauto import mouse as pwmouse
        initial_pos = pwmouse.get_cursor_pos()
        get_pos = pwmouse.get_cursor_pos
    except Exception:
        initial_pos = None
        get_pos = None

    app = open_notepad()
    if not app:
        return 0

    time.sleep(0.8)
    dlg, edit = _get_notepad_edit(app)
    if edit is None:
        close_notepad(app)
        return 0

    try:
        count = 0
        for word in words:
            # Every 10 words, check if mouse moved
            if initial_pos and get_pos and (count % 10 == 0):
                if get_pos() != initial_pos:
                    print("[open_doc_write] Mouse moved; aborting and closing Notepad.")
                    close_notepad(app)
                    return 0
            edit.type_keys(word, with_spaces=True, pause=0.02)
            edit.type_keys(" ", with_spaces=True, pause=0.02)
            count += 1
            if count % 10 == 0:
                edit.type_keys("{ENTER}", pause=0.02)
        time.sleep(0.3)
    except Exception as e:
        print(f"[open_doc_write] Error while typing with check: {e}")
        close_notepad(app)
        return 0

    close_notepad(app)
    return 1


# -------- Public Entry --------
def write_a_long_text(file_loc: str = "something_to_read.txt") -> int:
    """Read a file and type its contents into Notepad (focus-independent)."""
    words = read_doc(file_loc)
    if not words:
        return 0
    return open_notepad_and_write_check(words)


if __name__ == "__main__":
    path = "something_to_read.txt"
    result = write_a_long_text(path)
    print("Text written successfully." if result else "Failed to write text.")
