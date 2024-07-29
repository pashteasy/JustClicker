# JustClicker
Simple autoclicker with UI

Hotkeys:
Space - Start click and pause
Tab - Save coordinates in list

Text fields:
Click interval(ms) - sets the interval between clicks in milliseconds
Cycle delay(s) - sets the interval between cycles (click on all coordinates in the list) in seconds

Button:
Start/Pause - start click and pause
Reset crds - resets the list of coordinates
Save crds - saves the current list of coordinates to the file coordinates.txt
Load crds - loads a list of coordinates from a file


Random delay - sets the delay as t+random(0,t)

main.py uses the pyautogui library
main2.py uses the pynput library (sometimes works better in some games)
