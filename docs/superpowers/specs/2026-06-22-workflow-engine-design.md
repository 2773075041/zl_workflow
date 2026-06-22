# 工作流引擎 (WorkflowEngine) 设计文档

**版本**: 1.0  
**日期**: 2026-06-22  
**状态**: 设计中

---

## 1. 项目概述

### 1.1 项目目标
开发一个 PC 端可视化工作流节点框架，支持用户通过拖拽、连线、配置等方式构建工作流，并支持后续扩展自定义节点功能。

### 1.2 核心特性
- 可视化界面（PyQt/PySide）—— 节点面板 + 画布 + 连线 + 属性编辑
- 节点继承式扩展 —— 用户继承 `BaseNode` 实现自定义节点
- 变量系统 —— 工作流级别的键值存储，节点间数据共享
- 三种执行模式 —— 手动执行、定时执行、触发执行
- 完整调试能力 —— 执行日志、单步执行、执行状态可视化
- 高级特性 —— 多Agent协作、子流程嵌套、条件分支、循环、错误处理
- 并发执行 —— 多个工作流同时运行
- 节点分类 —— 节点支持多分类管理

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    可视化界面层 (PyQt/PySide)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ 节点面板  │  │  画布     │  │ 属性编辑  │  │ 执行监控│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
├─────────────────────────────────────────────────────────┤
│                    核心引擎层                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ 工作流引擎 │  │  节点容器  │  │ 变量系统  │  │ 执行器 │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 调度器   │  │ 触发器    │  │ Agent运行时│              │
│  └──────────┘  └──────────┘  └──────────┘              │
├─────────────────────────────────────────────────────────┤
│                    节点扩展层                            │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────┐ │
│  │ 内置节点 │ │ 插件节点 │ │ Agent  │ │ 子流程  │ │ ... │ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └─────┘ │
├─────────────────────────────────────────────────────────┤
│                    存储层                                │
│  ┌──────────────┐           ┌──────────────┐          │
│  │  JSON (工作流) │           │ SQLite (历史) │          │
│  └──────────────┘           └──────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 模块职责

| 模块 | 职责 |
|------|------|
| **可视化界面层** | 节点面板(分类列表)、画布(拖拽/连线/缩放)、属性编辑、执行监控 |
| **工作流引擎 (WorkflowEngine)** | 解析工作流DAG、节点调度、流程控制 |
| **节点容器 (NodeRegistry)** | 节点注册、发现、实例化管理 |
| **变量系统 (VariableStore)** | 工作流级变量存取、类型安全 |
| **执行器 (Executor)** | 顺序执行、并行执行、条件分支、循环执行 |
| **调度器 (Scheduler)** | 定时任务管理、触发器管理 |
| **Agent运行时** | LLM调用、工具执行、多Agent协作 |
| **存储层** | JSON存储工作流定义、SQLite存储执行历史 |

---

## 3. 核心组件设计

### 3.1 节点基类 (BaseNode)

```python
class BaseNode:
    """所有节点的基类"""

    # 节点分类
    category: str = "基础"
    # 节点显示名称
    display_name: str = "节点"
    # 节点唯一标识
    node_type: str = "base"

    # 输入端口定义 [(name, type), ...]
    input_ports: List[tuple] = []
    # 输出端口定义 [(name, type), ...]
    output_ports: List[tuple] = []

    # 节点配置项定义
    config_schema: Dict = {}

    def __init__(self, node_id: str, workflow: "Workflow"):
        self.node_id = node_id
        self.workflow = workflow
        self.variables = workflow.variables
        self.config = {}

    def execute(self, inputs: Dict) -> Dict:
        """节点执行逻辑，子类必须实现"""
        raise NotImplementedError

    def validate(self) -> bool:
        """节点配置校验"""
        return True
```

### 3.2 内置节点分类

| 分类 | 节点 | 说明 |
|------|------|------|
| **输入** | ManualInput | 手动输入触发 |
| | TimerTrigger | 定时触发 |
| | FileWatcher | 文件变化触发 |
| | Webhook | HTTP回调触发 |
| **输出** | Logger | 输出日志 |
| | FileWriter | 写入文件 |
| | HttpRequest | HTTP请求 |
| **流程控制** | Condition | 条件分支 |
| | Loop | 循环执行 |
| | SubWorkflow | 子流程调用 |
| **数据处理** | Transform | 数据转换 |
| | Filter | 数据过滤 |
| **AI** | Agent | AI Agent节点 |
| | LLMCall | LLM调用节点 |

