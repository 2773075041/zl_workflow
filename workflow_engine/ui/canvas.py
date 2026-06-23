from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsDropShadowEffect, QMenu
from PySide6.QtCore import Qt, QPointF, Signal, QRectF, QTimer
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath, QFont

BG_PRIMARY = "#1E1E1E"
EDGE_DEFAULT = "#5C6370"
GRID_DOT_COLOR = "#2A2A2A"
GRID_DOT_SIZE = 1.5
GRID_SPACING = 20
NODE_COLORS = {
    "input": {"primary": "#6A9EC9", "secondary": "#4A7EA9"},
    "output": {"primary": "#7A9E6B", "secondary": "#5A7E4B"},
    "flow": {"primary": "#C8A080", "secondary": "#A88060"},
    "data": {"primary": "#B0A07A", "secondary": "#90805A"},
    "ai": {"primary": "#9A7AAA", "secondary": "#7A5A8A"},
    "default": {"primary": "#6A9EC9", "secondary": "#4A7EA9"},
}
NODE_W, NODE_H, NODE_R, PORT_R = 140, 80, 8, 6
NODE_TYPE_TO_CATEGORY = {
    "manual_input": "input", "timer_trigger": "input", "file_watcher": "input", "webhook": "input",
    "logger": "output", "file_writer": "output", "http_request": "output",
    "condition": "flow", "loop": "flow", "sub_workflow": "flow",
    "transform": "data", "filter": "data",
    "agent": "ai", "llm_call": "ai",
}

class NodeGraphicsItem(QGraphicsRectItem):
    """美化版节点图形项 — 圆角卡片 + 发光效果"""

    def __init__(self, node_id: str, node_type: str, display_name: str = "",
                 category: str = "default", width: float = NODE_W, height: float = NODE_H):
        super().__init__(0, 0, width, height)
        self.node_id = node_id
        self.node_type = node_type
        self.category = category
        self.node_state = "idle"
        colors = NODE_COLORS.get(category, NODE_COLORS["default"])
        self.primary_color = colors["primary"]
        self.secondary_color = colors["secondary"]
        self.setBrush(QBrush(QColor(self.primary_color)))
        self.setPen(QPen(QColor(self.secondary_color), 1))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        text = QGraphicsTextItem(self)
        text.setPlainText(display_name or node_type)
        text.setDefaultTextColor(QColor("#D4D4D4"))
        text.setFont(QFont("Segoe UI", 10, QFont.Bold))
        text.setPos(12, height / 2 - 10)
        type_label = QGraphicsTextItem(self)
        type_label.setPlainText(f"[{category}]")
        type_label.setDefaultTextColor(QColor("#E0D8D0" + "80"))
        type_label.setFont(QFont("Segoe UI", 7))
        type_label.setPos(12, height / 2 + 6)
        port_y = height / 2
        self.input_port = QGraphicsEllipseItem(-PORT_R, port_y - PORT_R, PORT_R * 2, PORT_R * 2, self)
        self.input_port.setBrush(QBrush(QColor("#7A9E6B")))
        self.input_port.setPen(QPen(QColor("#5A7E4B"), 1))
        self.input_port.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.output_port = QGraphicsEllipseItem(width - PORT_R, port_y - PORT_R, PORT_R * 2, PORT_R * 2, self)
        self.output_port.setBrush(QBrush(QColor("#E74C3C")))
        self.output_port.setPen(QPen(QColor("#C0392b"), 1))
        self.output_port.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(0)
        self.glow_effect.setColor(QColor(self.primary_color + "00"))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)

    def set_state(self, state: str):
        self.node_state = state
        if state == "idle":
            self.glow_effect.setBlurRadius(0)
            self.glow_effect.setColor(QColor(self.primary_color + "00"))
            self.setPen(QPen(QColor(self.secondary_color), 1))
        elif state == "running":
            self._start_pulse()
        elif state == "success":
            self._stop_pulse()
            self.glow_effect.setBlurRadius(15)
            self.glow_effect.setColor(QColor("#7A9E6B60"))
            self.setPen(QPen(QColor("#7A9E6B"), 2))
        elif state == "error":
            self._stop_pulse()
            self.glow_effect.setBlurRadius(15)
            self.glow_effect.setColor(QColor("#E74C3C60"))
            self.setPen(QPen(QColor("#E74C3C"), 2))

    def _start_pulse(self):
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_step)
        self._pulse_timer.start(50)
        self._pulse_phase = 0.0

    def _stop_pulse(self):
        if hasattr(self, "_pulse_timer"):
            self._pulse_timer.stop()

    def _pulse_step(self):
        import math
        self._pulse_phase += 0.1
        glow = int(15 + 15 * math.sin(self._pulse_phase))
        self.glow_effect.setBlurRadius(glow)
        r1, g1, b1 = self._hex_to_rgb(self.secondary_color)
        r2, g2, b2 = 245, 192, 122
        t = (math.sin(self._pulse_phase) + 1) / 2
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        self.setPen(QPen(QColor(r, g, b), 2))

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def set_selected(self, selected: bool):
        if selected:
            self.setPen(QPen(QColor("#007ACC"), 2))
            self.glow_effect.setBlurRadius(10)
            self.glow_effect.setColor(QColor("#007ACC40"))
        else:
            self.set_state(self.node_state)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor("#007ACC"), 1))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.set_selected(self.isSelected())
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in getattr(self, '_edges', []):
                edge.update_path()
        return super().itemChange(change, value)


