import win32gui
import win32con
import time
import keyboard

class HotkeyManager:
    def __init__(self):
        self.hotkey_handle = None
        print('Ctrl+H 热键已初始化')  
        
    def register(self, callback):
        self.hotkey_handle = keyboard.add_hotkey('ctrl+h', lambda: callback())
        print('Ctrl+H 已注册')
        
    def unregister(self):
        if self.hotkey_handle:
            keyboard.remove_hotkey(self.hotkey_handle)
            print('Ctrl+H 已注销')

def find_wow_window():
    return win32gui.FindWindow(None, '魔兽世界')

def send_vk_key(hwnd, char):
    allowed_chars = {'0','1','2','3','4','5','6','7','8','9','Q','E','R','T','F','G','Z','X','C','V','Y'}
    if char.upper() not in allowed_chars:
        return '非法字符'
    if char.isdigit():
        vk_code = 0x30 + int(char)
    elif char.isalpha():
        vk_code = ord(char.upper())
    else:
        return '无效字符'
    
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
    time.sleep(0.001)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
    