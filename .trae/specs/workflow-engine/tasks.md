# 工作流引擎 实施任务

## Phase 1: 核心框架

- [ ] **Task 1**: 创建项目脚手架和目录结构
  - 创建 `workflow_engine/core/`, `workflow_engine/nodes/`, `workflow_engine/ui/`, `workflow_engine/storage/`, `workflow_engine/utils/` 目录
  - 创建所有 `__init__.py` 文件
  - 创建 `requirements.txt` (PySide6>=6.5, APScheduler>=3.10)

- [ ] **Task 2**: 实现变量系统 (VariableStore)
  - 创建 `workflow_engine/core/variable_store.py`
  - 创建 `tests/core/test_variable_store.py`
  - 实现 set/get/get_type/has/remove/clear/to_dict/from_dict 方法
  - 编写测试并验证

- [ ] **Task 3**: 实现节点注册表 (NodeRegistry)
  - 创建 `workflow_engine/core/node_registry.py`
  - 创建 `tests/core/test_node_registry.py`
  - 实现 register/get_node_class/get_all_types/get_categories 方法
  - 编写测试并验证

- [ ] **Task 4**: 实现节点基类 (BaseNode)
  - 创建 `workflow_engine/nodes/base.py`
  - 实现抽象基类，包含 category, display_name, node_type, input_ports, output_ports, config_schema
  - 实现 execute, validate, set_config, get_state, set_state 方法

- [ ] **Task 5**: 实现工作流主类 (Workflow)
  - 创建 `workflow_engine/core/workflow.py`
  - 创建 `tests/core/test_workflow.py`
  - 实现 add_node, remove_node, add_edge, remove_edge, to_dict, from_dict 方法
  - 编写测试并验证

- [ ] **Task 6**: 实现执行器 (Executor)
  - 创建 `workflow_engine/core/executor.py`
  - 创建 `tests/core/test_executor.py`
  - 实现顺序执行、并行执行、单步执行
  - 实现 topological_sort 拓扑排序
  - 编写测试并验证

- [ ] **Task 7**: 实现工作流引擎 (WorkflowEngine)
  - 创建 `workflow_engine/core/engine.py`
  - 实现 add_workflow, remove_workflow, run_workflow, pause_workflow, stop_workflow 方法

## Phase 2: 可视化界面

- [ ] **Task 8**: 实现主窗口 (MainWindow)
  - 创建 `workflow_engine/ui/main_window.py`
  - 实现 PySide6 主窗口框架
  - 集成节点面板、画布、属性面板、日志面板
  - 添加工具栏 (运行/单步/停止)

- [ ] **Task 9**: 实现节点面板 (NodePanel)
  - 创建 `workflow_engine/ui/node_panel.py`
  - 实现分类节点列表
  - 实现 node_selected 信号

- [ ] **Task 10**: 实现画布 (WorkflowCanvas)
  - 创建 `workflow_engine/ui/canvas.py`
  - 实现 QGraphicsView 画布
  - 实现 NodeGraphicsItem 节点图形
  - 支持拖拽、缩放、选择

- [ ] **Task 11**: 实现属性面板 (PropertyPanel)
  - 创建 `workflow_engine/ui/property_panel.py`
  - 显示选中节点配置
  - 支持配置编辑

- [ ] **Task 12**: 实现日志面板 (LogPanel)
  - 创建 `workflow_engine/ui/log_panel.py`
  - 实现 info/debug/warning/error 日志方法
  - 支持日志显示和清除

## Phase 3: 存储与执行

- [ ] **Task 13**: 实现存储层
  - 创建 `workflow_engine/storage/workflow_storage.py`
  - 创建 `workflow_engine/storage/history_storage.py`
  - 实现工作流 JSON 保存/加载
  - 实现执行历史 SQLite 存储

- [ ] **Task 14**: 实现调度器 (Scheduler)
  - 创建 `workflow_engine/core/scheduler.py`
  - 支持间隔任务和 Cron 任务
  - 后台线程运行

## Phase 4: 高级特性

- [ ] **Task 15**: 实现条件分支节点 (Condition)
  - 创建 `workflow_engine/nodes/flow/condition.py`
  - 支持表达式求值
  - 实现 true/false 分支输出

- [ ] **Task 16**: 实现循环节点 (Loop)
  - 创建 `workflow_engine/nodes/flow/loop.py`
  - 支持列表迭代
  - 变量注入

- [ ] **Task 17**: 实现子流程节点 (SubWorkflow)
  - 创建 `workflow_engine/nodes/flow/sub_workflow.py`
  - 支持嵌套工作流调用

- [ ] **Task 18**: 实现错误处理机制
  - 扩展 BaseNode 添加 retry_count 和 fallback_node
  - 实现 execute_with_error_handling 方法

## Phase 5: AI集成

- [ ] **Task 19**: 实现 Agent 节点
  - 创建 `workflow_engine/nodes/ai/agent.py`
  - 支持 LLM 调用
  - 支持工具执行

- [ ] **Task 20**: 实现 LLM 调用节点
  - 创建 `workflow_engine/nodes/ai/llm_call.py`
  - 支持 prompt 模板
  - 支持 temperature 参数

## Phase 6: UI 美化（复古工业风 × 赛博朋克暖光）

- [ ] **Task 21**: 创建样式基础设施（theme.py + QSS 加载入口 + 基础样式）
  - 创建 `workflow_engine/ui/styles/__init__.py`
  - 创建 `workflow_engine/ui/styles/theme.py`（颜色/字体常量）
  - 创建 `workflow_engine/ui/styles/base.qss`（全局基础样式）
  - 创建 `workflow_engine/ui/styles/components.qss`（通用组件样式）
  - 修改 `main_window.py` 添加样式加载

- [ ] **Task 22**: 美化主窗口（工具栏图标+文字、状态栏）
  - 填充 `workflow_engine/ui/styles/main_window.qss`
  - 修改 `main_window.py` 将 QAction 改为 QToolButton

- [ ] **Task 23**: 重构节点面板为网格卡片布局
  - 填充 `workflow_engine/ui/styles/node_panel.qss`
  - 重构 `node_panel.py` 为 NodeCard + QGridLayout

- [ ] **Task 24**: 美化画布（网格点阵背景 + 贝塞尔曲线连线）
  - 填充 `workflow_engine/ui/styles/canvas.qss`
  - 重写 `canvas.py` 实现 drawBackground 网格点阵
  - 重构 EdgeGraphicsItem 为贝塞尔曲线

- [ ] **Task 25**: 美化节点样式 + 呼吸脉冲动画
  - 重构 NodeGraphicsItem 圆角卡片 + QGraphicsDropShadowEffect
  - 实现 set_state + _start_pulse + _pulse_step

- [ ] **Task 26**: 美化属性面板 + 日志面板
  - 填充 property_panel.qss 和 log_panel.qss
  - 添加 objectName 到两个面板

- [ ] **Task 27**: 右键上下文菜单 + 最终整合测试
  - 在 canvas.py 中添加 QMenu 右键菜单
  - 整合测试所有美化效果

## 任务依赖关系

```
Task 21 (样式基础设施)
    ↓
Task 22 (主窗口美化)      Task 23 (节点面板网格卡片)
    ↓                           ↓
Task 24 (画布美化) ← ← ← ← ↗
    ↓
Task 25 (节点样式+呼吸动画)
    ↓
Task 26 (属性+日志面板美化)
    ↓
Task 27 (右键菜单+整合测试)
```

## 原 Phase 1-5 依赖关系

```
Task 1 (脚手架)
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
Task 15-18 (高级特性)
    ↓
Task 19-20 (AI节点)
```