class EdgeGraphicsItem(QGraphicsPathItem):
    """连线图形项（贝塞尔曲线）"""

    def __init__(self, source_item: NodeGraphicsItem, target_item: NodeGraphicsItem):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.setPen(QPen(QColor(EDGE_DEFAULT), 2))
        self.setZValue(-1)
        # 注册到源节点
        if not hasattr(source_item, '_edges'):
            source_item._edges = []
        source_item._edges.append(self)
        self.update_path()

    def update_path(self):
        """更新贝塞尔曲线路径"""
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

        # 计算控制点偏移
        dx = abs(end.x() - start.x())
        offset = max(dx * 0.5, 50)

        # 创建贝塞尔曲线
        path = QPainterPath()
        path.moveTo(start)
        cp1 = QPointF(start.x() + offset, start.y())
        cp2 = QPointF(end.x() - offset, end.y())
        path.cubicTo(cp1, cp2, end)
        self.setPath(path)

    def update_line(self):
        """兼容旧API"""
        self.update_path()


class WorkflowCanvas(QGraphicsView):
    """工作流画布"""

    node_double_clicked = Signal(str)
    node_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

        self._node_items = {}
        self._edge_items = []
        self._selected_node_id = None

        self._setup背景()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2D2D2D;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 32px 6px 16px;
                color: #D4D4D4;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QMenu::separator {
                height: 1px;
                background-color: #3C3C3C;
                margin: 4px 0;
            }
        """)
        delete_action = menu.addAction("删除节点 (Del)")
        menu.addSeparator()
        clear_action = menu.addAction("清空画布")

        action = menu.exec(self.mapToGlobal(pos))
        if action == delete_action and self._selected_node_id:
            self.remove_node(self._selected_node_id)
            self._selected_node_id = None
        elif action == clear_action:
            self.clear()

    def _setup背景(self):
        """设置背景"""
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        """绘制背景和点阵"""
        # 绘制背景色
        painter.fillRect(rect, QColor(BG_PRIMARY))

        # 绘制点阵
        painter.setPen(QPen(QColor(GRID_DOT_COLOR)))
        painter.setBrush(QBrush(QColor(GRID_DOT_COLOR)))

        left = int(rect.left()) - (int(rect.left()) % int(GRID_SPACING))
        top = int(rect.top()) - (int(rect.top()) % int(GRID_SPACING))

        for x in range(left, int(rect.right()), int(GRID_SPACING)):
            for y in range(top, int(rect.bottom()), int(GRID_SPACING)):
                painter.drawEllipse(x - GRID_DOT_SIZE / 2, y - GRID_DOT_SIZE / 2, GRID_DOT_SIZE, GRID_DOT_SIZE)

    def add_node(self, node_id: str, node_type: str, x: float, y: float, display_name: str = "", category: str = "") -> NodeGraphicsItem:
        """添加节点"""
        if node_id in self._node_items:
            return self._node_items[node_id]
        if not category:
            category = NODE_TYPE_TO_CATEGORY.get(node_type, "default")
        item = NodeGraphicsItem(node_id, node_type, display_name, category)
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
