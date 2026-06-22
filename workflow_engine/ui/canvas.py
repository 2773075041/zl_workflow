from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPointF, pyqtSignal as Signal, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter

class NodeGraphicsItem(QGraphicsRectItem):
    """节点图形项"""

    def __init__(self, node_id: str, node_type: str, display_name: str = "", width: float = 120, height: float = 60):
        super().__init__(0, 0, width, height)
        self.node_id = node_id
        self.node_type = node_type
        self.setBrush(QBrush(QColor("#3498db")))
        self.setPen(QPen(QColor("#2980b9"), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        # 添加文本
        text = QGraphicsTextItem(self)
        text.setPlainText(display_name or node_type)
        text.setDefaultTextColor(QColor("white"))
        text.setPos(10, 20)

        # 输入端口（左侧）
        self.input_port = QGraphicsRectItem(-8, height/2 - 5, 10, 10, self)
        self.input_port.setBrush(QBrush(QColor("#2ecc71")))
        self.input_port.setPen(QPen(QColor("#27ae60"), 1))

        # 输出端口（右侧）
        self.output_port = QGraphicsRectItem(width - 2, height/2 - 5, 10, 10, self)
        self.output_port.setBrush(QBrush(QColor("#e74c3c")))
        self.output_port.setPen(QPen(QColor("#c0392b"), 1))

    def set_color(self, color: str):
        self.setBrush(QBrush(QColor(color)))

    def set_selected(self, selected: bool):
        if selected:
            self.setPen(QPen(QColor("#f1c40f"), 3))
        else:
            self.setPen(QPen(QColor("#2980b9"), 2))


class EdgeGraphicsItem(QGraphicsLineItem):
    """连线图形项"""

    def __init__(self, source_item: NodeGraphicsItem, target_item: NodeGraphicsItem):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.setPen(QPen(QColor("#7f8c8d"), 2))
        self.setZValue(-1)
        self.update_line()

    def update_line(self):
        source_pos = self.source_item.scenePos()
        target_pos = self.target_item.scenePos()

        start = QPointF(
            source_pos.x() + self.source_item.rect().width(),
            source_pos.y() + self.source_item.rect().height() / 2
        )
        end = QPointF(
            target_pos.x(),
            target_pos.y() + self.target_item.rect().height() / 2
        )
        self.setLine(start.x(), start.y(), end.x(), end.y())


class WorkflowCanvas(QGraphicsView):
    """工作流画布"""

    node_double_clicked = Signal(str)
    node_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

        self._node_items = {}
        self._edge_items = []
        self._selected_node_id = None

        self._setup背景()

    def _setup背景(self):
        """设置背景"""
        self.setBackgroundBrush(QBrush(QColor("#2c3e50")))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def add_node(self, node_id: str, node_type: str, x: float, y: float, display_name: str = "") -> NodeGraphicsItem:
        """添加节点"""
        if node_id in self._node_items:
            return self._node_items[node_id]

        item = NodeGraphicsItem(node_id, node_type, display_name)
        item.setPos(x, y)
        self.scene.addItem(item)
        self._node_items[node_id] = item
        return item

    def remove_node(self, node_id: str):
        """删除节点"""
        if node_id not in self._node_items:
            return

        item = self._node_items.pop(node_id)
        self.scene.removeItem(item)

        # 移除相关连线
        edges_to_remove = [e for e in self._edge_items if e.source_item.node_id == node_id or e.target_item.node_id == node_id]
        for edge in edges_to_remove:
            self.scene.removeItem(edge)
            self._edge_items.remove(edge)

    def add_edge(self, source_id: str, target_id: str):
        """添加连线"""
        if source_id not in self._node_items or target_id not in self._node_items:
            return

        source_item = self._node_items[source_id]
        target_item = self._node_items[target_id]

        edge = EdgeGraphicsItem(source_item, target_item)
        self.scene.addItem(edge)
        self._edge_items.append(edge)

    def get_node_position(self, node_id: str) -> QPointF:
        """获取节点位置"""
        if node_id in self._node_items:
            return self._node_items[node_id].pos()
        return QPointF()

    def get_selected_node_id(self) -> str:
        """获取选中的节点ID"""
        return self._selected_node_id

    def clear(self):
        """清空画布"""
        self.scene.clear()
        self._node_items.clear()
        self._edge_items.clear()
        self._selected_node_id = None

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            if self._selected_node_id:
                self.remove_node(self._selected_node_id)
                self._selected_node_id = None
        super().keyPressEvent(event)
