# VS Code Dark+ 主题统一 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将工作流引擎 UI 从「复古工业风 × 赛博朋克暖光」完全切换到 VS Code Dark+ 风格，统一所有硬编码颜色。

**Architecture:** 修改 `theme.py` 颜色常量（驱动 QSS 变量），替换 `canvas.py`/`node_panel.py` 中硬编码颜色，修复 `log_panel.qss`/`property_panel.qss`/`node_panel.qss` 中仍硬编码的颜色改用 `@variable`。

**Tech Stack:** Python 3.12 + PySide6 + QSS

---

## 文件清单

| 文件 | 操作 | 职责 |
|------|------|------|
| `workflow_engine/ui/styles/theme.py` | 修改 L34-46 | 替换 `'dark'` 主题颜色常量 |
| `workflow_engine/ui/styles/log_panel.qss` | 修改 | 硬编码色 → `@variable` |
| `workflow_engine/ui/styles/property_panel.qss` | 修改 | 硬编码色 → `@variable` |
| `workflow_engine/ui/styles/node_panel.qss` | 修改 | 硬编码色 → `@variable` |
| `workflow_engine/ui/canvas.py` | 修改 L10-17, L48-126, L221-224 | 替换 NODE_COLORS、高亮色、文字色、右键菜单 QSS |
| `workflow_engine/ui/node_panel.py` | 修改 L8-19, L54 | 替换 NODE_CATEGORIES 颜色、文字色 |
| `workflow_engine/ui/main_window.py` | 修改 L165-166 | 状态栏背景改为蓝色 |

---

## Task 1: 替换 theme.py 颜色常量 + 修复 QSS 硬编码色

**Files:**
- 修改: `workflow_engine/ui/styles/theme.py`
- 修改: `workflow_engine/ui/styles/log_panel.qss`
- 修改: `workflow_engine/ui/styles/property_panel.qss`
- 修改: `workflow_engine/ui/styles/node_panel.qss`

- [ ] **Step 1: 修改 `theme.py` L34-46 颜色常量**

将 `THEMES['dark']['colors']` 中的 4 个变量替换：

```python
'colors': {
    'primary': '#007ACC',        # 曾: #E8A87C (琥珀) → VS Code 蓝
    'secondary': '#094771',      # 曾: #C38D9E (珊瑚) → VS Code 深蓝
    'accent': '#0098FF',          # 曾: #F5C07A (暖黄) → VS Code 亮蓝
    'background': '#1E1E1E',      # 不变
    'surface': '#2D2D2D',        # 不变
    'text': '#D4D4D4',           # 曾: #E0D8D0 (暖白) → VS Code 中性白
    'text_secondary': '#8A8A8A',  # 不变
    'border': '#3C3C3C',          # 不变
    'error': '#F14C4C',           # 不变
    'success': '#5CB85C',         # 不变
    'warning': '#DCDCAA',         # 不变
}
```

- [ ] **Step 2: 修复 `log_panel.qss` 硬编码色**

```css
/* log_panel.qss — 日志面板样式 */

#log_panel_container {
    background-color: @background;
    border-top: 1px solid @border;
}

#log_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: @text;
    padding: 8px 12px;
    border-bottom: 1px solid @border;
    border-left: 3px solid @primary;
}
```

- [ ] **Step 3: 修复 `property_panel.qss` 硬编码色**

```css
/* property_panel.qss — 属性面板样式 */

#property_panel_container {
    background-color: @surface;
    border-left: 1px solid @border;
}

#property_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: @text;
    padding: 10px 12px 8px;
    border-bottom: 1px solid @border;
    border-left: 3px solid @primary;
}
```

- [ ] **Step 4: 修复 `node_panel.qss` 硬编码色**

