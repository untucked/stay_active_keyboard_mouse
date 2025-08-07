# NoGUI/move_mouse_noSleep.py
import pyautogui as pag
import time
import argparse
import random
import sys

def parse_args():
    p = argparse.ArgumentParser(description="Lightweight keep-alive mouse jiggle.")
    p.add_argument("--interval", type=int, default=60, help="Seconds between actions (default: 60)")
    p.add_argument("--pixels", type=int, default=2, help="Jiggle distance in pixels (default: 2)")
    p.add_argument("--alt_tab", action="store_true", help="Also press Alt+Tab each interval (off by default)")
    p.add_argument("--idle_grace", type=int, default=10, help="Skip jiggle if mouse moved in last N seconds (default: 10)")
    return p.parse_args()

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

def main():
    args = parse_args()
    pag.FAILSAFE = True  # keep the safety

    print(f"Screen size: {pag.size()}")
    print(f"Moving mouse ~every {args.interval}s (pixels={args.pixels}, alt_tab={args.alt_tab})")

    last_pos = pag.position()
    last_pos_time = time.time()

    try:
        while True:
            now = time.time()
            curr_pos = pag.position()
            if curr_pos != last_pos:
                last_pos = curr_pos
                last_pos_time = now

            # Only act if no user move in the last idle_grace seconds
            if (now - last_pos_time) >= args.idle_grace:
                jiggle(args.pixels)
                if args.alt_tab:
                    maybe_alt_tab()
            else:
                # User is active; skip this cycle
                pass

            # Add a tiny random jitter to the timing to look less robotic
            sleep_s = args.interval + random.uniform(-1.0, 1.0)
            time.sleep(max(1.0, sleep_s))
    except KeyboardInterrupt:
        print("\nExiting. Bye!")

if __name__ == "__main__":
    main()
