from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class NodePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("节点面板 (待实现)"))