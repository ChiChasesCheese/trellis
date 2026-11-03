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

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定数据模型（场景图、`Op`）和接口 |
| 8–15 分 | 画整体设计：指针事件 → 按帧预览 → 提交 → 批量同步 |
| 15–45 分 | 写核心实现：`Op`、`Document`、`History`、`OpBuffer`、`DragTool` |
| 45–50 分 | 跑例子：拖动 100 个事件、抬起、撤销 |
| 50–60 分 | 追问：协作冲突、渲染、持久化与离线、笔迹简化 |

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
  - `History`：撤销与重做栈，元素是「一次手势的一组 (正向, 逆向) 操作」。
  - `OpBuffer`：待发送操作缓冲，按 (节点, 属性) 合并。
  - `Tool` 状态机：`SelectTool`、`DragTool`、`PenTool`，处理指针按下、移动、抬起。
  - `Renderer`：根据脏区域重绘（Canvas 2D 或 WebGL）。
  - `SyncClient`：与服务器通过 WebSocket 交换操作批。
- 对外接口：
  - 本地 API：`tool.on_pointer_down/move/up`、`doc.apply`、`history.undo/redo`。
  - 网络消息：`{type:"ops", clientSeq, ops:[...]}` 上行，`{type:"ack", clientSeq, serverSeq}` 与带全局顺序的广播下行；`{type:"presence", ...}` 传递光标位置和拖拽中的瞬时状态。
  - REST：`GET /documents/{id}` 取快照加增量，`POST /documents/{id}/export` 导出为位图或 SVG。

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
1. 输入：指针事件进入当前工具，工具只更新「最新位置」；浏览器每帧回调（`requestAnimationFrame`）调用一次 `on_frame`，把一帧内的多个事件合并为一次预览更新。
2. 预览：修改场景图后标记脏区域（受影响对象包围盒的并集），渲染器只重绘脏区域。
3. 提交：抬起时生成一组操作，写入撤销栈并放入发送缓冲。
4. 同步：`SyncClient` 每 50 到 100 毫秒把缓冲里的操作作为一个批次发出，服务器排序并广播，客户端用序号确认；未确认的批次在重连后重发，按 `(clientId, clientSeq)` 去重。
5. 模型始终是矢量；位图只出现在屏幕渲染和导出时。

**核心实现。** 89 行，写 `DragTool` 一个工具就够了。所有功能最终都是「对节点属性的赋值」，统一成可序列化的 `Op` 之后，撤销、同步、持久化、协作共用同一条管道。用到的模式：命令模式（操作加逆操作）、状态模式（工具状态机）、场景图（组合模式）。