### 3.3 变量系统

```python
class VariableStore:
    """工作流级变量存储"""

    def __init__(self):
        self._variables: Dict[str, Any] = {}
        self._types: Dict[str, type] = {}

    def set(self, key: str, value: Any, vtype: type = None):
        """设置变量"""
        self._variables[key] = value
        if vtype:
            self._types[key] = vtype

    def get(self, key: str, default: Any = None) -> Any:
        """获取变量"""
        return self._variables.get(key, default)

    def get_type(self, key: str) -> type:
        """获取变量类型"""
        return self._types.get(key, type(self._variables.get(key)))
```

### 3.4 执行器

```python
class Executor:
    """工作流执行器"""

    def __init__(self, workflow: "Workflow"):
        self.workflow = workflow

    def execute(self, mode: str = "sequential"):
        """执行工作流
        mode: sequential | parallel | step
        """
        pass

    def step(self) -> bool:
        """单步执行，返回是否还有下一步"""
        pass

    def get_status(self) -> Dict:
        """获取执行状态"""
        pass
```

### 3.5 存储结构

**工作流 JSON 格式** (`workflows/*.json`):
```json
{
    "id": "uuid",
    "name": "工作流名称",
    "version": 1,
    "nodes": [
        {
            "id": "node_1",
            "type": "manual_input",
            "category": "输入",
            "position": {"x": 100, "y": 200},
            "config": {},
            "inputs": [],
            "outputs": ["node_2"]
        }
    ],
    "variables": {}
}
```

**SQLite 执行历史**:
```sql
CREATE TABLE execution_history (
    id INTEGER PRIMARY KEY,
    workflow_id TEXT,
    started_at DATETIME,
    finished_at DATETIME,
    status TEXT,
    node_states JSON,
    error_message TEXT
);
```

---

## 4. 界面设计

### 4.1 主界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  菜单栏  │ 文件  编辑  运行  帮助                              │
├─────────────────────────────────────────────────────────────┤
│  工具栏  │ ▶运行 │ ⏸暂停 │ ⏹停止 │ ⏭单步 │ 🔄重置           │
├──────────┬──────────────────────────────────────┬──────────┤
│          │                                      │          │
│  节点面板  │           画布区域                   │  属性面板  │
│  ─────── │                                      │  ─────── │
│  📁 输入   │     [节点A] ──────→ [节点B]          │  节点配置  │
│  📁 输出   │         ↓                          │  ─────── │
│  📁 流程   │     [节点C]                         │  名称: xxx │
│  📁 AI    │                                      │  参数1:    │
│  📁 数据   │                                      │  参数2:    │
│          │                                      │          │
├──────────┴──────────────────────────────────────┴──────────┤
│  执行日志                                                   │
│  ─────────────────────────────────────────────────────────  │
│  [INFO] 2026-06-22 10:00:00 节点A 开始执行                    │
│  [INFO] 2026-06-22 10:00:01 节点A 执行完成                    │
│  [DEBUG] 2026-06-22 10:00:01 变量 x = 100                    │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 节点组件

每个节点在画布上显示：
- 节点标题栏（含图标、名称）
- 输入端口（左侧圆点）
- 输出端口（右侧圆点）
- 执行状态指示（等待/运行中/成功/失败）

### 4.3 连线交互
- 拖拽：从输出端口拖出，连接到输入端口
- 删除：选中连线，按 Delete 删除
- 弯曲线：自动避让节点

---

## 5. 高级特性

### 5.1 多Agent协作
```python
class AgentNode(BaseNode):
    """AI Agent节点"""

    def __init__(self, node_id: str, workflow: "Workflow"):
        super().__init__(node_id, workflow)
        self.llm_config = {}
        self.tools = []

    def execute(self, inputs: Dict) -> Dict:
        # 调用LLM
        response = self.llm.chat(self.config["prompt"], **self.llm_config)
        # 执行工具
        for tool_call in response.tool_calls:
            result = self.execute_tool(tool_call)
        return {"response": response.content}
```

### 5.2 子流程嵌套
```python
class SubWorkflowNode(BaseNode):
    """子流程节点"""

    def execute(self, inputs: Dict) -> Dict:
        sub_workflow = Workflow.load(self.config["sub_workflow_id"])
        result = sub_workflow.execute(inputs)
        return result
```

