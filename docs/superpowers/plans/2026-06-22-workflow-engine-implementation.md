# 工作流引擎 (WorkflowEngine) 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标:** 构建一个PC端可视化工作流节点框架，支持拖拽、连线、配置节点，节点继承式扩展，手动/定时/触发三种执行模式

**架构:** 分层模块化设计：可视化界面层(PyQt/PySide) → 核心引擎层 → 节点扩展层 → 存储层(JSON+SQLite)

**技术栈:** PySide6, Python 3.10+, json, sqlite3, APScheduler

---

## 项目结构

```
workflow_engine/
├── core/                      # 核心引擎
│   ├── __init__.py
│   ├── workflow.py            # 工作流主类
│   ├── engine.py              # 工作流引擎
│   ├── executor.py            # 执行器
│   ├── scheduler.py           # 调度器
│   ├── variable_store.py      # 变量系统
│   └── node_registry.py       # 节点注册表
├── nodes/                     # 节点定义
│   ├── __init__.py
│   ├── base.py                # 节点基类
│   ├── input/                 # 输入节点
│   │   ├── __init__.py
│   │   ├── manual_input.py    # 手动输入
│   │   ├── timer_trigger.py   # 定时触发
│   │   └── file_watcher.py    # 文件监听
│   ├── output/                # 输出节点
│   │   ├── __init__.py
│   │   ├── logger.py          # 日志输出
│   │   └── file_writer.py     # 文件写入
│   ├── flow/                  # 流程控制
│   │   ├── __init__.py
│   │   ├── condition.py       # 条件分支
│   │   ├── loop.py            # 循环
│   │   └── sub_workflow.py    # 子流程
│   └── ai/                    # AI节点
│       ├── __init__.py
│       ├── agent.py           # Agent节点
│       └── llm_call.py        # LLM调用
├── ui/                        # 可视化界面
│   ├── __init__.py
│   ├── main_window.py         # 主窗口
│   ├── node_panel.py          # 节点面板
│   ├── canvas.py              # 画布
│   ├── property_panel.py      # 属性面板
│   └── log_panel.py           # 日志面板
├── storage/                   # 存储层
│   ├── __init__.py
│   ├── workflow_storage.py    # 工作流存储
│   └── history_storage.py     # 历史记录
├── utils/                     # 工具函数
│   └── __init__.py
└── main.py                    # 程序入口
```

---

## 实施任务

### Phase 1: 核心框架

#### Task 1: 创建项目脚手架和目录结构

**Files:**
- Create: `workflow_engine/core/__init__.py`
- Create: `workflow_engine/nodes/__init__.py`
- Create: `workflow_engine/nodes/input/__init__.py`
- Create: `workflow_engine/nodes/output/__init__.py`
- Create: `workflow_engine/nodes/flow/__init__.py`
- Create: `workflow_engine/nodes/ai/__init__.py`
- Create: `workflow_engine/ui/__init__.py`
- Create: `workflow_engine/storage/__init__.py`
- Create: `workflow_engine/utils/__init__.py`
- Create: `workflow_engine/main.py`
- Create: `requirements.txt` (PySide6>=6.5, APScheduler>=3.10)

- [ ] **Step 1: 创建目录结构和空__init__.py文件**
- [ ] **Step 2: 创建requirements.txt**
- [ ] **Step 3: 提交初始项目结构**

```bash
git add -A && git commit -m "feat: 创建项目脚手架和目录结构"
```

---

#### Task 2: 实现变量系统 (VariableStore)

**Files:**
- Create: `workflow_engine/core/variable_store.py`
- Create: `tests/core/test_variable_store.py`

- [ ] **Step 1: 编写变量系统测试**

```python
# tests/core/test_variable_store.py
import pytest
from workflow_engine.core.variable_store import VariableStore

def test_set_and_get():
    store = VariableStore()
    store.set("name", "test")
    assert store.get("name") == "test"

def test_get_default():
    store = VariableStore()
    assert store.get("nonexistent", "default") == "default"

def test_typed_variables():
    store = VariableStore()
    store.set("count", 10, int)
    assert store.get_type("count") == int
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/core/test_variable_store.py -v`
Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现VariableStore类**

