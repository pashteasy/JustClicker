# JustClicker
Simple autoclicker with UI.

In the first window, you need to select the type of clicker.

PyAutoGuiClicker - uses the PyAutoGui library and pyautogui.click() to press the mouse button.
PynputClicker - uses the Pynput library and the press-sleep-release logic (sometimes works better in some games) to press the mouse button.
KeyboardClicker - uses the Pynput library to press keyboard keys.

When selecting a clicker, you can also select a mouse button/keyboard key.

Hotkeys:
Space - Start click and pause.
Tab - Save coordinates in list.

Text fields:
Click interval(ms) - sets the interval between clicks in milliseconds.
Cycle delay(s) - sets the interval between cycles (click on all coordinates in the list) in seconds.

Button:
Start/Pause - start click and pause.
Reset crds - resets the list of coordinates.
Save crds - saves the current list of coordinates to the file coordinates.json.
Load crds - loads a list of coordinates from a file.


Random delay - sets the delay as t+random(0,t).

