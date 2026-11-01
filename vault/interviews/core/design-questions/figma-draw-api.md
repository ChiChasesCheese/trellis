---
slug: figma-draw-api
kind: low-level-design
---

## Q
**矢量图形编辑器的绘图 API（类 Figma）**｜低层设计

设计一个矢量图形编辑器（类似 Figma）的绘图接口和内部架构：用户拖动鼠标或触控笔时会产生大量拖拽事件，要怎样高效地批处理这些事件，把它们转换成屏幕上的像素或矢量形状，并最终"提交"成持久的绘图操作。要求讲清楚整体架构、数据模型、操作如何提交（包括撤销重做、与服务器同步的批量发送）。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 核心是把"手势过程中的瞬时预览"和"手势结束时的持久提交"分开：高频指针事件只驱动本地预览和渲染（每帧最多处理一次），只有提交的操作才进入撤销栈、持久化和协作同步，并且按（对象, 属性）合并后批量发送。

**需求。**
- 功能：
  1. 工具：选择、移动、缩放、画矩形或椭圆、钢笔或自由画笔绘制路径。
  2. 拖拽时实时预览，抬起时提交为一次操作。
  3. 撤销与重做，一次手势对应一步。
  4. 文档保存，与服务器和协作者同步。
- 非功能：
  - 交互帧率 60 帧每秒，单帧预算约 16 毫秒；指针事件频率可达 120 到 240 次每秒。
  - 本地优先（local-first）：用户操作立即生效，网络不阻塞绘制。
  - 画布含数万个对象时仍能流畅平移缩放。
  - 同步带宽可控：拖拽一个对象 1 秒不应发送 100 多条网络消息。

**核心实体与接口。**
- 数据模型（场景图，scene graph）：
  - `Document` 含多个 `Page`；页面是节点树。`Node`：id、类型（Frame、Rect、Ellipse、Path、Text）、父节点、排序键、变换（位置、缩放、旋转）、样式（填充、描边）、路径数据（矢量命令序列）。
  - 节点 ID 由客户端生成（`clientId:自增序号`），离线或乐观创建时无需等待服务器。
  - 同级顺序用分数索引（fractional index，一个可无限细分的字符串），两个人同时在同一位置插入也不会冲突，不需要重排整个列表。
- 操作（Op）：对某个节点的某个属性赋值 `(node_id, prop, value)`，加上客户端序号。创建与删除也是特殊操作。
- 主要类：
  - `Document`：持有节点，`apply(op)` 修改并返回逆操作。
  - `History`：撤销与重做栈，元素是"一次手势的一组 (正向, 逆向) 操作"。
  - `OpBuffer`：待发送操作缓冲，按 (节点, 属性) 合并。
  - `Tool` 状态机：`SelectTool`、`DragTool`、`PenTool`，处理指针按下、移动、抬起。
  - `Renderer`：根据脏区域重绘（Canvas 2D 或 WebGL）。
  - `SyncClient`：与服务器通过 WebSocket 交换操作批。
- 对外接口：
  - 本地 API：`tool.on_pointer_down/move/up`、`doc.apply`、`history.undo/redo`。
  - 网络消息：`{type:"ops", clientSeq, ops:[...]}` 上行，`{type:"ack", clientSeq, serverSeq}` 与带全局顺序的广播下行；`{type:"presence", ...}` 传递光标位置和拖拽中的瞬时状态。
  - REST：`GET /documents/{id}` 取快照加增量，`POST /documents/{id}/export` 导出为位图或 SVG。

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Op:
    node_id: str
    prop: str                  # 例如 "x"、"y"、"fill"
    value: Any


class Document:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}

    def apply(self, op: Op) -> Op:
        """应用一个操作，返回它的逆操作（旧值），供撤销使用。"""
        node = self.nodes.setdefault(op.node_id, {})
        old = node.get(op.prop)
        node[op.prop] = op.value
        return Op(op.node_id, op.prop, old)


class History:
    """一次手势 = 一个分组 = 撤销栈里的一步，而不是每个鼠标事件一步。"""
    def __init__(self, doc: Document) -> None:
        self.doc, self._undo, self._redo = doc, [], []

    def commit(self, forward: list[Op], inverse: list[Op]) -> None:
        self._undo.append((forward, inverse))
        self._redo.clear()                     # 新提交会使重做失效

    def undo(self) -> list[Op]:
        if not self._undo:
            return []
        fwd, inv = self._undo.pop()
        for op in reversed(inv):               # 逆操作按相反顺序回放
            self.doc.apply(op)
        self._redo.append((fwd, inv))
        return list(reversed(inv))             # 返回需要同步的操作


