from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel
from PySide6.QtCore import Signal, Qt

class NodePanel(QWidget):
    """节点面板 - 显示可拖拽的节点分类列表"""

    node_selected = Signal(str)  # 发射选中的节点类型

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_nodes()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("节点面板")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree_widget)

    def _load_nodes(self):
        """加载节点分类"""
        categories = {
            "输入": [
                ("manual_input", "手动输入"),
                ("timer_trigger", "定时触发"),
                ("file_watcher", "文件监听"),
                ("webhook", "Webhook触发"),
            ],
            "输出": [
                ("logger", "日志输出"),
                ("file_writer", "文件写入"),
                ("http_request", "HTTP请求"),
            ],
            "流程控制": [
                ("condition", "条件分支"),
                ("loop", "循环执行"),
                ("sub_workflow", "子流程"),
            ],
            "数据处理": [
                ("transform", "数据转换"),
                ("filter", "数据过滤"),
            ],
            "AI": [
                ("agent", "AI Agent"),
                ("llm_call", "LLM调用"),
            ],
        }

        for category, nodes in categories.items():
            category_item = QTreeWidgetItem([category])
            category_item.setExpanded(True)
            for node_type, display_name in nodes:
                node_item = QTreeWidgetItem([display_name])
                node_item.setData(0, Qt.UserRole, node_type)
                category_item.addChild(node_item)
            self.tree_widget.addTopLevelItem(category_item)

    def _on_item_clicked(self, item, column):
        node_type = item.data(0, Qt.UserRole)
        if node_type:
            self.node_selected.emit(node_type)

    def get_selected_node_type(self) -> str:
        item = self.tree_widget.currentItem()
        if item:
            node_type = item.data(0, Qt.UserRole)
            if node_type:
                return node_type
        return ""
