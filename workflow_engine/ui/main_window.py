import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMessageBox
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
        main_layout = QHBoxLayout(central_widget)

        from .node_panel import NodePanel
        from .canvas import WorkflowCanvas
        from .property_panel import PropertyPanel
        from .log_panel import LogPanel

        self.node_panel = NodePanel()
        self.canvas = WorkflowCanvas()
        self.property_panel = PropertyPanel()
        self.log_panel = LogPanel()

        main_layout.addWidget(self.node_panel, 1)
        main_layout.addWidget(self.canvas, 4)
        main_layout.addWidget(self.property_panel, 1)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.addWidget(self.log_panel)
        main_layout.addWidget(bottom_widget, 1)

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

    def _setup_toolbar(self):
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        self.run_action = QAction("▶ 运行", self)
        self.run_action.setShortcut("F5")
        self.run_action.triggered.connect(self.on_run)
        toolbar.addAction(self.run_action)

        self.pause_action = QAction("⏸ 暂停", self)
        self.pause_action.setEnabled(False)
        toolbar.addAction(self.pause_action)

        self.stop_action = QAction("⏹ 停止", self)
        self.stop_action.setEnabled(False)
        toolbar.addAction(self.stop_action)

        toolbar.addSeparator()

        self.step_action = QAction("⏭ 单步", self)
        self.step_action.triggered.connect(self.on_step)
        toolbar.addAction(self.step_action)

        self.reset_action = QAction("🔄 重置", self)
        self.reset_action.triggered.connect(self.on_reset)
        toolbar.addAction(self.reset_action)

    def _setup_statusbar(self):
        self.statusBar().showMessage("就绪")

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

    def on_step(self):
        self.log_panel.info("单步执行")

    def on_reset(self):
        self.log_panel.info("重置工作流")
        self.statusBar().showMessage("就绪")

    def on_about(self):
        QMessageBox.about(self, "关于工作流引擎", "工作流引擎 v1.0\n\n一个可视化工作流节点框架")