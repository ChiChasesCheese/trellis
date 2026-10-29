---
id: uth-compose-spring-bean-registry-5-interview
node: compose.spring-bean-registry
type: qa
step: 5
---
## Q
**借到面试题上：规则 DAG 就是两张依赖表**｜Spring 依赖记录 · 7.0

面试题要你维护一批有先后依赖的规则：能加、能删，按依赖顺序执行。这和 Spring 的依赖记录是什么关系？

## A
**背景。** 一条规则就是一个 Bean，“规则 A 依赖规则 B”就是“A 依赖 B”。Spring 记两张方向相反的表，这类题也一样：`deps`（我依赖谁）、`users`（谁依赖我），每次增删两边一起改。

**结构。**

| Spring | 面试题 |
|---|---|
| `dependenciesForBeanMap` | `deps` |
| `dependentBeanMap` | `users` |
| 关闭时依赖者先销毁 | 执行时被依赖的先执行（拓扑序） |
| 销毁后从别人的记录里清掉 | 删规则时清掉两边的记录 |

**坑。** Spring 销毁的是整个容器，清掉记录就够了；规则 DAG 删一条规则时还要把前驱直接连到后继，否则“`a` 先于 `c`”这个传递出来的约束会随着 `b` 一起消失。

**例题：** OrderValidator（规则 DAG）

实现 `OrderValidator`：订单要依次通过一组校验规则，规则之间有依赖，构成有向无环图。`add_rule(name, check, depends_on=())` 添加规则（只能依赖已存在的规则）；`remove_rule(name)` 删除规则，并把它的所有前驱直接连到它的所有后继上，保持“谁必须先于谁”；`validate(order)` 按依赖顺序执行，返回 `(是否通过, 第一个失败的规则名或 None)`。规则数不超过 `10^4`。

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