```python
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
        self._start = self._origin = self._latest = (0.0, 0.0)

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

**运行。**

```python
doc = Document(); hist = History(doc); out = OpBuffer(); tool = DragTool(doc, hist, out)
doc.apply(Op("r1", "x", 100)); doc.apply(Op("r1", "y", 50))
tool.on_pointer_down("r1", 10, 10)
for i in range(1, 101):                # 100 个指针事件，每 10 个一帧
    tool.on_pointer_move(10 + i, 10 + i // 2)
    if i % 10 == 0:
        tool.on_frame()
```

- 拖动中 → 节点在 `{'x': 200, 'y': 100}`，撤销栈 0 步，待发送 0 条。
- 抬起 → 撤销栈 1 步；`out.flush()` 得到 2 个 `Op`（`x = 200`、`y = 100`），不是 100 个。
- 撤销 → 回到 `{'x': 100, 'y': 50}`。

**复杂度。** 每帧预览 `O(1)`；提交 `O(改动的属性数)`；缓冲大小不超过「被改过的 (节点, 属性) 数」。

**逐步扩展。**
1. 【追问再讲】重做：撤销栈里弹出来的分组放进了重做栈，补一个 `redo` 回放正向操作；新提交会清空重做栈（`commit` 里已有）。

```python
def redo(self) -> list[Op]:  # History
    if not self._redo:
        return []
    fwd, inv = self._redo.pop()
    for op in fwd:
        self.doc.apply(op)
    self._undo.append((fwd, inv))
    return fwd
```

撤销一次再重做 → 节点回到拖动后的位置，再重做一次返回 `[]`。

2. 【加分】自由笔迹：点流太密，抬起时用 Ramer-Douglas-Peucker 简化折线（再拟合贝塞尔曲线，这里不写）。

```python
import math

def simplify(points: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
    """找离首尾连线最远的点，超过 eps 就保留并递归两边。"""
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    length = math.hypot(x2 - x1, y2 - y1) or 1e-9
    dists = [abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / length for x, y in points[1:-1]]
    i = max(range(len(dists)), key=dists.__getitem__)
    if dists[i] <= eps:
        return [points[0], points[-1]]
    left = simplify(points[: i + 2], eps)
    return left[:-1] + simplify(points[i + 1 :], eps)
```

299 个点（一段带抖动的水平线加一段斜线）`eps = 0.5` → 4 个点。

**深入。**
1. 【必讲】预览与提交分离，高频事件按帧合并。
   - 逐事件处理：每个鼠标事件都改模型、重绘、发网络，CPU 和带宽都爆。指针事件可达每秒 120 到 240 次，渲染预算是 60 帧每秒、单帧约 16 毫秒。
   - 按帧合并（选用）：`on_pointer_move` 只记最新位置，每帧 `on_frame` 处理一次；位移按相对起点的绝对值计算，卡顿时丢掉中间事件也不会漂移。
   - 瞬时与持久：拖拽中的 100 个中间位置写进操作日志就是垃圾。光标、拖拽中的对象位置、选框只经在线状态（presence）通道转发，不进历史；提交后的操作才进撤销栈、操作日志和服务器。

2. 【必讲】撤销与重做。
   - 命令模式：每个提交保存正向和逆向操作，撤销就是按相反顺序回放逆向操作。
   - 一次手势一个分组，避免撤销 100 次才回到拖拽前。
   - 协作场景下，撤销只撤销自己的操作，而且是「产生新的逆向操作并同步」，不是回退全局历史，否则会抹掉别人的修改。

3. 【必讲】批量同步。
   - `OpBuffer` 按 (节点, 属性) 合并，同一键只保留最新值；每 50 到 100 毫秒一个批次，服务器排序后广播，客户端用序号确认。
   - 重连后未确认批次重发，按 `(clientId, clientSeq)` 去重。
   - 拖拽中的瞬时状态以 20 到 30 次每秒经 presence 广播，不持久化，丢包无所谓。

4. 【追问再讲】协作冲突。
   - 属性级「后写者胜」：两人改同一对象的同一属性，服务器接收顺序决定最终值；改不同属性则两者都保留，比锁整个对象冲突少。
   - 服务器忽略指向已删除节点的属性操作。
   - 层级移动可能成环（A 放入 B 的同时 B 放入 A）：服务器检测并拒绝，客户端回滚。
   - 不需要 OT 或 CRDT；文本编辑才需要更复杂的算法。

5. 【追问再讲】渲染与空间索引。
   - 脏区域重绘：只重画变化部分；拖拽的对象单独一层，静态内容分块（tile）缓存。
   - 命中测试和视口剔除用空间索引（四叉树或 R 树），不遍历全部节点。
   - 缩得很小时把子树渲染成位图做低细节缓存。

6. 【追问再讲】持久化与离线。
   - 服务器保存操作日志加周期性快照；新客户端加载最近快照再追放增量。
   - 离线时本地继续累计操作，重连时批量发送，同属性被别人改过则以服务器顺序为准。这就是本地优先（local-first）。

7. 【加分】自由笔迹：用 Ramer-Douglas-Peucker 简化折线再拟合成贝塞尔曲线，路径数据量降一个数量级，缩放不失真。笔迹绘制中本地实时显示，抬起时才简化并提交。位图笔刷是栅格图层，同步的是瓦片变更，代价大得多，产品上要限制尺寸。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 为什么不每个鼠标事件都发给服务器：带宽与服务器压力高，大部分是无意义的中间状态；批量、合并加提交语义足够，瞬时状态通道保证协作者看到流畅的移动。
- 用 OT 还是 CRDT：中心服务器排序加属性级后写者胜，实现简单，足以满足图形编辑。
- 精度与单位：坐标用浮点，变换用 2×3 矩阵；缩放后保持矢量精度，导出时再按目标分辨率栅格化。

**级别期望。**
- 中级：场景图数据模型、拖拽事件到更新节点位置的流程、命令式撤销；核心实现能跑通拖动和撤销。
- 高级：按帧合并事件、预览与提交分离、操作批量发送并按属性合并、脏区域渲染。
- 资深（staff）：协作冲突的属性级处理与分数索引排序、presence 通道设计、重连与幂等、自由笔迹的简化与拟合、大文档的渲染与空间索引、撤销在多人场景下的语义。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-system-design-core-concepts-networking-essentials|网络基础]]、[[hi-system-design-patterns-realtime-updates|实时更新]]

**同类题。** [[hi-system-design-in-the-wild-figma-multiplayer|Figma 多人编辑与简化 CRDT]]、[[hi-system-design-problem-breakdowns-google-docs|协同文档（Google Docs）]]、[[solution-google-docs]]、[[solution-text-editor]]
