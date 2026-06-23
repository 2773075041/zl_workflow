# 工作流引擎 UI 美化 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将工作流引擎 PySide6 UI 升级为复古工业风 × 赛博朋克暖光的深色专业主题，包含网格点阵画布、贝塞尔曲线连线、扁平卡片节点面板、节点呼吸脉冲动画、全套UI美化。

**Architecture:** 统一 QSS 样式表架构，颜色常量集中在 `theme.py`，各组件样式分散到独立 `.qss` 文件，`__init__.py` 统一加载。画布绘图使用 Qt Graphics Framework 重写节点/连线绘制逻辑，添加 QGraphicsEffect 实现发光效果。

**Tech Stack:** Python 3.12 + PySide6 >= 6.5 + Qt Graphics Framework

---

## 文件清单

| 文件 | 操作 | 职责 |
|------|------|------|
| `workflow_engine/ui/styles/__init__.py` | 新建 | 样式加载入口，暴露 `load_stylesheet()` |
| `workflow_engine/ui/styles/theme.py` | 新建 | 主题颜色/字体常量定义 |
| `workflow_engine/ui/styles/base.qss` | 新建 | 全局基础样式（背景/字体/滚动条） |
| `workflow_engine/ui/styles/components.qss` | 新建 | 通用组件样式（按钮/输入框/树形控件） |
| `workflow_engine/ui/styles/main_window.qss` | 新建 | 主窗口/菜单/工具栏样式 |
| `workflow_engine/ui/styles/node_panel.qss` | 新建 | 节点面板网格卡片样式 |
| `workflow_engine/ui/styles/canvas.qss` | 新建 | 画布背景样式 |
| `workflow_engine/ui/styles/property_panel.qss` | 新建 | 属性面板样式 |
| `workflow_engine/ui/styles/log_panel.qss` | 新建 | 日志面板样式 |
| `workflow_engine/ui/main_window.py` | 修改 | `_load_stylesheet()` 调用 |
| `workflow_engine/ui/canvas.py` | 修改 | 贝塞尔曲线 + 网格背景 + 节点样式 + 呼吸动画 |
| `workflow_engine/ui/node_panel.py` | 修改 | 网格卡片布局 + 拖拽信号 |

---

## Task 1: 创建样式基础设施（theme.py + base.qss + components.qss + 加载入口）

**Files:**
- 创建: `workflow_engine/ui/styles/__init__.py`
- 创建: `workflow_engine/ui/styles/theme.py`
- 创建: `workflow_engine/ui/styles/base.qss`
- 创建: `workflow_engine/ui/styles/components.qss`

- [ ] **Step 1: 创建 `workflow_engine/ui/styles/` 目录结构**

创建 `workflow_engine/ui/styles/__init__.py`：

```python
"""UI 样式模块 — 统一加载 QSS 样式表"""

import os
from pathlib import Path

_STYLES_DIR = Path(__file__).parent

def load_stylesheet() -> str:
    """加载并合并所有 QSS 样式文件"""
    files = [
        "base.qss",
        "components.qss",
        "main_window.qss",
        "node_panel.qss",
        "canvas.qss",
        "property_panel.qss",
        "log_panel.qss",
    ]
    parts = []
    for fname in files:
        path = _STYLES_DIR / fname
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)
```

- [ ] **Step 2: 创建 `workflow_engine/ui/styles/theme.py`** — 定义所有颜色/字体常量

