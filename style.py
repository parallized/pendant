class Styles:
    TEXT_EDIT = """
        QTextEdit {
            border-radius: 8px;
            padding: 12px;
            font-family: 'Segoe UI';
            font-size: 14px;
        }
    """

    BUTTON = """
        QPushButton {
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 16px;
            font-family: 'Segoe UI';
            font-size: 14px;
            min-width: 120px;
            background-color: #999;
        }
        QPushButton:hover {
            background-color: #777;
        }
        QPushButton:pressed {
            background-color: #888;
        }
    """

    ACTIVE_BUTTON = """
        QPushButton {
            color: white;
            border: none;
            border-radius: 6px;     
        }
    """