---
id: tlc-tt-ai-assisted-order-validator-2-code
node: a.tt-ai-assisted-order-validator
type: qa
step: 2
---
## Q
**OrderValidator（规则 DAG）**｜写出 Python 实现

用类实现 `OrderValidator`：`add_rule(name, check, depends_on=())` 添加规则（`check` 接收订单字典返回布尔值；依赖必须已存在，规则名唯一，否则抛 `ValueError`）；`remove_rule(name)` 删除规则并把它的前驱连到它的后继；`validate(order)` 按依赖顺序执行规则，返回 `(是否通过, 第一个失败的规则名或 None)`。规则数不超过 `10^4`。

## A
**思路。** `_deps` 存每个规则依赖谁，`_users` 存谁依赖它。`validate` 把 `_deps` 交给 `TopologicalSorter` 得到执行顺序，遇到失败立即返回；`remove_rule` 先取出前驱和后继，断开与自己的边，再把每个前驱连到每个后继。

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

运行：规则 `auth`、`stock`（依赖 `auth`）、`price`（依赖 `auth`）、`ship`（依赖 `stock`、`price`）：`validate({})` → `(True, None)`，执行顺序 `auth, stock, price, ship`；`validate({"price": False})` → `(False, 'price')`；`remove_rule("stock")` 后 `ship` 依赖 `{auth, price}`，顺序 `auth, price, ship`；再 `remove_rule("auth")` 后顺序 `price, ship`；依赖 `"nope"` → `ValueError: unknown dependencies: ['nope']`。

**复杂度。** `validate` 为 `O(V + E)` 加规则本身的代价；`remove_rule` 为 `O(前驱数 * 后继数)`；`add_rule` 为 `O(依赖数)`。

**写法要点。** `TopologicalSorter` 的入参是「节点 → 它的前驱集合」，和直觉里的「边方向」相反，别写反；`static_order()` 是惰性迭代器，边遍历边执行，失败时无需排完整张图；`Order`、`Rule` 用类型别名让签名更短；`dict.pop` 取出邻接集合的同时删除，规则不存在时自然抛 `KeyError`；集合 `discard` 对不存在的元素不报错，适合清理边。
