from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from style import Styles
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QAbstractNativeEventFilter
import win32con
import win32gui
from PyQt6.QtGui import QShortcut
from PyQt6.QtMultimedia import QSoundEffect
import sys
from screen_ocr import capture_and_recognize
from window_controller import find_wow_window, send_vk_key
import time

class OCRWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    stopped = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        lastTime = time.time()
        hwnd = find_wow_window()
        if hwnd == 0:
            self.error.emit("未找到魔兽世界窗口")
            self.stopped.emit()
            return

        self.is_running = True
        while self.is_running:
            try:
                result = capture_and_recognize()
                for num in result:
                    send_vk_key(hwnd, num)
                if result:
                    result += " "
                self.finished.emit(result + f"{round(1 / (time.time() - lastTime), 2)} fps")
                lastTime = time.time()
            except Exception as e:
                self.error.emit(str(e))
                self.stopped.emit()
                return
    
    def stop(self):
        self.is_running = False

class ModernApp(QMainWindow):
    hotkey_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.counter = 1
        self.is_active = False
        
        # 初始化热键管理器
        from window_controller import HotkeyManager
        self.hotkey_mgr = HotkeyManager()
        self.hotkey_mgr.register(self.handle_hotkey)
        self.hotkey_signal.connect(self.toggle_state)

    def handle_hotkey(self):
        print("hotkey pressed")
        self.hotkey_signal.emit()

    def toggle_state(self):
        self.is_active = not self.is_active
        if self.is_active:
            # stop
            self.worker.stop()
            self.action_btn.setText('开始持续识别')
            self.action_btn.setStyleSheet(Styles.BUTTON)
        else:
            # start
            self.worker.start()
            self.action_btn.setText('停止识别')
            self.action_btn.setStyleSheet(Styles.ACTIVE_BUTTON)
        # if self.is_active:
        #     self.sound_on.play()
        # else:
        #     self.sound_off.play()


    def initUI(self):
        self.setWindowTitle('pendant')
        self.setGeometry(300, 300, 600, 400)
        self.setFixedSize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet(Styles.TEXT_EDIT)
        layout.addWidget(self.text_output)

        self.action_btn = QPushButton('开始持续识别')
        self.worker = OCRWorker()
        self.worker.finished.connect(self.on_ocr_finished)
        self.worker.error.connect(self.on_ocr_error)
        self.worker.stopped.connect(self.on_ocr_stopped)
        self.action_btn.clicked.connect(self.toggle_ocr)
        self.action_btn.setStyleSheet(Styles.BUTTON)
        layout.addWidget(self.action_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def toggle_ocr(self):
        if self.worker.isRunning():
            self.worker.stop()
            self.action_btn.setText('开始持续识别')
            self.action_btn.setStyleSheet(Styles.BUTTON)
        else:
            self.worker.start()
            self.action_btn.setText('停止识别')
            self.action_btn.setStyleSheet(Styles.ACTIVE_BUTTON)

    def on_ocr_finished(self, result):
        self.text_output.append(f"{result}")

    def on_ocr_stopped(self):
        self.action_btn.setText('开始持续识别')
        self.action_btn.setStyleSheet(Styles.BUTTON)

    def on_ocr_error(self, error_msg):
        self.text_output.append(f"错误: {error_msg}")
        self.action_btn.setEnabled(True)

    def closeEvent(self, event):
        self.hotkey_mgr.unregister()
        event.accept()

class MsgThread(QThread):
    def run(self):
        while getattr(self, "_running", True):
            win32gui.PumpMessages()
            time.sleep(0.1)
    
    def stop(self):
        self._running = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernApp()
    window.show()
    sys.exit(app.exec())