```python
"""主题颜色与字体常量 — 复古工业风 × 赛博朋克暖光"""

# === 主背景色 ===
BG_PRIMARY = "#1E1E1E"        # 主背景
BG_SECONDARY = "#252526"       # 次级背景（菜单/工具栏）
BG_PANEL = "#2D2D2D"          # 面板背景
BG_INPUT = "#1E1E1E"           # 输入框背景
BORDER = "#3C3C3C"             # 边框/分割线
BORDER_HOVER = "#5C6370"       # 边框悬停

# === 强调色 ===
ACCENT_PRIMARY = "#E8A87C"     # 琥珀橙（主强调）
ACCENT_SECONDARY = "#C38D9E"   # 珊瑚橙
ACCENT_HIGHLIGHT = "#F5C07A"   # 暖黄（悬停/高亮）
ACCENT_SUBTLE = "#E8A87C30"    # 半透明琥珀（选中背景）

# === 文字色 ===
TEXT_PRIMARY = "#E0D8D0"      # 主要文字
TEXT_SECONDARY = "#8A8A8A"     # 次要文字
TEXT_INVERSE = "#1A1A1A"       # 反色文字（深底浅字）
TEXT_DISABLED = "#555555"      # 禁用文字

# === 节点分类色 ===
NODE_INPUT = {"primary": "#4A90D9", "secondary": "#2E6EB0"}      # 蓝色
NODE_OUTPUT = {"primary": "#5CB85C", "secondary": "#3D8B3D"}    # 绿色
NODE_FLOW = {"primary": "#E8A87C", "secondary": "#C38D9E"}     # 橙色/珊瑚
NODE_DATA = {"primary": "#D4A574", "secondary": "#B8860B"}     # 驼色
NODE_AI = {"primary": "#9B59B6", "secondary": "#7D3C98"}      # 紫色

# === 连线色 ===
EDGE_DEFAULT = "#5C6370"
EDGE_HOVER = "#E8A87C"
EDGE_RUNNING = "#F5C07A"
EDGE_SUCCESS = "#5CB85C"
EDGE_ERROR = "#E74C3C"

# === 日志色 ===
LOG_INFO = "#4EC9B0"
LOG_DEBUG = "#9CDCFE"
LOG_WARNING = "#DCDCAA"
LOG_ERROR = "#F14C4C"
LOG_SUCCESS = "#6A9955"
LOG_TIMESTAMP = "#808080"

# === 字体 ===
FONT_MAIN = "Segoe UI, Microsoft YaHei, sans-serif"
FONT_MONO = "Cascadia Code, Consolas, monospace"

# === 节点尺寸 ===
NODE_WIDTH = 140
NODE_HEIGHT = 80
NODE_RADIUS = 8
NODE_PORT_RADIUS = 6

# === 网格点阵 ===
GRID_DOT_COLOR = "#2A2A2A"
GRID_DOT_SIZE = 1.5
GRID_SPACING = 20
```

- [ ] **Step 3: 创建 `workflow_engine/ui/styles/base.qss`** — 全局基础样式

```css
/* base.qss — 全局基础样式 */

QWidget {
    background-color: #1E1E1E;
    color: #E0D8D0;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 12px;
}

QWidget:disabled {
    color: #555555;
}

/* 滚动条 */
QScrollBar:vertical {
    background: #1E1E1E;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #3C3C3C;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #5C6370;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background: #1E1E1E;
    height: 10px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: #3C3C3C;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #5C6370;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* 分隔线 */
QMainWindow::separator {
    background: #3C3C3C;
    width: 1px;
    height: 1px;
}

/* 工具提示 */
QToolTip {
    background-color: #2D2D2D;
    color: #E0D8D0;
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 4px;
}
```

- [ ] **Step 4: 创建 `workflow_engine/ui/styles/components.qss`** — 通用组件样式

