from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor

NODE_CATEGORIES = {
    "输入": {"color": "#4A90D9", "category_key": "input", "nodes": [
        ("manual_input", "手动输入"), ("timer_trigger", "定时触发"),
        ("file_watcher", "文件监听"), ("webhook", "Webhook")]},
    "输出": {"color": "#5CB85C", "category_key": "output", "nodes": [
        ("logger", "日志输出"), ("file_writer", "文件写入"), ("http_request", "HTTP请求")]},
    "流程控制": {"color": "#E8A87C", "category_key": "flow", "nodes": [
        ("condition", "条件分支"), ("loop", "循环执行"), ("sub_workflow", "子流程")]},
    "数据处理": {"color": "#D4A574", "category_key": "data", "nodes": [
        ("transform", "数据转换"), ("filter", "数据过滤")]},
    "AI": {"color": "#9B59B6", "category_key": "ai", "nodes": [
        ("agent", "AI Agent"), ("llm_call", "LLM调用")]},
}

NODE_ICONS = {
    "manual_input": "📝", "timer_trigger": "⏰", "file_watcher": "👁", "webhook": "🪝",
    "logger": "📋", "file_writer": "💾", "http_request": "🌐",
    "condition": "🔀", "loop": "🔁", "sub_workflow": "📦",
    "transform": "⚙", "filter": "🔍", "agent": "🤖", "llm_call": "💬",
}


class NodeCard(QWidget):
    clicked = Signal(str)

    def __init__(self, node_type, display_name, category_key, accent_color):
        super().__init__()
        self.node_type = node_type
        self.accent_color = accent_color
        self.setObjectName("NodeCard")
        self.setCursor(Qt.PointingHandCursor)
        self._setup_ui(display_name)

    def _setup_ui(self, display_name):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(NODE_ICONS.get(self.node_type, "⬡"))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 26px; color: {self.accent_color};")
        layout.addWidget(icon_label)

        name_label = QLabel(display_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("font-size: 10px; color: #E0D8D0; background: transparent; font-weight: bold;")
        layout.addWidget(name_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.node_type)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(8)
        glow.setColor(QColor(self.accent_color + "60"))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)
        super().leaveEvent(event)


class NodePanel(QWidget):
    node_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("node_panel_container")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("节点面板")
        title.setObjectName("node_panel_title")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background-color: #2D2D2D;")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(16)

        for category, config in NODE_CATEGORIES.items():
            cat_label = QLabel(category)
            cat_label.setStyleSheet(
                f"font-size: 11px; font-weight: bold; color: {config['color']};"
                "letter-spacing: 1px; padding: 4px 0;"
            )
            content_layout.addWidget(cat_label)

            grid = QGridLayout()
            grid.setSpacing(8)
            for i, (node_type, display_name) in enumerate(config["nodes"]):
                card = NodeCard(node_type, display_name, config["category_key"], config["color"])
                card.clicked.connect(self._on_card_clicked)
                grid.addWidget(card, i // 2, i % 2)
            content_layout.addLayout(grid)

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _on_card_clicked(self, node_type):
        self.node_selected.emit(node_type)

    def get_selected_node_type(self):
        return ""