```css
/* node_panel.qss — 节点面板网格卡片样式 */

#node_panel_container {
    background-color: @surface;
    border-right: 1px solid @border;
}

#node_panel_title {
    font-size: 14px;
    font-weight: bold;
    color: @text;
    padding: 10px 12px 8px;
    border-bottom: 1px solid @border;
    border-left: 3px solid @primary;
}

NodeCard {
    background-color: @background;
    border: 1px solid @border;
    border-radius: 6px;
    border-left-width: 3px;
    min-width: 90px;
    min-height: 70px;
}
NodeCard:hover {
    border-color: @primary;
    background-color: @surface;
}
```

- [ ] **Step 5: 测试运行**

```bash
cd d:\Code\jiedian_tool
python -c "from workflow_engine.ui.styles import load_stylesheet; s=load_stylesheet(); print(s[:100])"
```
预期: 无报错。

- [ ] **Step 6: 提交**

```bash
git add workflow_engine/ui/styles/theme.py workflow_engine/ui/styles/log_panel.qss workflow_engine/ui/styles/property_panel.qss workflow_engine/ui/styles/node_panel.qss
git commit -m "feat(ui): 切换到VS Code Dark+颜色主题，QSS统一使用变量"
```

---

## Task 2: 替换 canvas.py 硬编码颜色

**Files:**
- 修改: `workflow_engine/ui/canvas.py`

- [ ] **Step 1: 替换 NODE_COLORS（L10-17）为降饱和版本**

```python
NODE_COLORS = {
    "input": {"primary": "#6A9EC9", "secondary": "#4A7EA9"},
    "output": {"primary": "#7A9E6B", "secondary": "#5A7E4B"},
    "flow": {"primary": "#C8A080", "secondary": "#A88060"},
    "data": {"primary": "#B0A07A", "secondary": "#90805A"},
    "ai": {"primary": "#9A7AAA", "secondary": "#7A5A8A"},
    "default": {"primary": "#6A9EC9", "secondary": "#4A7EA9"},
}
```

- [ ] **Step 2: 替换文字颜色（L48, L53）**

```python
text.setDefaultTextColor(QColor("#D4D4D4"))       # 曾: #E0D8D0
type_label.setDefaultTextColor(QColor("#D4D4D480")) # 曾: #E0D8D080
```

- [ ] **Step 3: 替换端口颜色（L58, L62）**

```python
self.input_port.setBrush(QBrush(QColor("#7A9E6B")))   # 曾: #5CB85C
self.input_port.setPen(QPen(QColor("#5A7E4B"), 1))    # 曾: #3D8B3D
self.output_port.setBrush(QBrush(QColor("#E74C3C")))  # 不变
```

- [ ] **Step 4: 替换状态发光色（L82-83, L87-88）**

```python
elif state == "success":
    self._stop_pulse()
    self.glow_effect.setBlurRadius(15)
    self.glow_effect.setColor(QColor("#7A9E6B60"))  # 曾: #5CB85C60
    self.setPen(QPen(QColor("#7A9E6B"), 2))         # 曾: #5CB85C
elif state == "error":
    self._stop_pulse()
    self.glow_effect.setBlurRadius(15)
    self.glow_effect.setColor(QColor("#E74C3C60"))   # 不变
    self.setPen(QPen(QColor("#E74C3C"), 2))          # 不变
```

- [ ] **Step 5: 替换选中/悬停高亮色（L119-126）**

```python
def set_selected(self, selected: bool):
    if selected:
        self.setPen(QPen(QColor("#007ACC"), 2))          # 曾: #E8A87C
        self.glow_effect.setBlurRadius(10)
        self.glow_effect.setColor(QColor("#007ACC40"))   # 曾: #E8A87C40
    else:
        self.set_state(self.node_state)

def hoverEnterEvent(self, event):
    self.setPen(QPen(QColor("#007ACC"), 1))              # 曾: #E8A87C
    super().hoverEnterEvent(event)
```

- [ ] **Step 6: 替换右键菜单 QSS 硬编码色（L221-224）**

```python
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
```