### 5.3 条件分支
```python
class ConditionNode(BaseNode):
    """条件分支节点"""

    output_ports = [
        ("true", "flow"),
        ("false", "flow")
    ]

    def execute(self, inputs: Dict) -> Dict:
        condition = self.evaluate(self.config["expression"])
        return {"condition": condition}
```

### 5.4 循环执行
```python
class LoopNode(BaseNode):
    """循环节点"""

    def execute(self, inputs: Dict) -> Dict:
        for item in self.evaluate(self.config["items"]):
            self.workflow.execute_node(self.config["body_node"], {"item": item})
        return {"result": results}
```

### 5.5 错误处理
```python
class BaseNode:
    def execute(self, inputs: Dict) -> Dict:
        try:
            return self._execute(inputs)
        except Exception as e:
            if self.config.get("retry_count"):
                return self._retry(inputs)
            if self.config.get("fallback_node"):
                return self.workflow.execute_node(self.config["fallback_node"], inputs)
            raise
```

---

## 6. 项目结构

```
workflow_engine/
├── core/                      # 核心引擎
│   ├── __init__.py
│   ├── workflow.py            # 工作流主类
│   ├── engine.py              # 工作流引擎
│   ├── executor.py             # 执行器
│   ├── scheduler.py            # 调度器
│   ├── variable_store.py       # 变量系统
│   └── node_registry.py        # 节点注册表
├── nodes/                     # 节点定义
│   ├── __init__.py
│   ├── base.py                 # 节点基类
│   ├── input/                  # 输入节点
│   │   ├── manual_input.py
│   │   ├── timer_trigger.py
│   │   └── file_watcher.py
│   ├── output/                 # 输出节点
│   │   ├── logger.py
│   │   └── file_writer.py
│   ├── flow/                   # 流程控制
│   │   ├── condition.py
│   │   ├── loop.py
│   │   └── sub_workflow.py
│   └── ai/                     # AI节点
│       ├── agent.py
│       └── llm_call.py
├── ui/                         # 可视化界面
│   ├── __init__.py
│   ├── main_window.py          # 主窗口
│   ├── node_panel.py           # 节点面板
│   ├── canvas.py               # 画布
│   ├── property_panel.py       # 属性面板
│   ├── log_panel.py            # 日志面板
│   └── dialogs/                # 对话框
├── storage/                    # 存储层
│   ├── __init__.py
│   ├── workflow_storage.py     # 工作流存储
│   └── history_storage.py      # 历史记录
├── utils/                      # 工具函数
│   └── __init__.py
└── main.py                     # 程序入口
```

---

## 7. 技术选型

| 组件 | 技术 | 说明 |
|------|------|------|
| 界面框架 | PySide6 | 跨平台、原生界面、免费商用 |
| 图形渲染 | QGraphicsView | 适合节点图画布 |
| 存储 | json + sqlite3 | 轻量、无外部依赖 |
| 定时任务 | schedule / APScheduler | 简单可靠 |
| HTTP服务 | FastAPI (可选) | 触发器用 |
| LLM集成 | OpenAI SDK | 统一接口 |

---

## 8. 实施阶段

### Phase 1: 核心框架
- 项目脚手架搭建
- 节点基类实现
- 核心引擎实现
- 基础节点实现

### Phase 2: 可视化界面
- 主窗口框架
- 节点面板
- 画布编辑器
- 属性面板
- 日志面板

### Phase 3: 存储与执行
- 工作流存储
- 执行器实现
- 调度器实现

### Phase 4: 高级特性
- 条件分支、循环
- 子流程嵌套
- 错误处理

### Phase 5: AI集成
- Agent节点
- LLM调用节点

---

## 9. 验收标准

1. ✅ 用户可通过可视化界面创建、编辑、保存工作流
2. ✅ 支持节点拖拽、连线、配置
3. ✅ 支持节点继承式扩展
4. ✅ 支持手动执行、定时执行、触发执行
5. ✅ 支持变量系统在节点间传递数据
6. ✅ 支持执行日志、单步执行、状态可视化
7. ✅ 支持并发执行
8. ✅ 支持节点分类管理
9. ✅ 支持条件分支、循环、子流程嵌套
10. ✅ 支持错误处理机制