```css
/* components.qss — 通用组件样式 */

/* === 按钮 === */
QPushButton {
    background-color: #3C3C3C;
    color: #E0D8D0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 16px;
    min-width: 60px;
}
QPushButton:hover {
    background-color: #4A4A4A;
    border-color: #E8A87C;
    color: #E8A87C;
}
QPushButton:pressed {
    background-color: #2C2C2C;
}
QPushButton:disabled {
    background-color: #2A2A2A;
    color: #555555;
    border-color: #3C3C3C;
}

QPushButton[primary="true"] {
    background-color: #E8A87C;
    color: #1A1A1A;
    border-color: #C38D9E;
    font-weight: bold;
}
QPushButton[primary="true"]:hover {
    background-color: #F5C07A;
    border-color: #E8A87C;
}

/* === 输入框 === */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #1E1E1E;
    color: #E0D8D0;
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #E8A87C40;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #E8A87C;
}
QLineEdit:disabled, QTextEdit:disabled {
    background-color: #252526;
    color: #555555;
}

/* === 树形控件 === */
QTreeWidget {
    background-color: #2D2D2D;
    border: none;
    outline: none;
}
QTreeWidget::item {
    padding: 4px;
    border-radius: 3px;
}
QTreeWidget::item:hover {
    background-color: #3C3C3C;
}
QTreeWidget::item:selected {
    background-color: #E8A87C30;
    color: #E0D8D0;
}
QTreeWidget::branch:has-children:closed:has-children {
    background: none;
}

/* === 分组框 === */
QGroupBox {
    background-color: #2D2D2D;
    border: 1px solid #3C3C3C;
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 16px;
    font-weight: bold;
    color: #E8A87C;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
}

/* === 标签页 === */
QTabWidget::pane {
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    background-color: #2D2D2D;
}
QTabBar::tab {
    background-color: #252526;
    color: #8A8A8A;
    border: 1px solid #3C3C3C;
    border-bottom: none;
    padding: 6px 16px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background-color: #2D2D2D;
    color: #E0D8D0;
    border-color: #E8A87C;
}
QTabBar::tab:hover:!selected {
    background-color: #3C3C3C;
    color: #E0D8D0;
}

/* === 菜单 === */
QMenuBar {
    background-color: #252526;
    border-bottom: 1px solid #3C3C3C;
}
QMenuBar::item {
    padding: 6px 12px;
    color: #E0D8D0;
}
QMenuBar::item:selected {
    background-color: #3C3C3C;
}

QMenu {
    background-color: #2D2D2D;
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 3px;
    color: #E0D8D0;
}
QMenu::item:selected {
    background-color: #E8A87C30;
}
QMenu::separator {
    height: 1px;
    background-color: #3C3C3C;
    margin: 4px 0;
}
QMenu::indicator {
    width: 14px;
    height: 14px;
}

/* === 工具栏 === */
QToolBar {
    background-color: #252526;
    border-bottom: 1px solid #3C3C3C;
    spacing: 4px;
    padding: 4px;
}
QToolBar::separator {
    width: 1px;
    background-color: #3C3C3C;
    margin: 4px 6px;
}
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 4px;
    color: #8A8A8A;
}
QToolButton:hover {
    background-color: #3C3C3C;
    color: #E8A87C;
}
QToolButton:pressed {
    background-color: #2C2C2C;
}

/* === 状态栏 === */
QStatusBar {
    background-color: #252526;
    border-top: 1px solid #3C3C3C;
    color: #8A8A8A;
}
QStatusBar::section {
    background-color: transparent;
    border: none;
    padding: 0 4px;
}

/* === 消息框 === */
QMessageBox {
    background-color: #2D2D2D;
}
QMessageBox QLabel {
    color: #E0D8D0;
}
```

- [ ] **Step 5: 创建剩余空 QSS 文件占位**

创建以下空文件（后续任务会填充内容）：
- `workflow_engine/ui/styles/main_window.qss`
- `workflow_engine/ui/styles/node_panel.qss`
- `workflow_engine/ui/styles/canvas.qss`
- `workflow_engine/ui/styles/property_panel.qss`
- `workflow_engine/ui/styles/log_panel.qss`

每个文件内容：
```css
/* TODO: 由对应任务填充 */
```

- [ ] **Step 6: 修改 `workflow_engine/ui/main_window.py` 添加样式加载**

在 `_setup_ui()` 方法后添加 `_load_stylesheet()` 方法，并在 `__init__` 末尾调用它。

```python
def _load_stylesheet(self):
    """加载统一样式表"""
    from .styles import load_stylesheet
    self.setStyleSheet(load_stylesheet())
```

在 `__init__` 的 `_setup_statusbar()` 后添加：
```python
self._load_stylesheet()
```

- [ ] **Step 7: 提交**

```bash
git add workflow_engine/ui/styles/
git commit -m "feat(ui): 创建统一QSS样式表架构和基础样式文件"
```

---

## Task 2: 美化主窗口（菜单 + 工具栏 + 状态栏）

**Files:**
- 修改: `workflow_engine/ui/styles/main_window.qss`
- 修改: `workflow_engine/ui/main_window.py`

- [ ] **Step 1: 填充 `workflow_engine/ui/styles/main_window.qss`**

```css
/* main_window.qss — 主窗口专属样式 */

/* 状态栏左侧琥珀色指示条 */
QStatusBar {
    background-color: #252526;
    border-top: 1px solid #3C3C3C;
}
QStatusBar::item {
    border: none;
}

/* 工具栏图标按钮样式 */
QToolBar QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 8px;
    min-width: 56px;
}
QToolBar QToolButton:hover {
    background-color: #3C3C3C;
}
QToolBar QToolButton:on {
    background-color: #E8A87C30;
    color: #E8A87C;
}

/* 工具栏 Action 文字标签 */
QToolBar QToolButton #action_label {
    font-size: 9px;
    color: #8A8A8A;
}

/* 工具栏标题 */
QToolBar {
    background-color: #252526;
    border-bottom: 1px solid #3C3C3C;
    border-top: none;
    border-left: none;
    border-right: none;
    padding: 4px 8px;
    spacing: 6px;
}

/* 关于对话框按钮 */
QDialogButtonBox QPushButton {
    min-width: 80px;
}
```

- [ ] **Step 2: 修改 `workflow_engine/ui/main_window.py` — 工具栏添加文字标签**

