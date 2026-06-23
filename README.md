# 节点工具 (jiedian_tool)

可视化工作流节点框架，基于 **Python + PySide6** 构建的桌面端应用。

## 功能特性

- **可视化编辑**：拖拽节点到画布、端口间贝塞尔曲线连线、属性配置
- **节点体系**：5 大类 14 种节点（输入/输出/流程控制/数据处理/AI），继承 `BaseNode` 即可扩展
- **执行引擎**：拓扑排序驱动，支持顺序/并行执行、单步调试
- **流程控制**：条件分支、循环、子流程嵌套（最大 3 层）
- **容错机制**：节点重试 + fallback 节点
- **定时调度**：基于 APScheduler 的间隔/每日/Cron 定时执行
- **持久化**：工作流 JSON 存储 + SQLite 执行历史
- **暗色主题**：VS Code Dark+ 色系，3 套可切换主题

## 快速开始

### 环境要求

- Python >= 3.10

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

```bash
python -m workflow_engine.main
```

## 项目结构

```
workflow_engine/
├── main.py              # 主入口
├── core/                # 核心引擎
│   ├── engine.py        # WorkflowEngine 工作流管理器
│   ├── executor.py      # Executor 执行器（拓扑排序）
│   ├── workflow.py      # Workflow 数据模型
│   ├── node_registry.py # NodeRegistry 节点注册表
│   ├── scheduler.py     # Scheduler 定时调度器
│   └── variable_store.py# VariableStore 变量存储
├── nodes/               # 节点定义
│   ├── base.py          # BaseNode 抽象基类
│   ├── ai/              # AI 节点（agent、llm_call）
│   ├── flow/            # 流程控制节点（condition、loop、sub_workflow）
│   ├── input/           # 输入节点
│   └── output/          # 输出节点
├── storage/             # 持久化存储
│   ├── workflow_storage.py  # JSON 文件存储
│   └── history_storage.py   # SQLite 执行历史
├── ui/                  # PySide6 可视化界面
│   ├── main_window.py   # 主窗口
│   ├── canvas.py        # 画布（拖拽/连线/缩放）
│   ├── node_panel.py    # 节点面板
│   ├── property_panel.py# 属性面板
│   ├── log_panel.py     # 日志面板
│   └── styles/          # QSS 样式系统
└── utils/               # 工具模块
```

## 自定义节点

继承 `BaseNode` 并实现 `execute` 方法：

```python
from workflow_engine.nodes.base import BaseNode

class MyNode(BaseNode):
    node_type = "my_node"
    display_name = "自定义节点"
    category = "数据处理"
    input_ports = [{"name": "input", "type": "any"}]
    output_ports = [{"name": "output", "type": "any"}]

    def execute(self, inputs):
        data = inputs.get("input", "")
        return {"output": data.upper()}
```