```python
# workflow_engine/core/variable_store.py
from typing import Any, Dict, Optional, type

class VariableStore:
    """工作流级变量存储"""

    def __init__(self):
        self._variables: Dict[str, Any] = {}
        self._types: Dict[str, type] = {}

    def set(self, key: str, value: Any, vtype: Optional[type] = None):
        self._variables[key] = value
        if vtype:
            self._types[key] = vtype

    def get(self, key: str, default: Any = None) -> Any:
        return self._variables.get(key, default)

    def get_type(self, key: str) -> type:
        return self._types.get(key, type(self._variables.get(key)))

    def has(self, key: str) -> bool:
        return key in self._variables

    def remove(self, key: str):
        self._variables.pop(key, None)
        self._types.pop(key, None)

    def clear(self):
        self._variables.clear()
        self._types.clear()

    def to_dict(self) -> Dict:
        return {"variables": self._variables, "types": {k: v.__name__ for k, v in self._types.items()}}

    @classmethod
    def from_dict(cls, data: Dict) -> "VariableStore":
        store = cls()
        store._variables = data.get("variables", {})
        return store
```

- [ ] **Step 4: 运行测试验证通过**

Run: `pytest tests/core/test_variable_store.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add tests/core/test_variable_store.py workflow_engine/core/variable_store.py
git commit -m "feat(core): 实现变量系统 VariableStore"
```

---

#### Task 3: 实现节点注册表 (NodeRegistry)

**Files:**
- Create: `workflow_engine/core/node_registry.py`
- Create: `tests/core/test_node_registry.py`

- [ ] **Step 1: 编写节点注册表测试**

```python
# tests/core/test_node_registry.py
import pytest
from workflow_engine.core.node_registry import NodeRegistry, BaseNode

class TestNode(BaseNode):
    node_type = "test"
    display_name = "测试节点"

registry = NodeRegistry()

def test_register_node():
    registry.register(TestNode)
    assert "test" in registry.get_all_types()

def test_get_node_class():
    registry.register(TestNode)
    assert registry.get_node_class("test") == TestNode

def test_get_nodes_by_category():
    TestNode.category = "测试"
    registry.register(TestNode)
    assert "测试" in registry.get_categories()
```

- [ ] **Step 2: 运行测试验证失败**
- [ ] **Step 3: 实现NodeRegistry类**
- [ ] **Step 4: 运行测试验证通过**
- [ ] **Step 5: 提交**

---

#### Task 4: 实现节点基类 (BaseNode)

**Files:**
- Create: `workflow_engine/nodes/base.py`

- [ ] **Step 1: 实现BaseNode基类**

```python
# workflow_engine/nodes/base.py
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from workflow_engine.core.workflow import Workflow

class BaseNode(ABC):
    """所有节点的基类"""

    category: str = "基础"
    display_name: str = "节点"
    node_type: str = "base"
    input_ports: List[tuple] = []
    output_ports: List[tuple] = []
    config_schema: Dict = {}

    def __init__(self, node_id: str, workflow: "Workflow"):
        self.node_id = node_id
        self.workflow = workflow
        self.variables = workflow.variables
        self.config: Dict = {}
        self._state = "pending"

    @abstractmethod
    def execute(self, inputs: Dict) -> Dict:
        """节点执行逻辑，子类必须实现"""
        raise NotImplementedError

    def validate(self) -> bool:
        """节点配置校验"""
        return True

    def set_config(self, config: Dict):
        self.config = config

    def get_state(self) -> str:
        return self._state

    def set_state(self, state: str):
        self._state = state

    @property
    def inputs(self) -> List[str]:
        return [port[0] for port in self.input_ports]

    @property
    def outputs(self) -> List[str]:
        return [port[0] for port in self.output_ports]
```

