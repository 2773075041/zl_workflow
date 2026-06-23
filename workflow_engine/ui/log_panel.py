from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from datetime import datetime

class LogPanel(QWidget):
    """日志面板 - 显示执行日志"""

    def __init__(self):
        super().__init__()
        self.setObjectName("log_panel_container")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        title_layout = QHBoxLayout()
        title = QLabel("执行日志")
        title.setObjectName("log_panel_title")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title)
        title_layout.addStretch()

        clear_btn = QPushButton("清除")
        clear_btn.clicked.connect(self.clear)
        title_layout.addWidget(clear_btn)

        layout.addLayout(title_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_text)

    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "#4ec9b0",
            "DEBUG": "#9cdcfe",
            "WARNING": "#dcdcaa",
            "ERROR": "#f14c4c",
            "SUCCESS": "#6a9955",
        }
        color = colors.get(level, "#d4d4d4")

        html = f'<span style="color: #808080;">[{timestamp}]</span> '
        html += f'<span style="color: {color}; font-weight: bold;">[{level}]</span> '
        html += f'<span style="color: #d4d4d4;">{message}</span>'

        self.log_text.append(html)

    def info(self, message: str):
        self.log("INFO", message)

    def debug(self, message: str):
        self.log("DEBUG", message)

    def warning(self, message: str):
        self.log("WARNING", message)

    def error(self, message: str):
        self.log("ERROR", message)

    def success(self, message: str):
        self.log("SUCCESS", message)

    def clear(self):
        self.log_text.clear()
