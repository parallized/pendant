# win32gui，cv2, numpy
import win32gui
from ctypes import windll
import win32ui
import win32con
import cv2
import time
import numpy as np
from window_controller import find_wow_window

def screenshot(hwnd: int = None, file=None, x=14, y=10, width=90, height=95) -> np.ndarray:
    if not hwnd:
        hwnd = find_wow_window()
    if hwnd == 0:
        raise ValueError("未找到有效窗口句柄")

    windll.user32.SetProcessDPIAware()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bit_map = win32ui.CreateBitmap()
    save_bit_map.CreateCompatibleBitmap(mfc_dc, width, height)

    # 设置视口偏移
    save_dc.SetViewportOrg((-x, -y))
    # 设置截取区域
    save_dc.SelectObject(save_bit_map)

    windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
    bmpinfo = save_bit_map.GetInfo()
    bmpstr = save_bit_map.GetBitmapBits(True)
    capture = np.frombuffer(bmpstr, dtype=np.uint8).reshape(
        (bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
    capture = np.ascontiguousarray(capture)[..., :-1]

    win32gui.DeleteObject(save_bit_map.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    # capture = cv2.cvtColor(capture, cv2.COLOR_RGBA2RGB)

    capture = cv2.cvtColor(capture, cv2.COLOR_RGB2GRAY)
    if file:
        cv2.imwrite(file, capture)
    return capture

if __name__ == "__main__":
    try:
        lastTime = time.time()
        while True:
            screenshot(file="screenshot.png", x=14, y=10, width=90, height=95)
            print("fps: ", 1 / (time.time() - lastTime))
            lastTime = time.time()
        print("截图保存成功")
    except Exception as e:
        print(f"截图失败: {str(e)}")