- [ ] **Step 2: 提交**

```bash
git add workflow_engine/nodes/base.py
git commit -m "feat(nodes): 实现节点基类 BaseNode"
```

---

#### Task 5: 实现工作流主类 (Workflow)

**Files:**
- Create: `workflow_engine/core/workflow.py`
- Create: `tests/core/test_workflow.py`

- [ ] **Step 1: 实现Workflow类**

```python
# workflow_engine/core/workflow.py
from typing import Dict, List, Optional, Any
from uuid import uuid4
from .variable_store import VariableStore
from .node_registry import NodeRegistry

class Workflow:
    def __init__(self, workflow_id: Optional[str] = None, name: str = "未命名工作流"):
        self.id = workflow_id or str(uuid4())
        self.name = name
        self.nodes: Dict[str, BaseNode] = {}
        self.edges: List[Dict] = []
        self.variables = VariableStore()
        self._registry = NodeRegistry()

    def add_node(self, node_type: str, node_id: Optional[str] = None, position: Dict = None) -> BaseNode:
        node_id = node_id or f"{node_type}_{len(self.nodes)}"
        node_class = self._registry.get_node_class(node_type)
        node = node_class(node_id, self)
        node.position = position or {"x": 0, "y": 0}
        self.nodes[node_id] = node
        return node

    def remove_node(self, node_id: str):
        self.nodes.pop(node_id, None)
        self.edges = [e for e in self.edges if e["source"] != node_id and e["target"] != node_id]

    def add_edge(self, source: str, target: str, source_port: str = "output", target_port: str = "input"):
        self.edges.append({
            "source": source,
            "target": target,
            "source_port": source_port,
            "target_port": target_port
        })

    def remove_edge(self, source: str, target: str):
        self.edges = [e for e in self.edges if not (e["source"] == source and e["target"] == target)]

    def get_node(self, node_id: str) -> Optional[BaseNode]:
        return self.nodes.get(node_id)

    def get_outgoing_edges(self, node_id: str) -> List[Dict]:
        return [e for e in self.edges if e["source"] == node_id]

    def get_incoming_edges(self, node_id: str) -> List[Dict]:
        return [e for e in self.edges if e["target"] == node_id]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "nodes": [
                {
                    "id": node_id,
                    "type": node.node_type,
                    "category": node.category,
                    "position": getattr(node, "position", {"x": 0, "y": 0}),
                    "config": node.config
                }
                for node_id, node in self.nodes.items()
            ],
            "edges": self.edges,
            "variables": self.variables.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Workflow":
        workflow = cls(workflow_id=data["id"], name=data["name"])
        workflow.edges = data.get("edges", [])
        for node_data in data.get("nodes", []):
            node = workflow.add_node(node_data["type"], node_data["id"], node_data.get("position"))
            node.set_config(node_data.get("config", {}))
        workflow.variables = VariableStore.from_dict(data.get("variables", {}))
        return workflow
```

- [ ] **Step 2: 编写并运行测试**
- [ ] **Step 3: 提交**

---

#### Task 6: 实现执行器 (Executor)

**Files:**
- Create: `workflow_engine/core/executor.py`
- Create: `tests/core/test_executor.py`

- [ ] **Step 1: 实现Executor类**

