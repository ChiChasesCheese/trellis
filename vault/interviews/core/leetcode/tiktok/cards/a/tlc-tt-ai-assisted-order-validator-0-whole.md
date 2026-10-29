---
id: tlc-tt-ai-assisted-order-validator-0-whole
node: a.tt-ai-assisted-order-validator
type: qa
---
## Q
**OrderValidator（规则 DAG）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-06（面试记录）

实现 `OrderValidator`：订单要依次通过一组校验规则，规则之间有依赖，构成有向无环图（DAG）；按拓扑顺序执行，被依赖的规则先执行，任一规则失败则订单不通过。接口：`add_rule(name, check, depends_on=())` 添加规则（`check` 接收订单字典、返回布尔值；`depends_on` 只能引用已存在的规则，规则名唯一，否则抛 `ValueError`）；`remove_rule(name)` 删除规则，并把它的所有前驱直接连到它的所有后继上，保持「谁必须先于谁」的关系；`validate(order)` 返回 `(是否通过, 第一个失败的规则名或 None)`，遇到失败立即返回。规则数不超过 `10^4`。例：`auth`；`stock` 依赖 `auth`；`price` 依赖 `auth`；`ship` 依赖 `stock` 和 `price`；订单 `{}` 全部通过，订单 `{"price": False}` 在 `price` 处失败，`ship` 不会被执行。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用两个字典存 DAG：`deps`（规则 → 它依赖的规则）和 `users`（规则 → 依赖它的规则）；`validate` 用标准库 `graphlib.TopologicalSorter(deps).static_order()` 按依赖顺序执行，遇到第一个失败就返回；`remove_rule` 把每个前驱连到每个后继，再删除节点，传递关系保持不变。

**识别。** 「规则有依赖、按依赖顺序执行」是拓扑排序；「删除一个节点但保留它两侧的顺序约束」是图的节点收缩：前驱 × 后继两两连边；「一旦失败整单不通过」说明可以短路。面试里自带 AI 工具时，评分点是可运行的代码加完整的测试，所以要把边界情形和不变量列清楚。

**推导。** 暴力：自己写递归 DFS 带访问标记执行规则，手写环检测，删除规则只删节点 → 浪费：拓扑排序和环检测标准库已提供；只删节点会让原来经过它传递的约束消失（`a -> b -> c` 删掉 `b` 后，`a` 与 `c` 之间不再有约束）→ 洞察：`add_rule` 只允许依赖已存在的规则，图在构造上就无环；删除时前驱到后继的新边不会成环（`p` 在 `name` 之前、`name` 在 `s` 之前本来就成立）；再维护反向边 `users`，删除只需遍历该规则的前驱和后继。

```python
from collections.abc import Callable
from graphlib import TopologicalSorter

Order = dict[str, object]
Rule = Callable[[Order], bool]


class OrderValidator:
    def __init__(self) -> None:
        self._rules: dict[str, Rule] = {}
        self._deps: dict[str, set[str]] = {}       # 规则 -> 它依赖的规则（必须先执行）
        self._users: dict[str, set[str]] = {}      # 规则 -> 依赖它的规则（反向边，删除时要用）

    def add_rule(self, name: str, check: Rule, depends_on: tuple[str, ...] = ()) -> None:
        if name in self._rules:
            raise ValueError(f"rule {name!r} already exists")
        missing = [d for d in depends_on if d not in self._rules]
        if missing:
            raise ValueError(f"unknown dependencies: {missing}")   # 新规则只依赖已有规则，所以不会成环
        self._rules[name] = check
        self._deps[name] = set(depends_on)
        self._users[name] = set()
        for d in depends_on:
            self._users[d].add(name)

    def remove_rule(self, name: str) -> None:
        preds, succs = self._deps.pop(name), self._users.pop(name)   # 不存在时抛 KeyError
        del self._rules[name]
        for p in preds:
            self._users[p].discard(name)
        for s in succs:
            self._deps[s].discard(name)
        for p in preds:                            # 前驱直接连后继：原来 p 先于 s 的约束不能丢
            for s in succs:
                self._deps[s].add(p)
                self._users[p].add(s)

    def validate(self, order: Order) -> tuple[bool, str | None]:
        for name in TopologicalSorter(self._deps).static_order():   # 依赖在前、被依赖者在后
            if not self._rules[name](order):
                return False, name                 # 任一规则失败：订单不通过，并说明是哪条
        return True, None
```

运行：四条规则下 `validate({})` → `(True, None)`，执行顺序 `auth, stock, price, ship`；`validate({"price": False})` → `(False, 'price')`，执行到 `price` 为止；删除 `stock` 后 `ship` 的前驱是 `{auth, price}`，`validate({})` → `(True, None)`，顺序 `auth, price, ship`；再删除 `auth` 后顺序 `price, ship`；依赖不存在的规则 → `ValueError: unknown dependencies: ['nope']`。

**复杂度。** `validate` 为 `O(V + E)` 加上各规则自身的代价；`add_rule` 为 `O(依赖数)`；`remove_rule` 为 `O(前驱数 * 后继数)`；空间 `O(V + E)`。

**易错点。**
- 删除后不重连：`a -> b -> c` 删除 `b` 后 `deps` 变成 `{'a': set(), 'c': set()}`，而正确是 `{'a': set(), 'c': {'a'}}`，`c` 与 `a` 的先后约束丢了。
- 重连时只更新 `deps`、漏了 `users`：随后删除 `a` 时找不到后继 `c`，`c` 的依赖里残留已不存在的 `a`，`validate` 抛 `KeyError: 'a'`。
- `add_rule` 不校验依赖是否存在：`TopologicalSorter` 会把未知名字当成一个节点排到最前面，`validate` 时 `self._rules['nope']` 抛 `KeyError`。

**追问。**
- 不想一失败就停，要收集所有失败：用 `prepare()` / `get_ready()` / `done()` 逐层处理，前驱失败或被跳过的规则不执行，只记录真正失败的规则。
- 同一层互不依赖的规则并发执行：`get_ready()` 一次返回当前所有可执行的规则，丢进线程池，全部完成后再对每个调用 `done()`。
- 之后允许给已有规则加依赖：加边 `u -> v` 前必须检查 `v` 是否已经能到达 `u`，否则会成环。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1462 课程表 IV、LC 1136 并行课程。