class OpBuffer:
    """待发送缓冲：同一 (节点, 属性) 只保留最新值，批量发出。"""
    def __init__(self) -> None:
        self._pending: dict[tuple[str, str], Op] = {}

    def add(self, op: Op) -> None:
        self._pending[(op.node_id, op.prop)] = op   # 后写覆盖先写

    def flush(self) -> list[Op]:
        ops, self._pending = list(self._pending.values()), {}
        return ops


class DragTool:
    def __init__(self, doc: Document, history: History, out: OpBuffer) -> None:
        self.doc, self.history, self.out = doc, history, out
        self._node: str | None = None
        self._start: tuple[float, float] = (0, 0)
        self._origin: tuple[float, float] = (0, 0)
        self._latest: tuple[float, float] = (0, 0)

    def on_pointer_down(self, node_id: str, x: float, y: float) -> None:
        n = self.doc.nodes[node_id]
        self._node, self._start, self._origin = node_id, (x, y), (n["x"], n["y"])
        self._latest = (x, y)

    def on_pointer_move(self, x: float, y: float) -> None:
        self._latest = (x, y)                  # 只记录最新位置；每帧由 on_frame 统一处理一次

    def on_frame(self) -> None:
        if self._node is None:
            return
        # 相对起点的绝对位移，不累加增量，避免丢事件时漂移
        nx = self._origin[0] + self._latest[0] - self._start[0]
        ny = self._origin[1] + self._latest[1] - self._start[1]
        self.doc.apply(Op(self._node, "x", nx))        # 本地预览：立即改场景，不进撤销栈
        self.doc.apply(Op(self._node, "y", ny))
        # 预览数据只作为瞬时状态按较低频率广播给协作者，这里不放进持久缓冲

    def on_pointer_up(self) -> None:
        if self._node is None:
            return
        self.on_frame()
        n = self.doc.nodes[self._node]
        fwd = [Op(self._node, "x", n["x"]), Op(self._node, "y", n["y"])]
        inv = [Op(self._node, "x", self._origin[0]), Op(self._node, "y", self._origin[1])]
        self.history.commit(fwd, inv)          # 一次手势只提交一组操作
        for op in fwd:
            self.out.add(op)                   # 进入待发送缓冲，下个批次发给服务器
        self._node = None
```

用到的模式：命令模式（操作加逆操作，撤销重做）、状态模式（工具状态机）、观察者模式（文档变化通知渲染器与同步器）、场景图（组合模式）。原因：编辑器的所有功能最终都是"对节点属性的赋值"，把它们统一成可序列化的操作，撤销、同步、持久化、协作就共用同一条管道。

**整体设计。**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 294">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="170" y1="36" x2="170" y2="53"/>
<line x1="170" y1="86" x2="170" y2="103"/>
<line x1="170" y1="136" x2="170" y2="153"/>
<line x1="170" y1="186" x2="170" y2="203"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="8" width="316" height="28" rx="3"/>
<rect x="12" y="58" width="316" height="28" rx="3"/>
<rect x="12" y="108" width="316" height="28" rx="3"/>
<rect x="12" y="158" width="316" height="28" rx="3"/>
<rect x="12" y="208" width="316" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="170,58 167,52 173,52"/>
<polygon points="170,108 167,102 173,102"/>
<polygon points="170,158 167,152 173,152"/>
<polygon points="170,208 167,202 173,202"/>
</g>
<g fill="currentColor">
<text x="170" y="26" font-size="12">指针事件 -> 工具(记最新位置)</text>
<text x="170" y="76" font-size="12">每帧一次: 本地预览 + 脏区重绘</text>
<text x="170" y="126" font-size="12">抬起: 一组 Op 入撤销栈</text>
<text x="170" y="176" font-size="12">OpBuffer 按(节点,属性)合并</text>
<text x="170" y="226" font-size="12">50-100ms 批量发服务器 -> 排序广播</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="252" font-size="11">预览与瞬时状态不进历史</text></g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="268" font-size="11">拖拽过程只广播 presence</text></g>
</g></svg>
```
1. 输入：指针事件进入当前工具，工具只更新"最新位置"；浏览器每帧回调（`requestAnimationFrame`）调用一次 `on_frame`，把一帧内的多个事件合并为一次预览更新。高刷设备上浏览器提供的合并事件（coalesced events）可用于平滑笔迹。
2. 预览：修改场景图后标记脏区域（受影响对象的包围盒的并集），渲染器只重绘脏区域；视口外的对象通过空间索引（四叉树或 R 树）剔除。
3. 提交：抬起时生成一组操作，写入撤销栈并放入发送缓冲。
4. 同步：`SyncClient` 每 50 到 100 毫秒把缓冲里的操作作为一个批次发出，服务器排序并广播，客户端用序号确认；未确认的批次在断线重连后重发，按 `(clientId, clientSeq)` 去重。
5. 渲染产物：模型始终是矢量；位图只出现在屏幕渲染和导出时。位图图片是单独的图片填充节点，不与矢量路径混用。

