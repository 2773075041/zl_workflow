from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PropertyPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("属性面板 (待实现)"))