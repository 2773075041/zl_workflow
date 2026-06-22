# 工作流引擎 检查清单

## Phase 1: 核心框架

- [x] Task 1: 项目脚手架创建完成，所有目录和 __init__.py 文件存在
- [x] Task 2: VariableStore 的 set/get/to_dict/from_dict 方法测试通过
- [x] Task 3: NodeRegistry 的 register/get_node_class 方法测试通过
- [x] Task 4: BaseNode 抽象基类可被继承，子类必须实现 execute 方法
- [x] Task 5: Workflow 的 add_node/add_edge/to_dict/from_dict 测试通过
- [x] Task 6: Executor 顺序执行测试通过，单步执行测试通过
- [x] Task 7: WorkflowEngine 可添加工作流并执行

## Phase 2: 可视化界面

- [x] Task 8: MainWindow 可启动，显示四个面板
- [x] Task 9: NodePanel 显示分类节点列表，点击发射 node_selected 信号
- [x] Task 10: WorkflowCanvas 可添加/删除节点，节点可拖拽
- [x] Task 11: PropertyPanel 显示选中节点配置
- [x] Task 12: LogPanel 支持 info/debug/warning/error 日志输出

## Phase 3: 存储与执行

- [x] Task 13: WorkflowStorage 可保存/加载工作流 JSON
- [x] Task 13: HistoryStorage 可记录执行历史到 SQLite
- [x] Task 14: Scheduler 可添加间隔任务并执行

## Phase 4: 高级特性

- [x] Task 15: ConditionNode 根据表达式返回 true/false 分支
- [x] Task 16: LoopNode 可迭代列表并执行
- [x] Task 17: SubWorkflowNode 可调用子工作流
- [x] Task 18: BaseNode 支持 retry_count 和 fallback_node 配置

## Phase 5: AI集成

- [x] Task 19: AgentNode 可调用 LLM
- [x] Task 20: LLMCallNode 支持 prompt 模板渲染

## 集成验证

- [x] 所有节点可通过继承 BaseNode 实现
- [x] 工作流可保存为 JSON 并重新加载
- [x] 界面可正常启动和交互
- [x] 执行日志正确显示
- [x] 调度器可定时执行工作流
