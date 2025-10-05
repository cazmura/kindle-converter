# check_mouse_position.py
import pyautogui
import time

print('マウスの座標を調べます。Ctrl+Cで終了します。')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.5)
except KeyboardInterrupt:
    print('\n終了しました。')