修改 `_setup_toolbar` 方法，将纯 action 按钮改为带文字标签的 QToolButton：

```python
def _create_toolbar_button(self, icon, text, slot, shortcut=None, enabled=True) -> QToolButton:
    """创建带图标+文字的工具栏按钮"""
    btn = QToolButton(self)
    btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    btn.setIcon(icon)
    btn.setText(text)
    btn.setShortcut(shortcut or "")
    btn.setEnabled(enabled)
    btn.setCursor(Qt.PointingHandCursor)
    if slot:
        btn.clicked.connect(slot)
    return btn
```

将 `self.run_action = QAction(...)` 替换为 `QToolButton`：
```python
btn_run = self._create_toolbar_button(
    QIcon.fromTheme("media-playback-start", QIcon(":/icons/play.png")),
    "运行", self.on_run, "F5"
)
self.addToolBarWidget(btn_run)
```

- [ ] **Step 3: 测试运行，验证样式加载**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

预期：应用应正常启动，背景色从默认 Fusion 变为深灰 #1E1E1E。

- [ ] **Step 4: 提交**

```bash
git add workflow_engine/ui/styles/main_window.qss workflow_engine/ui/main_window.py
git commit -m "feat(ui): 美化主窗口工具栏+状态栏样式"
```

---

## Task 3: 重构节点面板为网格卡片布局

**Files:**
- 创建: `workflow_engine/ui/styles/node_panel.qss`
- 修改: `workflow_engine/ui/node_panel.py`

- [ ] **Step 1: 填充 `workflow_engine/ui/styles/node_panel.qss`**

```css
/* node_panel.qss — 节点面板网格卡片样式 */

#node_panel_container {
    background-color: #2D2D2D;
    border-right: 1px solid #3C3C3C;
}

#node_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: #E0D8D0;
    padding: 10px 12px 8px;
    border-bottom: 1px solid #3C3C3C;
    border-left: 3px solid #E8A87C;
}

/* 分类标题 */
NodeCategoryLabel {
    font-size: 11px;
    font-weight: bold;
    color: #8A8A8A;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 8px 8px 4px;
}

/* 节点卡片容器 */
NodeCardGrid {
    background-color: transparent;
    border: none;
}

/* 节点卡片 */
NodeCard {
    background-color: #252526;
    border: 1px solid #3C3C3C;
    border-radius: 6px;
    padding: 8px;
    min-width: 90px;
    max-width: 90px;
    min-height: 70px;
    max-height: 70px;
}
NodeCard:hover {
    border-color: #E8A87C;
    background-color: #2D2D2D;
}
NodeCard[node_category="input"] {
    border-left: 3px solid #4A90D9;
}
NodeCard[node_category="output"] {
    border-left: 3px solid #5CB85C;
}
NodeCard[node_category="flow"] {
    border-left: 3px solid #E8A87C;
}
NodeCard[node_category="data"] {
    border-left: 3px solid #D4A574;
}
NodeCard[node_category="ai"] {
    border-left: 3px solid #9B59B6;
}
```

- [ ] **Step 2: 重构 `workflow_engine/ui/node_panel.py` — 网格卡片布局**

将 `QTreeWidget` 树形列表改为网格布局：