```python
# workflow_engine/core/executor.py
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from .workflow import Workflow

class ExecutionState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Executor:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.state = ExecutionState.IDLE
        self.current_node_id: Optional[str] = None
        self.node_results: Dict[str, Any] = {}
        self.error: Optional[Exception] = None
        self._step_callbacks: List[Callable] = []

    def on_step(self, callback: Callable):
        self._step_callbacks.append(callback)

    def execute(self, mode: str = "sequential") -> Dict:
        self.state = ExecutionState.RUNNING
        self.node_results = {}
        self.error = None

        try:
            if mode == "sequential":
                result = self._execute_sequential()
            elif mode == "parallel":
                result = self._execute_parallel()
            else:
                raise ValueError(f"Unknown mode: {mode}")
            self.state = ExecutionState.COMPLETED
            return result
        except Exception as e:
            self.state = ExecutionState.FAILED
            self.error = e
            raise

    def _execute_sequential(self) -> Dict:
        order = self._topological_sort()
        for node_id in order:
            self.current_node_id = node_id
            node = self.workflow.get_node(node_id)
            if not node:
                continue
            node.set_state("running")
            inputs = self._gather_inputs(node_id)
            result = node.execute(inputs)
            self.node_results[node_id] = result
            node.set_state("completed")
            for cb in self._step_callbacks:
                cb(node_id, result)
        return self.node_results

    def _topological_sort(self) -> List[str]:
        visited = set()
        result = []

        def visit(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            for edge in self.workflow.get_outgoing_edges(node_id):
                visit(edge["target"])
            result.append(node_id)

        for node_id in self.workflow.nodes:
            visit(node_id)
        return result

    def _gather_inputs(self, node_id: str) -> Dict:
        inputs = {}
        for edge in self.workflow.get_incoming_edges(node_id):
            source_result = self.node_results.get(edge["source"], {})
            inputs[edge["source_port"]] = source_result
        return inputs

    def step(self) -> bool:
        if self.state == ExecutionState.IDLE:
            order = self._topological_sort()
            if order:
                self.current_node_id = order[0]
                self.state = ExecutionState.RUNNING
        elif self.current_node_id:
            order = self._topological_sort()
            current_idx = order.index(self.current_node_id) if self.current_node_id in order else -1
            if current_idx < len(order) - 1:
                self.current_node_id = order[current_idx + 1]
            else:
                self.state = ExecutionState.COMPLETED
                return False
        return True

    def get_status(self) -> Dict:
        return {
            "state": self.state.value,
            "current_node": self.current_node_id,
            "completed_nodes": list(self.node_results.keys()),
            "error": str(self.error) if self.error else None
        }
```

- [ ] **Step 2: 提交**

---

#### Task 7: 实现工作流引擎 (WorkflowEngine)

**Files:**
- Create: `workflow_engine/core/engine.py`

- [ ] **Step 1: 实现WorkflowEngine类**

```python
# workflow_engine/core/engine.py
from typing import Dict, Optional
from .workflow import Workflow
from .executor import Executor, ExecutionState

class WorkflowEngine:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.active_executors: Dict[str, Executor] = {}

    def add_workflow(self, workflow: Workflow):
        self.workflows[workflow.id] = workflow

    def remove_workflow(self, workflow_id: str):
        self.workflows.pop(workflow_id, None)

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)

    def run_workflow(self, workflow_id: str, mode: str = "sequential") -> Dict:
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        executor = Executor(workflow)
        self.active_executors[workflow_id] = executor
        return executor.execute(mode)

    def pause_workflow(self, workflow_id: str):
        executor = self.active_executors.get(workflow_id)
        if executor:
            executor.state = ExecutionState.PAUSED

    def stop_workflow(self, workflow_id: str):
        executor = self.active_executors.get(workflow_id)
        if executor:
            executor.state = ExecutionState.IDLE

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        executor = self.active_executors.get(workflow_id)
        return executor.get_status() if executor else None
```

- [ ] **Step 2: 提交**

---

### Phase 2: 可视化界面

#### Task 8: 实现主窗口 (MainWindow)

**Files:**
- Create: `workflow_engine/ui/main_window.py`

- [ ] **Step 1: 实现PySide6主窗口框架**