- [ ] **Step 7: 测试**

```bash
cd d:\Code\jiedian_tool
python -c "from workflow_engine.ui.canvas import NodeGraphicsItem, NODE_COLORS; print(NODE_COLORS['flow']['primary'])"
```
预期: `#C8A080`

- [ ] **Step 8: 提交**

```bash
git add workflow_engine/ui/canvas.py
git commit -m "feat(ui): canvas切换VS Code Dark+色系+降饱和节点颜色"
```

---

## Task 3: 替换 node_panel.py 硬编码颜色 + main_window.py 状态栏

**Files:**
- 修改: `workflow_engine/ui/node_panel.py`
- 修改: `workflow_engine/ui/main_window.py`

- [ ] **Step 1: 替换 node_panel.py NODE_CATEGORIES 颜色（L8-19）**

```python
NODE_CATEGORIES = {
    "输入": {"color": "#6A9EC9", "category_key": "input", "nodes": [
        ("manual_input", "手动输入"), ("timer_trigger", "定时触发"),
        ("file_watcher", "文件监听"), ("webhook", "Webhook")]},
    "输出": {"color": "#7A9E6B", "category_key": "output", "nodes": [
        ("logger", "日志输出"), ("file_writer", "文件写入"), ("http_request", "HTTP请求")]},
    "流程控制": {"color": "#C8A080", "category_key": "flow", "nodes": [
        ("condition", "条件分支"), ("loop", "循环执行"), ("sub_workflow", "子流程")]},
    "数据处理": {"color": "#B0A07A", "category_key": "data", "nodes": [
        ("transform", "数据转换"), ("filter", "数据过滤")]},
    "AI": {"color": "#9A7AAA", "category_key": "ai", "nodes": [
        ("agent", "AI Agent"), ("llm_call", "LLM调用")]},
}
```

- [ ] **Step 2: 替换 node_panel.py 文字色（L54）**

```python
name_label.setStyleSheet("font-size: 10px; color: #D4D4D4; background: transparent; font-weight: bold;")
```

- [ ] **Step 3: 修改 main_window.py 状态栏背景（L165-166）**

```python
def _setup_statusbar(self):
    self.statusBar().showMessage("就绪")
    self.statusBar().setStyleSheet(
        "QStatusBar { background-color: #007ACC; color: #FFFFFF; font-weight: bold; }"
    )
```

- [ ] **Step 4: 最终整合测试**

```bash
cd d:\Code\jiedian_tool
python -m workflow_engine.main
```

验证清单：
- [ ] 菜单悬停 → 蓝底 `#094771`
- [ ] 工具栏按钮悬停 → 蓝底
- [ ] 状态栏 → 蓝色底 `#007ACC`
- [ ] 面板标题左边框 → 蓝色 `#007ACC`
- [ ] 节点画布选中 → 蓝色发光
- [ ] 节点分类色 → 降饱和（柔和不刺眼）
- [ ] 右键菜单选中 → 蓝底
- [ ] 应用正常启动，无崩溃

- [ ] **Step 5: 提交**

```bash
git add workflow_engine/ui/node_panel.py workflow_engine/ui/main_window.py
git commit -m "feat(ui): 节点面板+状态栏切换VS Code Dark+色系"
```

---

## 验收清单

- [ ] Task 1: theme.py 颜色常量已替换为 VS Code Blue 系
- [ ] Task 1: log_panel.qss / property_panel.qss / node_panel.qss 全部使用 @variable
- [ ] Task 2: NODE_COLORS 降饱和 40%
- [ ] Task 2: 节点选中/悬停改为蓝色发光
- [ ] Task 2: 右键菜单选中改为蓝底
- [ ] Task 3: NODE_CATEGORIES 颜色降饱和
- [ ] Task 3: 状态栏蓝色背景 `#007ACC`
- [ ] 整合: 应用正常启动，全部颜色统一为 VS Code Dark+ 风格