```python
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QFont, QColor

# 节点分类配置
NODE_CATEGORIES = {
    "输入": {
        "color": "#4A90D9",
        "nodes": [
            ("manual_input", "手动输入"),
            ("timer_trigger", "定时触发"),
            ("file_watcher", "文件监听"),
            ("webhook", "Webhook"),
        ],
    },
    "输出": {
        "color": "#5CB85C",
        "nodes": [
            ("logger", "日志输出"),
            ("file_writer", "文件写入"),
            ("http_request", "HTTP请求"),
        ],
    },
    "流程控制": {
        "color": "#E8A87C",
        "nodes": [
            ("condition", "条件分支"),
            ("loop", "循环执行"),
            ("sub_workflow", "子流程"),
        ],
    },
    "数据处理": {
        "color": "#D4A574",
        "nodes": [
            ("transform", "数据转换"),
            ("filter", "数据过滤"),
        ],
    },
    "AI": {
        "color": "#9B59B6",
        "nodes": [
            ("agent", "AI Agent"),
            ("llm_call", "LLM调用"),
        ],
    },
}


class NodeCard(QWidget):
    """节点卡片组件"""
    clicked = Signal(str)  # 发射节点类型

    def __init__(self, node_type: str, display_name: str, category: str, accent_color: str):
        super().__init__()
        self.node_type = node_type
        self.category = category
        self.accent_color = accent_color
        self.setObjectName("NodeCard")
        self.setProperty("node_category", category)
        self.setCursor(Qt.PointingHandCursor)
        self._setup_ui(display_name)

    def _setup_ui(self, display_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel("⬡")  # 六边形占位符，后续可用真实图标
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 28px; color: {self.accent_color};")
        layout.addWidget(icon_label)

        name_label = QLabel(display_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("font-size: 10px; color: #E0D8D0; background: transparent;")
        layout.addWidget(name_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.node_type)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10, color=QColor(self.accent_color + "40"), offset=QPointF(0, 0)
        ))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)
        super().leaveEvent(event)


class NodePanel(QWidget):
    """节点面板 — 网格卡片布局"""

    node_selected = Signal(str)  # 发射选中的节点类型

    def __init__(self):
        super().__init__()
        self.setObjectName("node_panel_container")
        self._setup_ui()
        self._load_nodes()

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
                "text-transform: uppercase; letter-spacing: 1px;"
            )
            content_layout.addWidget(cat_label)

            grid = QGridLayout()
            grid.setSpacing(8)
            col = 0
            for node_type, display_name in config["nodes"]:
                card = NodeCard(node_type, display_name, category.lower(), config["color"])
                card.clicked.connect(self._on_card_clicked)
                row = col // 2
                grid.addWidget(card, row, col % 2)
                col += 1
            content_layout.addLayout(grid)

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _on_card_clicked(self, node_type: str):
        self.node_selected.emit(node_type)

    def get_selected_node_type(self) -> str:
        return ""
```

- [ ] **Step 3: 测试运行**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

预期：左侧节点面板显示为分类网格卡片，按类别有不同颜色左边框。

- [ ] **Step 4: 提交**

```bash
git add workflow_engine/ui/styles/node_panel.qss workflow_engine/ui/node_panel.py
git commit -m "feat(ui): 重构节点面板为网格卡片布局"
```

---

## Task 4: 美化画布（网格点阵背景 + 贝塞尔曲线连线）

**Files:**
- 创建: `workflow_engine/ui/styles/canvas.qss`
- 修改: `workflow_engine/ui/canvas.py`

- [ ] **Step 1: 填充 `workflow_engine/ui/styles/canvas.qss`**

```css
/* canvas.qss — 画布样式 */

WorkflowCanvas {
    background-color: #1E1E1E;
    border: none;
}
```

- [ ] **Step 2: 重构 `workflow_engine/ui/canvas.py` — 网格点阵 + 贝塞尔曲线**

用网格背景重写 `_setup背景` 方法，用 `QPainterPath` + `QPainter` 绘制贝塞尔曲线替代直线：

```python
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsPathItem
)
from PySide6.QtCore import Qt, QPointF, Signal, QRectF, QTimer
from PySide6.QtGui import (
    QPen, QBrush, QColor, QPainter, QPainterPath,
    QFont, QPolygonF, QTransform
)

# 在文件顶部添加常量
from ..styles.theme import (
    BG_PRIMARY, GRID_DOT_COLOR, GRID_DOT_SIZE, GRID_SPACING,
    NODE_INPUT, NODE_OUTPUT, NODE_FLOW, NODE_DATA, NODE_AI,
    EDGE_DEFAULT, EDGE_HOVER, EDGE_RUNNING, EDGE_SUCCESS, EDGE_ERROR,
    NODE_WIDTH, NODE_HEIGHT, NODE_RADIUS
)

# 节点类别颜色映射
NODE_COLORS = {
    "input": NODE_INPUT,
    "output": NODE_OUTPUT,
    "flow": NODE_FLOW,
    "data": NODE_DATA,
    "ai": NODE_AI,
    "default": {"primary": "#4A90D9", "secondary": "#2E6EB0"},
}
```

重写 `_setup背景` 方法为 `_draw_grid`：

```python
def _draw_grid(self, painter: QPainter, rect: QRectF):
    """绘制网格点阵背景"""
    painter.save()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
    painter.setBrush(QBrush(QColor(BG_PRIMARY)))
    painter.setPen(Qt.NoPen)
    painter.drawRect(self.sceneRect())

    painter.setBrush(QBrush(QColor(GRID_DOT_COLOR)))
    painter.setPen(Qt.NoPen)
    dot_size = GRID_DOT_SIZE
    spacing = GRID_SPACING

    view_rect = self.viewport().rect()
    top_left = self.mapToScene(0, 0)
    bottom_right = self.mapToScene(view_rect.width(), view_rect.height())

    x_start = int(top_left.x() // spacing) * spacing
    y_start = int(top_left.y() // spacing) * spacing

    for x in range(int(x_start), int(bottom_right.x()) + spacing, spacing):
        for y in range(int(y_start), int(bottom_right.y()) + spacing, spacing):
            painter.drawEllipse(x - dot_size/2, y - dot_size/2, dot_size, dot_size)
    painter.restore()
```

