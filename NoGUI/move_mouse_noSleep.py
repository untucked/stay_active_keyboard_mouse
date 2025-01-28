# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:03:15 2021

@author: beylander
"""

import pyautogui as pag
from  time import sleep
print(pag.size())

print('Moving mouse slightly every 1 minutes')
wait_time = 60*1
i=0
while True:    
    # pag.moveRel(0, 1, duration = 1)
    # pag.scroll(1)
    pos= pag.position()
    x,y = pos.x,pos.y
    if i%2:
        x = x+2
        y = y+2
    else:
        x = x-2
        y = y-2

    pag.moveTo(x,y,duration=1)

    
    pag.hotkey("altleft","tab")
    # pag.hotkey("shift")
    sleep(wait_time)
    i+=1



# pag.moveTo(1, 1, duration = 1)