```python
# workflow_engine/ui/main_window.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("工作流引擎")
        self.resize(1280, 800)
        self._setup_ui()

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
        bottom_layout.addWidget(self.log_panel, 1)
        main_layout.addWidget(bottom_widget, 1)

        self._setup_toolbar()

    def _setup_toolbar(self):
        from PySide6.QtGui import QAction
        from PySide6.QtCore import SIGNAL

        self.run_action = QAction("▶ 运行", self)
        self.step_action = QAction("⏭ 单步", self)
        self.stop_action = QAction("⏹ 停止", self)

        toolbar = self.addToolBar("主工具栏")
        toolbar.addAction(self.run_action)
        toolbar.addAction(self.step_action)
        toolbar.addAction(self.stop_action)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 提交**

---

#### Task 9: 实现节点面板 (NodePanel)

**Files:**
- Create: `workflow_engine/ui/node_panel.py`

- [ ] **Step 1: 实现节点面板**

```python
# workflow_engine/ui/node_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt, Signal

class NodePanel(QWidget):
    node_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_nodes()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("节点面板")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.node_list = QListWidget()
        self.node_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.node_list)

    def _load_nodes(self):
        categories = {
            "输入": ["manual_input", "timer_trigger", "file_watcher"],
            "输出": ["logger", "file_writer"],
            "流程控制": ["condition", "loop", "sub_workflow"],
            "AI": ["agent", "llm_call"]
        }

        for category, nodes in categories.items():
            for node_type in nodes:
                item = QListWidgetItem(f"{category}: {node_type}")
                item.setData(Qt.UserRole, node_type)
                self.node_list.addItem(item)

    def _on_item_clicked(self, item):
        node_type = item.data(Qt.UserRole)
        self.node_selected.emit(node_type)
```

- [ ] **Step 2: 提交**

---

#### Task 10: 实现画布 (WorkflowCanvas)

**Files:**
- Create: `workflow_engine/ui/canvas.py`

- [ ] **Step 1: 实现画布组件**

```python
# workflow_engine/ui/canvas.py
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPen, QBrush, QColor

