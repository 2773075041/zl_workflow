from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QScrollArea, QGroupBox, QPushButton
from PySide6.QtCore import Signal, Qt

class PropertyPanel(QWidget):
    """属性面板 - 显示选中节点的配置"""

    config_changed = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self._current_node_id = None
        self._config_widgets = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        title = QLabel("属性面板")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)

        self._show_empty_state()

    def _show_empty_state(self):
        self._clear_content()
        empty_label = QLabel("选择节点查看属性")
        empty_label.setStyleSheet("color: gray; padding: 20px;")
        empty_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(empty_label)

    def _clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._config_widgets = {}
        self._current_node_id = None

    def set_node(self, node_id: str, node_type: str, display_name: str, config: dict):
        self._clear_content()
        self._current_node_id = node_id

        info_group = QGroupBox("基本信息")
        info_layout = QFormLayout()
        info_layout.addRow("节点ID:", QLabel(node_id))
        info_layout.addRow("类型:", QLabel(node_type))
        info_layout.addRow("名称:", QLabel(display_name))
        info_group.setLayout(info_layout)
        self.content_layout.addWidget(info_group)

        config_group = QGroupBox("配置")
        config_layout = QFormLayout()

        default_configs = {
            "manual_input": {"prompt": "请输入"},
            "timer_trigger": {"interval": "60", "unit": "秒"},
            "logger": {"level": "INFO", "message": ""},
            "file_writer": {"path": "", "content": ""},
            "http_request": {"url": "", "method": "GET"},
            "condition": {"expression": ""},
            "loop": {"items": "", "variable_name": "item"},
            "sub_workflow": {"workflow_id": ""},
            "agent": {"prompt": "", "model": "gpt-4"},
            "llm_call": {"prompt_template": "", "model": "gpt-4", "temperature": "0.7"},
        }

        default_config = default_configs.get(node_type, {})

        for key, default_value in default_config.items():
            value = config.get(key, default_value)
            edit = QLineEdit(str(value))
            edit.setObjectName(key)
            config_layout.addRow(f"{key}:", edit)
            self._config_widgets[key] = edit

        config_group.setLayout(config_layout)
        self.content_layout.addWidget(config_group)

        btn_layout = QVBoxLayout()
        save_btn = QPushButton("保存配置")
        save_btn.clicked.connect(self._on_save_config)
        reset_btn = QPushButton("重置")
        reset_btn.clicked.connect(self._on_reset_config)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reset_btn)
        self.content_layout.addLayout(btn_layout)

    def _on_save_config(self):
        if self._current_node_id:
            config = self.get_config()
            self.config_changed.emit(self._current_node_id, config)

    def _on_reset_config(self):
        for widget in self._config_widgets.values():
            widget.clear()

    def get_config(self) -> dict:
        if not self._current_node_id:
            return {}
        return {key: widget.text() for key, widget in self._config_widgets.items()}

    def clear(self):
        self._show_empty_state()
