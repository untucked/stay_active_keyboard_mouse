# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:03:15 2021

An updated script to prevent the computer from going to sleep by moving the mouse and simulating keystrokes.
"""

import pyautogui as pag
from time import sleep

print(pag.size())  # Print screen size
print('Moving mouse slightly every 1 minute')
wait_time = 60  # 1 minute
i = 0

def move_mouse(i):
    """
    Moves the mouse slightly to prevent inactivity.
    """
    try:
        pos = pag.position()
        x, y = pos.x, pos.y
        if i % 2:
            x += 2
            y += 2
        else:
            x -= 2
            y -= 2

        pag.moveTo(x, y, duration=1)
    except pag.FailSafeException as e:
        print(f"Mouse movement error: {e}")

def press_alt_tab():
    """
    Simulates pressing Alt+Tab to switch windows.
    """
    try:
        pag.hotkey("alt", "tab")
    except pag.FailSafeException as e:
        print(f"Keyboard action error: {e}")

while True:
    move_mouse(i)
    press_alt_tab()
    sleep(wait_time)
    i += 1