**深入。**
1. 高频事件的批处理。
   - 逐事件处理：每个鼠标事件都改模型、重绘、发网络，CPU 和带宽都爆。
   - 按帧合并（选用）：事件只更新状态，渲染在每帧一次；卡顿时丢掉中间事件也不影响正确性，因为位移是相对起点的绝对值。
   - 网络层再合并：同一 (节点, 属性) 在批次内只保留最后一个值；拖拽过程的瞬时状态用较低频率（20 到 30 次每秒）广播，且不持久化，丢包无所谓。
2. 瞬时状态与持久状态分离。
   - 拖拽过程中只有手势结束时的位置才有意义，中间的 100 个位置写进操作日志就是垃圾。
   - 瞬时：光标位置、拖拽中的对象位置、选框，只通过在线状态（presence）通道转发，不进历史。
   - 持久：提交后的操作，进入撤销栈、操作日志、服务器。
3. 撤销与重做。
   - 命令模式：每个提交保存正向和逆向操作；撤销就是回放逆向操作。一次手势一个分组，避免撤销 100 次才回到拖拽前。
   - 协作场景下，撤销只撤销自己的操作，而且是"产生新的逆向操作并同步"，不是回退全局历史，否则会抹掉别人的修改。
4. 冲突与顺序。
   - 属性级别的"后写者胜"：两人改同一对象的同一属性，服务器接收顺序决定最终值；改不同属性则两者都保留。比整段文档的锁或整对象覆盖粒度更细，冲突更少。
   - 节点删除与对删除节点的修改：服务器忽略指向已删除节点的属性操作。
   - 层级移动可能成环（A 放入 B 的同时 B 放入 A）：服务器检测并拒绝导致环的移动，客户端回滚。
5. 自由绘制：把点流变成矢量。
   - 采样的点密集，直接存会很大；用 Ramer-Douglas-Peucker 简化折线，再拟合成贝塞尔曲线，路径数据量降低一个数量级，并且缩放不失真。
   - 笔迹在绘制中本地实时显示，抬起时才做简化和提交；简化后的形状与预览略有差别，可以在抬起时做一次平滑过渡。
6. 渲染。
   - 脏区域重绘：只重画变化部分；对象多时用分块（tile）缓存静态内容，拖拽的对象单独一层。
   - 命中测试：点击或框选需要找到鼠标下的对象，用空间索引而不是遍历全部节点。
   - 大文档：只渲染视口内节点，缩小很多时用低细节缓存（把子树渲染成位图）。
7. 持久化。
   - 服务器保存操作日志加周期性快照；新客户端加载最近快照再追放增量。日志也用于恢复和审计。

**取舍与追问。**
- 追问"为什么不每个鼠标事件都发给服务器"：带宽与服务器压力高，且大部分是无意义的中间状态；批量加合并加上提交语义足够，并提供瞬时状态通道保证协作者看到流畅的移动。
- 追问"用 OT 还是 CRDT"：这里用中心服务器排序加属性级后写者胜，实现简单，足以满足图形编辑；文本编辑才需要更复杂的算法。
- 追问"离线编辑"：本地继续累计操作，重连时批量发送；冲突按服务器顺序解决，同属性被别人改过则以服务器顺序为准。
- 追问"位图笔刷（栅格图层）怎么处理"：栅格图层是单独节点，笔画写入位图瓦片，同步的是瓦片变更而不是点序列，代价大得多，需要产品上限制尺寸。
- 追问"精度与单位"：坐标用浮点，变换用 2×3 矩阵；缩放后保持矢量精度，导出时再按目标分辨率栅格化。

**级别期望。**
- 中级：场景图数据模型、拖拽事件到更新节点位置的流程，命令式撤销。
- 高级：按帧合并事件、预览与提交分离、操作批量发送并按属性合并、脏区域渲染。
- 资深（staff）：协作冲突的属性级处理与分数索引排序、presence 通道设计、重连与幂等、自由笔迹的简化与拟合、大文档的渲染与空间索引、撤销在多人场景下的语义。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-system-design-core-concepts-networking-essentials|网络基础]]、[[hi-system-design-patterns-realtime-updates|实时更新]]

**同类题。** [[hi-system-design-in-the-wild-figma-multiplayer|Figma 多人编辑与简化 CRDT]]、[[hi-system-design-problem-breakdowns-google-docs|协同文档（Google Docs）]]、[[solution-google-docs]]、[[solution-text-editor]]
