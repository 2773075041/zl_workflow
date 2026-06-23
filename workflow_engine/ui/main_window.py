import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMessageBox, QToolButton, QSizePolicy,
    QScrollArea, QSplitter
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    """工作流引擎主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("工作流引擎")
        self.resize(1280, 800)
        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_statusbar()
        self._load_stylesheet()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        from .node_panel import NodePanel
        from .canvas import WorkflowCanvas
        from .property_panel import PropertyPanel
        from .log_panel import LogPanel

        self.node_panel = NodePanel()
        self.canvas = WorkflowCanvas()
        self.canvas.node_double_clicked.connect(self._on_node_double_clicked)
        self.property_panel = PropertyPanel()
        self.log_panel = LogPanel()

        # 上部三栏布局
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.node_panel, 1)
        top_layout.addWidget(self.canvas, 4)
        top_layout.addWidget(self.property_panel, 1)

        # 日志开关按钮
        self.log_toggle_btn = QToolButton()
        self.log_toggle_btn.setText("📜 执行日志")
        self.log_toggle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.log_toggle_btn.setArrowType(Qt.ArrowType.DownArrow)
        self.log_toggle_btn.setCheckable(True)
        self.log_toggle_btn.setChecked(False)
        self.log_toggle_btn.clicked.connect(self._toggle_log_panel)
        self.log_toggle_btn.setStyleSheet(
            "border: none; padding: 6px 12px; font-size: 11px; color: #8A8A8A;"
            "background: transparent;"
        )
        self.log_toggle_btn.setCursor(Qt.PointingHandCursor)

        log_header = QWidget()
        log_header.setStyleSheet("background-color: #252526; border-top: 1px solid #3C3C3C;")
        log_header_layout = QHBoxLayout(log_header)
        log_header_layout.setContentsMargins(0, 0, 0, 0)
        log_header_layout.addWidget(self.log_toggle_btn)
        log_header_layout.addStretch()

        # 日志面板默认收起
        self._log_expanded = False
        self.log_panel.setMaximumHeight(0)
        self.log_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # 底部容器（日志开关 + 日志面板）
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(log_header)
        bottom_layout.addWidget(self.log_panel)

        # 垂直分割器：上部内容 + 底部日志（只和内容区同宽）
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(2)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setStretchFactor(0, 1)  # 上部可拉伸
        splitter.setStretchFactor(1, 0)  # 底部不拉伸

        top_container = QWidget()
        top_container.setLayout(top_layout)
        splitter.addWidget(top_container)
        splitter.addWidget(bottom_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(splitter)

    def _toggle_log_panel(self, checked: bool):
        """展开/收起日志面板"""
        self._log_expanded = checked
        if checked:
            self.log_panel.setMaximumHeight(200)
            self.log_toggle_btn.setArrowType(Qt.ArrowType.UpArrow)
            self.log_toggle_btn.setText("📜 收起日志")
        else:
            self.log_panel.setMaximumHeight(0)
            self.log_toggle_btn.setArrowType(Qt.ArrowType.DownArrow)
            self.log_toggle_btn.setText("📜 执行日志")

    def _setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件")
        new_action = QAction("新建工作流", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_new_workflow)
        file_menu.addAction(new_action)

        open_action = QAction("打开工作流", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open_workflow)
        file_menu.addAction(open_action)

        save_action = QAction("保存工作流", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_save_workflow)
        file_menu.addAction(save_action)

        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("编辑")
        run_menu = menubar.addMenu("运行")
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)

    def _create_toolbar_button(self, icon_char: str, text: str, slot=None, shortcut: str = "", enabled: bool = True) -> QToolButton:
        """创建带文字标签的工具栏按钮"""
        btn = QToolButton(self)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setText(text)
        btn.setShortcut(shortcut)
        btn.setEnabled(enabled)
        btn.setCursor(Qt.PointingHandCursor)
        # 使用字体符号作为图标替代（避免依赖外部图标资源）
        btn.setStyleSheet("font-size: 16px;")
        if slot:
            btn.clicked.connect(slot)
        return btn

    def _setup_toolbar(self):
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(12, 12))
        self.addToolBar(toolbar)

        # 使用内联样式替代图标
        btn_run = self._create_toolbar_button("▶", "运行", self.on_run, "F5", True)
        toolbar.addWidget(btn_run)

        btn_pause = self._create_toolbar_button("⏸", "暂停", None, "", False)
        toolbar.addWidget(btn_pause)
        self._pause_btn = btn_pause

        btn_stop = self._create_toolbar_button("⏹", "停止", None, "", False)
        toolbar.addWidget(btn_stop)
        self._stop_btn = btn_stop

        toolbar.addSeparator()

        btn_step = self._create_toolbar_button("⏭", "单步", self.on_step, "", True)
        toolbar.addWidget(btn_step)

        btn_reset = self._create_toolbar_button("🔄", "重置", self.on_reset, "", True)
        toolbar.addWidget(btn_reset)

    def _setup_statusbar(self):
        self.statusBar().showMessage("就绪")
        self.statusBar().setStyleSheet(
            "QStatusBar { background-color: #007ACC; color: #FFFFFF; font-weight: bold; }"
        )

    def _load_stylesheet(self):
        from .styles import get_theme
        theme = get_theme()
        stylesheet = theme.get_stylesheet()
        self.setStyleSheet(stylesheet)

    def on_new_workflow(self):
        self.log_panel.info("新建工作流")

    def on_open_workflow(self):
        self.log_panel.info("打开工作流")

    def on_save_workflow(self):
        self.log_panel.info("保存工作流")

    def on_run(self):
        self.log_panel.info("开始运行工作流")
        self.statusBar().showMessage("运行中...")
        if hasattr(self, '_pause_btn'):
            self._pause_btn.setEnabled(True)
        if hasattr(self, '_stop_btn'):
            self._stop_btn.setEnabled(True)

    def on_step(self):
        self.log_panel.info("单步执行")

    def on_reset(self):
        self.log_panel.info("重置工作流")
        self.statusBar().showMessage("就绪")

    def on_about(self):
        QMessageBox.about(self, "关于工作流引擎", "工作流引擎 v1.0\n\n一个可视化工作流节点框架")

    def _on_node_double_clicked(self, node_id: str):
        item = self.canvas._node_items.get(node_id)
        if not item:
            return
        self.property_panel.set_node(
            node_id=node_id,
            node_type=item.node_type,
            display_name=item.display_name,
            config={}
        )