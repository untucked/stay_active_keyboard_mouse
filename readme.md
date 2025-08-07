# Stay Active (Keyboard & Mouse)

A toolkit of small Python utilities and GUIs to prevent your system from going idle.  
Includes both **GUI-based** and **No-GUI** scripts for mouse jiggle, key presses, and even automated "essay" typing.

> ⚠️ Use responsibly. You are solely responsible for complying with all applicable workplace, legal, and platform rules.

---

## 📦 Features

### GUI Applications
- **`mouse_keyboard.py`** – Tkinter GUI to prevent idle by moving the mouse or pressing keys after a period of inactivity.
- **`mouse_keyboard_wEssay.py`** – Like above, but after a configurable number of idle events, automatically opens Notepad and types text from a file.

Features include:
- Global mouse + keyboard activity detection (via `pynput`)
- Inactivity threshold control
- "Meeting Mode" toggle to disable actions temporarily
- Optional "essay" mode to type content into Notepad after repeated inactivity

### No-GUI Scripts
- **`NoGUI/move_mouse_noSleep.py`** – Lightweight background script that jiggles the mouse and optionally presses Alt+Tab.
    - Tracks both mouse and keyboard activity to skip actions when you're active.
    - Interval, jiggle distance, idle grace period, and Alt+Tab are configurable via CLI arguments.

### Essay Typing Engine
- **`utils/open_doc_write.py`** – Opens Notepad (Windows only) and types the contents of a text file directly into its Edit control (no focus needed).
    - Closes Notepad automatically after typing.
    - Optional "abort on mouse move" mode.

---

## 🔧 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/untucked/stay_active_keyboard_mouse.git
cd stay_active_keyboard_mouse
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

**Requirements**:
- Python 3.10+
- `pyautogui`
- `pynput`
- `pywinauto` (for essay mode, Windows only)
- `pytz`

---

## 🚀 Usage

### GUI Mode
Run the Tkinter app:

```bash
python mouse_keyboard.py
```

Or with "essay" mode:

```bash
python mouse_keyboard_wEssay.py
```

You can set the inactivity timeout, start/stop the activity prevention, and enable "Meeting Mode" to pause actions.

### No-GUI Mode
Run in the background with optional arguments:

```bash
python NoGUI/move_mouse_noSleep.py --interval 60 --pixels 2 --alt_tab
```

Arguments:
```
--interval N       Seconds between actions (default: 60)
--pixels N         Pixels to jiggle (default: 2)
--alt_tab          Also press Alt+Tab each interval
--idle_grace N     Skip actions if input detected within last N seconds (default: 10)
--no-keyboard      Disable keyboard listener
```

### Essay Mode
Prepare a text file, e.g. `utils/something_to_read.txt`, then trigger from GUI after inactivity threshold is met.

Standalone test:
```bash
python utils/open_doc_write.py
```

---

## ⚠️ Notes
- macOS/Linux: GUI mode works, but essay mode (Notepad automation) is Windows only.
- macOS: May need to grant **Accessibility** permissions to Python in *System Settings → Privacy & Security → Accessibility* for input control.
- PyAutoGUI has a **fail-safe**: move your mouse to the top-left corner to abort any script.

---

## 📄 License
MIT