重写 `drawBackground` 方法：

```python
def drawBackground(self, painter: QPainter, rect: QRectF):
    self._draw_grid(painter, rect)
```

重写 `EdgeGraphicsItem.__init__` 使用贝塞尔曲线：

```python
class EdgeGraphicsItem(QGraphicsPathItem):
    """贝塞尔曲线连线"""

    def __init__(self, source_item: NodeGraphicsItem, target_item: NodeGraphicsItem):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.edge_state = "default"
        self.setZValue(-1)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self._update_path()

    def _update_path(self):
        """计算贝塞尔曲线路径"""
        sp = self._output_port_pos()
        tp = self._input_port_pos()

        dx = tp.x() - sp.x()
        ctrl_offset = max(abs(dx) * 0.5, 50)

        path = QPainterPath()
        path.moveTo(sp)
        path.cubicTo(
            QPointF(sp.x() + ctrl_offset, sp.y()),
            QPointF(tp.x() - ctrl_offset, tp.y()),
            tp
        )
        self.setPath(path)

    def _output_port_pos(self) -> QPointF:
        item = self.source_item
        return QPointF(
            item.scenePos().x() + NODE_WIDTH,
            item.scenePos().y() + NODE_HEIGHT / 2
        )

    def _input_port_pos(self) -> QPointF:
        item = self.target_item
        return QPointF(
            item.scenePos().x(),
            item.scenePos().y() + NODE_HEIGHT / 2
        )

    def update_position(self):
        self._update_path()
```

同时更新 `NodeGraphicsItem` 的 `setPos` 方法，在节点移动时触发连线更新：

```python
def setPos(self, x: float, y: float):
    super().setPos(x, y)
    # 通知所有连线更新
    for edge in self.scene().findChildren(EdgeGraphicsItem):
        if edge.source_item == self or edge.target_item == self:
            edge.update_position()
```

- [ ] **Step 3: 测试运行**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

预期：画布背景显示点阵网格，连线变为光滑的贝塞尔曲线。

- [ ] **Step 4: 提交**

```bash
git add workflow_engine/ui/styles/canvas.qss workflow_engine/ui/canvas.py
git commit -m "feat(ui): 画布添加网格点阵背景和贝塞尔曲线连线"
```

---

## Task 5: 美化节点样式 + 呼吸脉冲动画

**Files:**
- 修改: `workflow_engine/ui/canvas.py`

- [ ] **Step 1: 重构 `NodeGraphicsItem` — 圆角卡片 + 选中发光 + 状态管理**

