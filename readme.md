# Stay Active (Keyboard & Mouse)

Keeps your computer from going idle and helps you appear “active” in chat apps by periodically nudging the mouse and/or tapping a harmless key **only when you’ve been inactive for a set amount of time**. It also listens for your real mouse/keyboard activity to reset the inactivity timer.

## What it does
- Watches for **real** keyboard and mouse activity globally.
- If you’re inactive longer than your chosen threshold, it:
  - Jiggles the mouse by a pixel and back, **or**
  - Sends a no-op key tap (like `Shift`)
- Resets the timer the moment you touch your mouse or keyboard.

> ⚠️ Use responsibly. Apps and employers may have policies about activity simulators. You’re responsible for complying with all applicable policies and laws.

## Features
- Global activity detection (mouse move, click/scroll, key press)
- Configurable inactivity timeout and action
- Cross‑platform (Windows, macOS, Linux)

## Install

```bash
git clone https://github.com/untucked/stay_active_keyboard_mouse.git
cd stay_active_keyboard_mouse
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

> If you use macOS, you’ll likely need to grant **Accessibility** permissions (System Settings → Privacy & Security → Accessibility) to your terminal/IDE for input control and event listening.

## Run

```bash
python mouse_keyboard.py --timeout 300 --mode mouse  # 5 min timeout, mouse jiggle
# or
python mouse_keyboard.py --timeout 300 --mode key --key shift  # tap Shift instead
```

### Options
- `--timeout <seconds>`: inactivity seconds before a keep‑alive action (default: 300)
- `--mode <mouse|key>`: action type (default: `mouse`)
- `--key <keyname>`: key for key mode (default: `shift`)

## Troubleshooting
- **No activity detected on macOS**: ensure Accessibility permission is granted to your terminal/IDE and Python.
- **Listener doesn’t reset timer**: some VMs/remote desktops block global hooks—try running locally or with admin privileges.
- **Corporate devices**: endpoint security may block simulated input.

## License
MIT
