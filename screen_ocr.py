import pyautogui
import pytesseract
from PIL import Image
import os
from datetime import datetime

def capture_and_recognize(x=14, y=10, width=90, height=95):
    from bgclip import screenshot
    capture = screenshot(x=x, y=y, width=width, height=height)
    processed_img = Image.fromarray(capture)

    # 截取 x,y 开始的区域
    processed_img = processed_img.crop((x, y, width-x, height-y))
    
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    img_path = os.path.join('logs', f'screenshot_{timestamp}.png')
    # processed_img.save(img_path)
    
    text = pytesseract.image_to_string(processed_img, config='--psm 6')
    allowed_chars = set('0123456789QERTFGZXCVY')
    return ''.join([c for c in text.strip().upper() if c in allowed_chars])