```python
class NodeGraphicsItem(QGraphicsRectItem):
    """美化版节点图形项 — 圆角卡片 + 发光效果"""

    def __init__(self, node_id: str, node_type: str, display_name: str = "",
                 category: str = "default", width: float = NODE_WIDTH, height: float = NODE_HEIGHT):
        super().__init__(0, 0, width, height)
        self.node_id = node_id
        self.node_type = node_type
        self.category = category
        self.node_state = "idle"  # idle / running / success / error

        colors = NODE_COLORS.get(category, NODE_COLORS["default"])
        self.primary_color = colors["primary"]
        self.secondary_color = colors["secondary"]

        # 圆角矩形
        self.setBrush(QBrush(QColor(self.primary_color)))
        self.setPen(QPen(QColor(self.secondary_color), 1))
        self.setCornerRadius(QPointF(NODE_RADIUS, NODE_RADIUS))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)

        # 文字
        text = QGraphicsTextItem(self)
        text.setPlainText(display_name or node_type)
        text.setDefaultTextColor(QColor("#E0D8D0"))
        text.setFont(QFont("Segoe UI", 10, QFont.Bold))
        text.setPos(12, height / 2 - 10)

        # 类型标签
        type_label = QGraphicsTextItem(self)
        type_label.setPlainText(f"[{category}]")
        type_label.setDefaultTextColor(QColor("#E0D8D0" + "80"))
        type_label.setFont(QFont("Segoe UI", 7))
        type_label.setPos(12, height / 2 + 6)

        # 端口
        port_y = height / 2
        self.input_port = QGraphicsEllipseItem(-NODE_PORT_RADIUS, port_y - NODE_PORT_RADIUS,
                                                NODE_PORT_RADIUS * 2, NODE_PORT_RADIUS * 2, self)
        self.input_port.setBrush(QBrush(QColor("#5CB85C")))
        self.input_port.setPen(QPen(QColor("#3D8B3D"), 1))
        self.input_port.setFlag(QGraphicsItem.ItemIsSelectable, False)

        self.output_port = QGraphicsEllipseItem(width - NODE_PORT_RADIUS, port_y - NODE_PORT_RADIUS,
                                                 NODE_PORT_RADIUS * 2, NODE_PORT_RADIUS * 2, self)
        self.output_port.setBrush(QBrush(QColor("#E74C3C")))
        self.output_port.setPen(QPen(QColor("#C0392B"), 1))
        self.output_port.setFlag(QGraphicsItem.ItemIsSelectable, False)

        # 发光效果
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(0)
        self.glow_effect.setColor(QColor(self.primary_color + "00"))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)

    def set_state(self, state: str):
        """设置节点执行状态：idle / running / success / error"""
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
            self.glow_effect.setColor(QColor("#5CB85C60"))
            self.setPen(QPen(QColor("#5CB85C"), 2))
        elif state == "error":
            self._stop_pulse()
            self.glow_effect.setBlurRadius(15)
            self.glow_effect.setColor(QColor("#E74C3C60"))
            self.setPen(QPen(QColor("#E74C3C"), 2))

    def _start_pulse(self):
        """启动呼吸脉冲动画"""
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_step)
        self._pulse_timer.start(50)
        self._pulse_phase = 0.0

    def _stop_pulse(self):
        """停止脉冲动画"""
        if hasattr(self, "_pulse_timer"):
            self._pulse_timer.stop()

    def _pulse_step(self):
        """脉冲动画一步"""
        import math
        self._pulse_phase += 0.1
        glow = int(15 + 15 * math.sin(self._pulse_phase))
        self.glow_effect.setBlurRadius(glow)
        # 边框在主色和暖黄之间脉冲
        r1, g1, b1 = self._hex_to_rgb(self.secondary_color)
        r2, g2, b2 = (245, 192, 122)  # #F5C07A
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
            self.setPen(QPen(QColor("#E8A87C"), 2))
            self.glow_effect.setBlurRadius(10)
            self.glow_effect.setColor(QColor("#E8A87C40"))
        else:
            self.set_state(self.node_state)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor("#E8A87C"), 1))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.set_selected(self.isSelected())
        super().hoverLeaveEvent(event)
```

- [ ] **Step 2: 更新 `add_node` 方法支持 category**

```python
def add_node(self, node_id: str, node_type: str, x: float, y: float,
             display_name: str = "", category: str = "default") -> NodeGraphicsItem:
    if node_id in self._node_items:
        return self._node_items[node_id]
    item = NodeGraphicsItem(node_id, node_type, display_name, category)
    item.setPos(x, y)
    self.scene.addItem(item)
    self._node_items[node_id] = item
    # 连接移动信号以更新连线
    item.yChanged.connect(lambda: self._on_node_moved(node_id))
    item.xChanged.connect(lambda: self._on_node_moved(node_id))
    return item

def _on_node_moved(self, node_id: str):
    for edge in self._edge_items:
        if edge.source_item.node_id == node_id or edge.target_item.node_id == node_id:
            edge.update_position()
```

- [ ] **Step 3: 测试运行**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

预期：节点显示圆角卡片 + 类别颜色，有选中发光效果。后续 Task 6 连接引擎后可测试呼吸脉冲。

- [ ] **Step 4: 提交**

```bash
git add workflow_engine/ui/canvas.py
git commit -m "feat(ui): 美化节点样式，添加圆角+发光+呼吸脉冲动画"
```

---

## Task 6: 美化属性面板 + 日志面板

**Files:**
- 创建: `workflow_engine/ui/styles/property_panel.qss`
- 创建: `workflow_engine/ui/styles/log_panel.qss`
- 修改: `workflow_engine/ui/property_panel.py`（可选小调整）
- 修改: `workflow_engine/ui/log_panel.py`（可选小调整）

- [ ] **Step 1: 填充 `workflow_engine/ui/styles/property_panel.qss`**

```css
/* property_panel.qss — 属性面板样式 */

#property_panel_container {
    background-color: #2D2D2D;
    border-left: 1px solid #3C3C3C;
}

#property_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: #E0D8D0;
    padding: 10px 12px 8px;
    border-bottom: 1px solid #3C3C3C;
    border-left: 3px solid #E8A87C;
}

#property_empty_label {
    color: #8A8A8A;
    padding: 20px;
    alignment: center;
}
```

