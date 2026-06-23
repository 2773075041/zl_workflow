# 画布节点名称不显示 — 根因修复计划

## 根因分析

**问题：** 拖入画布后节点不显示中文名称（如"手动输入"）。

**数据流验证（✅ 正确）：**
```
drag → dropEvent: NODE_TYPE_DISPLAY_NAMES["manual_input"] = "手动输入"
     → add_node("手动输入") → NodeGraphicsItem("手动输入")
     → L57: text.setPlainText("手动输入")
```

**真实根因：** [canvas.py:L79-L83](file:///d:/Code/jiedian_tool/workflow_engine/ui/canvas.py#L79-L83) — 父级 `QGraphicsRectItem` 上设置了 `QGraphicsDropShadowEffect`（即使 blurRadius=0 + 透明色 + 零偏移）：

```python
self.glow_effect = QGraphicsDropShadowEffect()
self.glow_effect.setBlurRadius(0)
self.glow_effect.setColor(QColor(self.primary_color + "00"))  # 完全透明
self.glow_effect.setOffset(0, 0)
self.setGraphicsEffect(self.glow_effect)
```

**机理：** PySide6/Qt6 中，当父级 QGraphicsItem 被设置了 QGraphicsEffect（即使是"空"的），Qt 切换到离屏渲染管线：
1. `drawSource()` 只渲染父项的 `paint()`（填充矩形+边框）到离屏缓冲
2. 子项 `QGraphicsTextItem` 不被纳入该离屏缓冲
3. Scene 合成时，effect 的离屏结果遮挡了子文本项

**旁证：** 端口（`QGraphicsEllipseItem`）通常还能看到，因为它们渲染在节点边界之外（左端口 x=-6，右端口 x=134+），部分避开了离屏缓冲覆盖区。文字在节点中央（x=12, y=30），恰好在被遮挡的核心区域。

## 修复方案

**用独立的 `QGraphicsRectItem` 叠加层替代 `QGraphicsDropShadowEffect`。**

- 移除所有 `QGraphicsDropShadowEffect` 相关代码
- 新增一个子 `QGraphicsRectItem`（`glow_overlay`），比节点略大、置于节点背后（`ItemStacksBehindParent`）
- 通过对 `glow_overlay` 的 brush 颜色和透明度进行状态切换/动画，实现等价的发光效果

## 修改内容

### 文件：`workflow_engine/ui/canvas.py`

#### 1. `NodeGraphicsItem.__init__` — 删除 effect，新增 glow_overlay

**删除 L79-L83（4 行）：**
```python
self.glow_effect = QGraphicsDropShadowEffect()
self.glow_effect.setBlurRadius(0)
self.glow_effect.setColor(QColor(self.primary_color + "00"))
self.glow_effect.setOffset(0, 0)
self.setGraphicsEffect(self.glow_effect)
```

**在 L65 之后（`type_label.setPos(12, height / 2 + 6)` 之后）新增：**
```python
self.glow_overlay = QGraphicsRectItem(-8, -8, width + 16, height + 16, self)
self.glow_overlay.setPen(QPen(Qt.NoPen))
self.glow_overlay.setBrush(QBrush(QColor(0, 0, 0, 0)))
self.glow_overlay.setZValue(-1)
```

**同时移除 import 中的 `QGraphicsDropShadowEffect`（L1）：**
```python
# 改前：
from PySide6.QtWidgets import ..., QGraphicsDropShadowEffect, QMenu
# 改后：
from PySide6.QtWidgets import ..., QMenu
```

#### 2. `set_state()` — 用 glow_overlay 替代 glow_effect

**完整替换 L85-L102：**
```python
def set_state(self, state: str):
    self.node_state = state
    if state == "idle":
        self.glow_overlay.setBrush(QBrush(QColor(0, 0, 0, 0)))
        self.setPen(QPen(QColor(self.secondary_color), 1))
    elif state == "running":
        self._start_pulse()
    elif state == "success":
        self._stop_pulse()
        self.glow_overlay.setBrush(QBrush(QColor("#7A9E6B40")))
        self.setPen(QPen(QColor("#7A9E6B"), 2))
    elif state == "error":
        self._stop_pulse()
        self.glow_overlay.setBrush(QBrush(QColor("#E74C3C40")))
        self.setPen(QPen(QColor("#E74C3C"), 2))
```

#### 3. `_pulse_step()` — 用 glow_overlay brush 替代 glow_effect blurRadius

**替换 L104-L125：**
```python
def _pulse_step(self):
    import math
    self._pulse_phase += 0.1
    r1, g1, b1 = self._hex_to_rgb(self.secondary_color)
    r2, g2, b2 = 245, 192, 122
    t = (math.sin(self._pulse_phase) + 1) / 2
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    alpha = int(30 + 60 * t)
    self.glow_overlay.setBrush(QBrush(QColor(r, g, b, alpha)))
    self.setPen(QPen(QColor(r, g, b), 2))
```

#### 4. `_stop_pulse()` — 重置 glow_overlay

**替换 L110-L112：**
```python
def _stop_pulse(self):
    if hasattr(self, "_pulse_timer"):
        self._pulse_timer.stop()
```

不需要额外重置 glow_overlay，因为调用 `_stop_pulse()` 之后总是紧跟着设置新状态（success/error/idle），新状态会设置正确的 brush。

#### 5. `set_selected()` — 用 glow_overlay 替代 glow_effect

**替换 L131-L137：**
```python
def set_selected(self, selected: bool):
    if selected:
        self.setPen(QPen(QColor("#007ACC"), 2))
        self.glow_overlay.setBrush(QBrush(QColor("#007ACC30")))
    else:
        self.set_state(self.node_state)
```

#### 6. 清理 `__pycache__`

清除旧 `.pyc` 缓存，避免加载旧的、带 `QGraphicsDropShadowEffect` 的字节码。

### 同时验证 `node_panel.py` 的 import

确认 `node_panel.py` 中 `QGraphicsDropShadowEffect` 仅用于 `NodeCard`（面板卡片），不受本次修改影响。

## 假设与决策

- `QGraphicsRectItem` 作为 glow 叠加层足够满足发光效果需求（不需要圆形或圆角）
- 叠加层比节点大 16px（每边多 8px），形成视觉光晕
- `ItemStacksBehindParent` 确保叠加层在节点背后，不遮挡文字
- 移除 import 中的 `QGraphicsDropShadowEffect` 后，`node_panel.py` 仍有自己的 import，不受影响
- 清理 `.pyc` 是预防措施，应对可能的字节码缓存问题

## 验证步骤

1. 删除 `__pycache__` 目录中的旧缓存文件
2. 启动应用 `python -m workflow_engine.main`
3. 从节点面板拖入任意节点到画布，确认节点上显示中文名称
4. 拖入所有 14 种节点类型，确认每种都显示对应中文名
5. 双击节点，确认右侧属性面板加载节点信息
6. 选中节点，确认出现蓝色发光叠加层
7. 点击"运行"按钮（如果可用），确认运行状态有脉冲发光
8. 检查控制台无报错