class NodeGraphicsItem(QGraphicsRectItem):
    def __init__(self, node_id: str, node_type: str, width: int = 120, height: int = 60):
        super().__init__(0, 0, width, height)
        self.node_id = node_id
        self.node_type = node_type
        self.setBrush(QBrush(QColor("#3498db")))
        self.setPen(QPen(QColor("#2980b9"), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        from PySide6.QtWidgets import QGraphicsTextItem
        text = QGraphicsTextItem(self)
        text.setPlainText(f"{node_type}\n{node_id}")
        text.setDefaultTextColor(QColor("white"))
        text.setPos(10, 15)

class WorkflowCanvas(QGraphicsView):
    node_double_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self._node_items = {}

    def add_node(self, node_id: str, node_type: str, x: float, y: float):
        item = NodeGraphicsItem(node_id, node_type)
        item.setPos(x, y)
        self.scene.addItem(item)
        self._node_items[node_id] = item
        return item

    def remove_node(self, node_id: str):
        if node_id in self._node_items:
            item = self._node_items.pop(node_id)
            self.scene.removeItem(item)

    def get_node_position(self, node_id: str) -> QPointF:
        if node_id in self._node_items:
            return self._node_items[node_id].pos()
        return QPointF()

    def clear(self):
        self.scene.clear()
        self._node_items.clear()
```

- [ ] **Step 2: 提交**

---

#### Task 11: 实现属性面板 (PropertyPanel)

**Files:**
- Create: `workflow_engine/ui/property_panel.py`

- [ ] **Step 1: 实现属性面板**

```python
# workflow_engine/ui/property_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QFormLayout
from PySide6.QtCore import Signal

class PropertyPanel(QWidget):
    config_changed = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._current_node_id = None

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("属性面板")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)

        layout.addStretch()

    def set_node(self, node_id: str, node_type: str, config: dict):
        self._current_node_id = node_id
        self._clear_form()

        self.form_layout.addRow("节点ID:", QLabel(node_id))
        self.form_layout.addRow("类型:", QLabel(node_type))

        self.config_widgets = {}
        for key, value in config.items():
            edit = QLineEdit(str(value))
            self.form_layout.addRow(f"{key}:", edit)
            self.config_widgets[key] = edit

    def _clear_form(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_config(self) -> dict:
        if not self._current_node_id:
            return {}
        return {key: widget.text() for key, widget in self.config_widgets.items()}
```

- [ ] **Step 2: 提交**

---

#### Task 12: 实现日志面板 (LogPanel)

**Files:**
- Create: `workflow_engine/ui/log_panel.py`

- [ ] **Step 1: 实现日志面板**

```python
# workflow_engine/ui/log_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PySide6.QtCore import Qt
from datetime import datetime

class LogPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("执行日志")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = {
            "INFO": "#2ecc71",
            "DEBUG": "#3498db",
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c"
        }.get(level, "#000000")

        html = f'<span style="color: #888;">[{timestamp}]</span> '
        html += f'<span style="color: {color};">[{level}]</span> '
        html += f'{message}<br>'

        self.log_text.append(html)

    def info(self, message: str):
        self.log("INFO", message)

    def debug(self, message: str):
        self.log("DEBUG", message)

    def warning(self, message: str):
        self.log("WARNING", message)

    def error(self, message: str):
        self.log("ERROR", message)

    def clear(self):
        self.log_text.clear()
```

- [ ] **Step 2: 提交**

---

### Phase 3: 存储与执行

#### Task 13: 实现存储层

**Files:**
- Create: `workflow_engine/storage/workflow_storage.py`
- Create: `workflow_engine/storage/history_storage.py`

- [ ] **Step 1: 实现存储层**

```python
# workflow_engine/storage/workflow_storage.py
import json
import os
from typing import Optional
from workflow_engine.core.workflow import Workflow

class WorkflowStorage:
    def __init__(self, storage_dir: str = "workflows"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, workflow: Workflow):
        filepath = os.path.join(self.storage_dir, f"{workflow.id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(workflow.to_dict(), f, ensure_ascii=False, indent=2)

    def load(self, workflow_id: str) -> Optional[Workflow]:
        filepath = os.path.join(self.storage_dir, f"{workflow_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Workflow.from_dict(data)

    def list_workflows(self):
        files = [f[:-5] for f in os.listdir(self.storage_dir) if f.endswith(".json")]
        return files

    def delete(self, workflow_id: str):
        filepath = os.path.join(self.storage_dir, f"{workflow_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
```

```python
# workflow_engine/storage/history_storage.py
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class HistoryStorage:
    def __init__(self, db_path: str = "workflow_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT,
                    node_states TEXT,
                    error_message TEXT
                )
            """)

    def add_execution(self, workflow_id: str, status: str = "running") -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO execution_history (workflow_id, started_at, status)
                VALUES (?, ?, ?)
            """, (workflow_id, datetime.now().isoformat(), status))
            return cursor.lastrowid

    def finish_execution(self, execution_id: int, status: str, node_states: Dict, error_message: str = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE execution_history
                SET finished_at = ?, status = ?, node_states = ?, error_message = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), status, json.dumps(node_states), error_message, execution_id))

    def get_history(self, workflow_id: str, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM execution_history
                WHERE workflow_id = ?
                ORDER BY started_at DESC
                LIMIT ?
            """, (workflow_id, limit))
            return [dict(row) for row in cursor.fetchall()]
```

- [ ] **Step 2: 提交**

---

#### Task 14: 实现调度器 (Scheduler)

**Files:**
- Create: `workflow_engine/core/scheduler.py`

- [ ] **Step 1: 实现调度器**

```python
# workflow_engine/core/scheduler.py
import threading
import schedule
import time
from typing import Dict, Callable, Optional
from datetime import datetime

class Scheduler:
    def __init__(self):
        self._jobs: Dict[str, Dict] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def add_interval_job(self, job_id: str, func: Callable, seconds: int, workflow_id: str):
        self._jobs[job_id] = {
            "func": func,
            "interval": seconds,
            "workflow_id": workflow_id,
            "type": "interval"
        }
        schedule.every(seconds).seconds.do(self._run_job, job_id)

    def add_cron_job(self, job_id: str, func: Callable, cron_expr: str, workflow_id: str):
        self._jobs[job_id] = {
            "func": func,
            "cron": cron_expr,
            "workflow_id": workflow_id,
            "type": "cron"
        }
        parts = cron_expr.split()
        if len(parts) == 5:
            schedule.every().day.at(f"{parts[1]}:{parts[0]}").do(self._run_job, job_id)

    def remove_job(self, job_id: str):
        if job_id in self._jobs:
            del self._jobs[job_id]

    def _run_job(self, job_id: str):
        job = self._jobs.get(job_id)
        if job:
            job["func"](job["workflow_id"])

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def _run_loop(self):
        while self._running:
            schedule.run_pending()
            time.sleep(1)
```

- [ ] **Step 2: 提交**

---

### Phase 4: 高级特性

#### Task 15: 实现条件分支节点 (Condition)

**Files:**
- Create: `workflow_engine/nodes/flow/condition.py`

- [ ] **Step 1: 实现条件分支节点**

```python
# workflow_engine/nodes/flow/condition.py
from typing import Dict
from workflow_engine.nodes.base import BaseNode

class ConditionNode(BaseNode):
    """条件分支节点"""

    category = "流程控制"
    display_name = "条件分支"
    node_type = "condition"

    input_ports = [("input", "flow")]
    output_ports = [("true", "flow"), ("false", "flow")]

    config_schema = {
        "expression": {"type": "string", "required": True}
    }

    def execute(self, inputs: Dict) -> Dict:
        expression = self.config.get("expression", "")
        try:
            result = self._evaluate_expression(expression, inputs)
            return {"condition": result, "branch": "true" if result else "false"}
        except Exception as e:
            return {"condition": False, "branch": "false", "error": str(e)}

    def _evaluate_expression(self, expression: str, context: Dict) -> bool:
        local_vars = {**self.variables.to_dict().get("variables", {}), **context}
        try:
            return eval(expression, {"__builtins__": {}}, local_vars)
        except:
            return False
```

- [ ] **Step 2: 提交**

---

#### Task 16: 实现循环节点 (Loop)

**Files:**
- Create: `workflow_engine/nodes/flow/loop.py`

- [ ] **Step 1: 实现循环节点**

```python
# workflow_engine/nodes/flow/loop.py
from typing import Dict, List
from workflow_engine.nodes.base import BaseNode

class LoopNode(BaseNode):
    """循环执行节点"""

    category = "流程控制"
    display_name = "循环"
    node_type = "loop"

    input_ports = [("input", "flow")]
    output_ports = [("output", "flow")]

    config_schema = {
        "items": {"type": "string", "required": True},
        "variable_name": {"type": "string", "default": "item"}
    }

    def execute(self, inputs: Dict) -> Dict:
        items_expr = self.config.get("items", "[]")
        variable_name = self.config.get("variable_name", "item")

        try:
            items = self._evaluate_items(items_expr, inputs)
            results = []
            for item in items:
                self.variables.set(variable_name, item)
                results.append({"item": item, "success": True})
            return {"results": results, "count": len(results)}
        except Exception as e:
            return {"results": [], "count": 0, "error": str(e)}

    def _evaluate_items(self, expression: str, context: Dict) -> List:
        local_vars = {**self.variables.to_dict().get("variables", {}), **context}
        try:
            result = eval(expression, {"__builtins__": {}}, local_vars)
            return result if isinstance(result, list) else []
        except:
            return []
```

- [ ] **Step 2: 提交**

---

#### Task 17: 实现错误处理机制

- [ ] **Step 1: 扩展BaseNode添加错误处理**

```python
# 在 base.py 中添加
class BaseNode(ABC):
    # ... existing code ...

    def execute_with_error_handling(self, inputs: Dict) -> Dict:
        retry_count = self.config.get("retry_count", 0)
        fallback_node_id = self.config.get("fallback_node")

        for attempt in range(retry_count + 1):
            try:
                return self.execute(inputs)
            except Exception as e:
                if attempt < retry_count:
                    continue
                if fallback_node_id:
                    return self.workflow.execute_node(fallback_node_id, inputs)
                raise
```

- [ ] **Step 2: 提交**

---

### Phase 5: AI集成

#### Task 18: 实现Agent节点

**Files:**
- Create: `workflow_engine/nodes/ai/agent.py`

- [ ] **Step 1: 实现Agent节点**

```python
# workflow_engine/nodes/ai/agent.py
from typing import Dict, List, Optional
from workflow_engine.nodes.base import BaseNode

class AgentNode(BaseNode):
    """AI Agent节点"""

    category = "AI"
    display_name = "Agent"
    node_type = "agent"

    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    config_schema = {
        "prompt": {"type": "string", "required": True},
        "model": {"type": "string", "default": "gpt-4"},
        "api_key": {"type": "string", "required": True},
        "tools": {"type": "list", "default": []}
    }

    def execute(self, inputs: Dict) -> Dict:
        prompt = self.config.get("prompt", "")
        model = self.config.get("model", "gpt-4")
        api_key = self.config.get("api_key", "")

        try:
            response = self._call_llm(prompt, model, api_key, inputs)
            return {"response": response, "success": True}
        except Exception as e:
            return {"response": None, "success": False, "error": str(e)}

    def _call_llm(self, prompt: str, model: str, api_key: str, inputs: Dict) -> str:
        # Placeholder for OpenAI API call
        # In real implementation, use openai library
        return f"LLM response for: {prompt}"
```

- [ ] **Step 2: 提交**

---

#### Task 19: 实现LLM调用节点

**Files:**
- Create: `workflow_engine/nodes/ai/llm_call.py`

- [ ] **Step 1: 实现LLM调用节点**

```python
# workflow_engine/nodes/ai/llm_call.py
from typing import Dict
from workflow_engine.nodes.base import BaseNode

class LLMCallNode(BaseNode):
    """LLM调用节点"""

    category = "AI"
    display_name = "LLM调用"
    node_type = "llm_call"

    input_ports = [("input", "any")]
    output_ports = [("output", "string")]

    config_schema = {
        "prompt_template": {"type": "string", "required": True},
        "model": {"type": "string", "default": "gpt-4"},
        "temperature": {"type": "float", "default": 0.7}
    }

    def execute(self, inputs: Dict) -> Dict:
        prompt_template = self.config.get("prompt_template", "")
        model = self.config.get("model", "gpt-4")
        temperature = self.config.get("temperature", 0.7)

        try:
            prompt = self._render_template(prompt_template, inputs)
            response = self._call_api(prompt, model, temperature)
            return {"text": response, "success": True}
        except Exception as e:
            return {"text": None, "success": False, "error": str(e)}

    def _render_template(self, template: str, context: Dict) -> str:
        for key, value in context.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template

    def _call_api(self, prompt: str, model: str, temperature: float) -> str:
        # Placeholder for OpenAI API call
        return f"Response: {prompt[:50]}..."
```

- [ ] **Step 2: 提交**

---

## 任务依赖关系

```
Task 1 (项目脚手架)
    ↓
Task 2 (VariableStore) ← Task 3 (NodeRegistry)
    ↓                    ↓
Task 4 (BaseNode) ←─────────────────────
    ↓
Task 5 (Workflow)
    ↓
Task 6 (Executor)
    ↓
Task 7 (WorkflowEngine)
    ↓
Task 8-12 (UI组件)
    ↓
Task 13 (存储层)
    ↓
Task 14 (调度器)
    ↓
Task 15-17 (高级特性)
    ↓
Task 18-19 (AI节点)
```

---

## 执行方式选择

**Plan 完成并保存至 `docs/superpowers/plans/2026-06-22-workflow-engine-implementation.md`**

两种执行方式：

1. **Subagent-Driven (推荐)** - 每任务派遣独立subagent，任务间审查，快速迭代
2. **Inline Execution** - 本会话批量执行，带检查点

选择哪种方式？