- [ ] **Step 2: 填充 `workflow_engine/ui/styles/log_panel.qss`**

```css
/* log_panel.qss — 日志面板样式 */

#log_panel_container {
    background-color: #1E1E1E;
    border-top: 1px solid #3C3C3C;
}

#log_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: #E0D8D0;
    padding: 8px 12px;
    border-bottom: 1px solid #3C3C3C;
    border-left: 3px solid #E8A87C;
}
```

- [ ] **Step 3: 给属性/日志面板添加 objectName 以便 QSS 匹配**

在 `property_panel.py` 的 `__init__` 开始处添加：
```python
self.setObjectName("property_panel_container")
```

在 `log_panel.py` 的 `__init__` 开始处添加：
```python
self.setObjectName("log_panel_container")
```

给两个面板的标题 QLabel 也添加 objectName：
```python
title.setObjectName("property_panel_title")  # property_panel.py
title.setObjectName("log_panel_title")       # log_panel.py
```

- [ ] **Step 4: 测试运行**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

预期：右侧属性面板和底部日志面板配色统一，左侧有琥珀色装饰条。

- [ ] **Step 5: 提交**

```bash
git add workflow_engine/ui/styles/property_panel.qss workflow_engine/ui/styles/log_panel.qss
git add workflow_engine/ui/property_panel.py workflow_engine/ui/log_panel.py
git commit -m "feat(ui): 美化属性面板和日志面板样式"
```

---

## Task 7: 右键上下文菜单美化 + 最终整合测试

**Files:**
- 修改: `workflow_engine/ui/canvas.py`（添加右键菜单）
- 创建: `workflow_engine/ui/styles/context_menu.qss`（合并到 components.qss）

- [ ] **Step 1: 在 `canvas.py` 的 `WorkflowCanvas` 中添加右键菜单**

```python
from PySide6.QtWidgets import QMenu

def __init__(self):
    # ... 现有代码 ...
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
            color: #E0D8D0;
        }
        QMenu::item:selected {
            background-color: #E8A87C30;
        }
        QMenu::separator {
            height: 1px;
            background-color: #3C3C3C;
            margin: 4px 0;
        }
    """)
    delete_action = menu.addAction("删除节点 (Del)")
    run_action = menu.addAction("运行此节点")
    menu.addSeparator()
    clear_action = menu.addAction("清空画布")

    action = menu.exec(self.mapToGlobal(pos))
    if action == delete_action and self._selected_node_id:
        self.remove_node(self._selected_node_id)
        self._selected_node_id = None
    elif action == clear_action:
        self.clear()
```

- [ ] **Step 2: 最终整合测试**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

验证清单：
- [ ] 主窗口背景为深灰 #1E1E1E
- [ ] 左侧节点面板为网格卡片，按类别有不同颜色左边框
- [ ] 中间画布有点阵网格背景
- [ ] 画布上节点为圆角卡片，选中有琥珀色发光
- [ ] 节点连线为光滑贝塞尔曲线
- [ ] 右侧属性面板有琥珀色装饰条
- [ ] 底部日志面板为深色终端风格
- [ ] 工具栏按钮有图标+文字

- [ ] **Step 3: 提交**

```bash
git add workflow_engine/ui/canvas.py
git commit -m "feat(ui): 添加右键上下文菜单，完成全套UI美化"
```

---

## 验收清单 (Checklist)

- [ ] Task 1: 样式基础设施 — `theme.py`、QSS 文件加载入口正常
- [ ] Task 1: 基础样式 — 全局背景色、滚动条、按钮、输入框样式统一
- [ ] Task 2: 主窗口 — 工具栏图标+文字、状态栏样式
- [ ] Task 3: 节点面板 — 分类网格卡片、悬停效果、左侧颜色边框
- [ ] Task 4: 画布背景 — 网格点阵正常显示
- [ ] Task 4: 贝塞尔曲线 — 连线变为光滑曲线
- [ ] Task 5: 节点样式 — 圆角卡片、类别颜色、选中发光
- [ ] Task 5: 呼吸动画 — 运行时节点脉冲效果
- [ ] Task 6: 属性面板 — 统一配色+装饰条
- [ ] Task 6: 日志面板 — 统一配色+装饰条
- [ ] Task 7: 右键菜单 — 深色上下文菜单
- [ ] 整体 — 应用正常启动，所有面板正常显示，无崩溃
