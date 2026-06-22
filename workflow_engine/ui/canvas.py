from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout, QLabel

class WorkflowCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("画布 (待实现)"))
        self.setWidget(widget)