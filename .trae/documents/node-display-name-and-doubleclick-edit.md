# 节点拖拽显示名称 + 双击编辑属性

## 摘要

1. 拖拽节点到画布后显示对应的中文名称（而非 `node_type` 标识符）
2. 双击画布节点时，右侧属性面板自动加载该节点的信息供编辑

## 当前状态分析

| 问题 | 位置 | 根因 |
|------|------|------|
| 拖入节点不显示中文名 | [canvas.py:354-357](file:///d:/Code/jiedian_tool/workflow_engine/ui/canvas.py#L354-L357) | `dropEvent` → `add_node` 传入 `display_name=""`，无映射查询 |
| 双击不弹出属性 | [main_window.py](file:///d:/Code/jiedian_tool/workflow_engine/ui/main_window.py) | `canvas.node_double_clicked` 信号无人监听 |
| display_name 未存储 | [canvas.py:46-48](file:///d:/Code/jiedian_tool/workflow_engine/ui/canvas.py#L46-L48) | `NodeGraphicsItem.__init__` 用完 display_name 就丢弃，未存为属性 |

## 修改内容

### 1. `workflow_engine/ui/canvas.py` — 三处改动

#### A. 新增节点类型→中文名映射（文件顶部，紧跟 `NODE_TYPE_TO_CATEGORY` 之后）

```python
NODE_TYPE_DISPLAY_NAMES = {
    "manual_input": "手动输入", "timer_trigger": "定时触发",
    "file_watcher": "文件监听", "webhook": "Webhook",
    "logger": "日志输出", "file_writer": "文件写入", "http_request": "HTTP请求",
    "condition": "条件分支", "loop": "循环执行", "sub_workflow": "子流程",
    "transform": "数据转换", "filter": "数据过滤",
    "agent": "AI Agent", "llm_call": "LLM调用",
}
```

与 [node_panel.py 的 NODE_CATEGORIES](file:///d:/Code/jiedian_tool/workflow_engine/ui/node_panel.py#L9-L21) 保持同步。

#### B. `NodeGraphicsItem.__init__` 存储 `display_name`（L30-34 之后）

在 `self.category = category` 后新增一行：

```python
self.display_name = display_name or node_type
```

#### C. `WorkflowCanvas.dropEvent` 传入 display_name（L356）

```python
# 改前：
self.add_node(node_id, node_type, scene_pos.x(), scene_pos.y())

# 改后：
display_name = NODE_TYPE_DISPLAY_NAMES.get(node_type, node_type)
self.add_node(node_id, node_type, scene_pos.x(), scene_pos.y(), display_name)
```

---

### 2. `workflow_engine/ui/main_window.py` — 两处改动

#### A. 绑定双击信号（紧跟 `self.canvas = WorkflowCanvas()` 之后，L33 附近）

```python
self.canvas = WorkflowCanvas()
self.canvas.node_double_clicked.connect(self._on_node_double_clicked)
```

#### B. 新增处理方法（类末尾）

```python
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
```

## 假设与决策

- 只修改 canvas.py 和 main_window.py，不动 node_panel.py 和 property_panel.py
- 映射表在 canvas.py 中重复一份（避免跨模块循环引用），与 node_panel.py 保持内容一致
- 双击行为：填充属性面板即可，不额外弹窗也不自动滚动
- 属性面板的 config 传空 dict，让 property_panel 使用其内置默认值
- 首次拖入的节点 config 为空，用户在属性面板编辑后点"保存配置"触发 `config_changed`（该信号暂未在任何地方处理，属于后续需求）

## 验证步骤

1. 启动应用 `python -m workflow_engine.main`
2. 从节点面板拖入各类节点（输入/输出/流程/数据/AI）到画布
3. 确认拖入的节点显示中文名称（如"手动输入"而非"manual_input"）
4. 双击画布上的节点，确认右侧属性面板显示该节点的 ID、类型、名称和配置项
5. 在属性面板中修改配置值，点击"保存配置"不报错
