from window_controller import send_vk_key
import win32gui
import time

def find_wow_window():
    return win32gui.FindWindow(None, '魔兽世界')

def auto_press_key_1():
    hwnd = find_wow_window()
    if hwnd:
        while True:
            send_vk_key(hwnd, "1")
            time.sleep(1)
    else:
        print('找不到魔兽世界窗口')

if __name__ == '__main__':
    auto_press_key_1()