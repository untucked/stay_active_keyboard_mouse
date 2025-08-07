# NoGUI/move_mouse_noSleep.py
import pyautogui as pag
import time
import argparse
import random
import sys
import threading

try:
    from pynput import keyboard
except ImportError:
    keyboard = None  # we'll warn if user asked for keyboard listening but lib isn't installed

def parse_args():
    p = argparse.ArgumentParser(description="Lightweight keep-alive mouse jiggle.")
    p.add_argument("--interval", type=int, default=60, help="Seconds between actions (default: 60)")
    p.add_argument("--pixels", type=int, default=2, help="Jiggle distance in pixels (default: 2)")
    p.add_argument("--alt_tab", action="store_true", help="Also press Alt+Tab each interval (off by default)")
    p.add_argument("--idle_grace", type=int, default=10, help="Skip jiggle if input in last N seconds (default: 10)")
    p.add_argument("--no-keyboard", action="store_true", help="Disable keyboard listener (enabled by default)")
    return p.parse_args()

_last_input_time = time.time()
_lock = threading.Lock()

def mark_input():
    global _last_input_time
    with _lock:
        _last_input_time = time.time()

def seconds_since_input():
    with _lock:
        return time.time() - _last_input_time

def jiggle(pixels: int):
    try:
        x, y = pag.position()
        dx = pixels if random.choice((True, False)) else -pixels
        dy = pixels if random.choice((True, False)) else -pixels
        pag.moveRel(dx, dy, duration=0)   # out
        pag.moveRel(-dx, -dy, duration=0) # back
    except pag.FailSafeException:
        print("[move_mouse] PyAutoGUI fail-safe triggered (top-left).", file=sys.stderr)

def maybe_alt_tab():
    try:
        pag.hotkey("alt", "tab")
    except pag.FailSafeException:
        print("[alt_tab] PyAutoGUI fail-safe triggered.", file=sys.stderr)

def start_keyboard_listener():
    if keyboard is None:
        print("[warn] pynput not installed; keyboard listening disabled. `pip install pynput` to enable.")
        return None
    def on_press(_key):
        mark_input()
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener

def main():
    args = parse_args()
    pag.FAILSAFE = True  # keep the safety

    print(f"Screen: {pag.size()}")
    print(f"Tick ~every {args.interval}s (pixels={args.pixels}, alt_tab={args.alt_tab}, keyboard={'on' if not args.no_keyboard else 'off'})")

    # seed with current mouse position so mouse movement updates idle immediately
    last_mouse_pos = pag.position()
    mark_input()

    # optional keyboard listener
    kb_listener = None
    if not args.no_keyboard:
        kb_listener = start_keyboard_listener()

    try:
        while True:
            # update last-input time on mouse movement
            curr = pag.position()
            if curr != last_mouse_pos:
                last_mouse_pos = curr
                mark_input()

            # act only if we've been idle longer than grace
            if seconds_since_input() >= args.idle_grace:
                jiggle(args.pixels)
                if args.alt_tab:
                    maybe_alt_tab()

            sleep_s = args.interval + random.uniform(-1.0, 1.0)
            time.sleep(max(1.0, sleep_s))
    except KeyboardInterrupt:
        print("\nExiting. Bye!")
    finally:
        if kb_listener:
            kb_listener.stop()

if __name__ == "__main__":
    main()
