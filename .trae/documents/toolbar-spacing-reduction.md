# 工具栏按钮间距缩小计划

## 摘要

将工具栏按钮之间的间距从 4px 缩小到 2px，同时缩小按钮内部边距和最小宽度，使工具栏整体更紧凑。

## 当前状态分析

工具栏间距由两个 QSS 文件控制：

| 属性 | 文件 | 行号 | 当前值 | 作用 |
|------|------|------|--------|------|
| `QToolBar spacing` | `base.qss` | L241 | `4px` | 按钮之间水平间距 |
| `QToolButton padding` | `main_window.qss` | L8 | `4px 6px` | 按钮内部边距 |
| `QToolButton min-width` | `main_window.qss` | L9 | `52px` | 按钮最小宽度 |

## 修改内容

### 1. `workflow_engine/ui/styles/base.qss` (L241)

**改什么：** `QToolBar` 的 `spacing`

**改前：**
```css
spacing: 4px;
```

**改后：**
```css
spacing: 2px;
```

**为什么：** 用户需求——按钮间距减半，从 4px 到 2px。

---

### 2. `workflow_engine/ui/styles/main_window.qss` (L8-L9)

**改什么：** `QToolBar QToolButton` 的 `padding` 和 `min-width`

**改前：**
```css
padding: 4px 6px;
min-width: 52px;
```

**改后：**
```css
padding: 2px 4px;
min-width: 44px;
```

**为什么：** 用户要求按钮也一起缩小。padding 从 `4px 6px` → `2px 4px`（减半），min-width 从 `52px` → `44px`（缩小约15%），使按钮整体更紧凑但文字仍然完整显示。

## 假设与决策

- 只修改 QSS 样式表，不修改 Python 代码
- min-width 从 52px → 44px，确保"运行/暂停/停止/单步/重置"等中文双字标签仍能完整显示
- 不影响工具栏分隔线（`QToolBar::separator`）的间距

## 验证步骤

1. 启动应用 `python -m workflow_engine.main`
2. 目视检查工具栏按钮之间间距是否明显缩小
3. 确认按钮文字（运行、暂停、停止、单步、重置）完整显示、无截断
4. 确认按钮 hover 和点击交互正常
5. 确认工具栏分隔线仍然可见且位置正常
