---
slug: tt-ai-assisted-order-validator
---
## Q
**OrderValidator（规则 DAG）**｜Medium

订单要通过一组有依赖的校验规则（DAG），按拓扑顺序执行，任一失败即不通过。实现 `add_rule(name, check, depends_on=())`（依赖须已存在，规则名唯一，否则抛 `ValueError`）、`remove_rule(name)`（把它的前驱直接连到后继，保持先后关系）、`validate(order)` 返回 `(是否通过, 第一个失败的规则名或 None)`。

## A
**一句话。** 用 `deps` 和 `users` 两个字典存 DAG，`validate` 用 `TopologicalSorter` 按依赖顺序执行，删除时前驱连后继。

```python
class OrderValidator:
    def __init__(self):
        self.rules = {}
        self.deps = {}     # 规则 -> 它依赖的规则
        self.users = {}    # 规则 -> 依赖它的规则（反向边）

    def add_rule(self, name, check, depends_on=()):
        if name in self.rules:
            raise ValueError("duplicate rule")
        if any(d not in self.rules for d in depends_on):
            raise ValueError("unknown dependency")  # 不成环
        self.rules[name] = check
        self.deps[name] = set(depends_on)
        self.users[name] = set()
        for d in depends_on:
            self.users[d].add(name)

    def remove_rule(self, name):
        preds = self.deps.pop(name)    # 不存在抛 KeyError
        succs = self.users.pop(name)
        del self.rules[name]
        for p in preds:
            self.users[p].discard(name)
        for s in succs:
            self.deps[s].discard(name)
        for p in preds:                # p 先于 s 的约束不能丢
            for s in succs:
                self.deps[s].add(p)
                self.users[p].add(s)

    def validate(self, order):
        seq = TopologicalSorter(self.deps).static_order()
        for name in seq:
            if not self.rules[name](order):
                return False, name
        return True, None
```

**复杂度。** `validate` `O(V + E)` 加规则自身代价，`remove_rule` `O(前驱数 × 后继数)`，空间 `O(V + E)`。

**易错点。**
- 删除后不重连：`a -> b -> c` 删 `b` 后 `c` 与 `a` 的先后约束丢了。
- 重连只改 `deps` 漏了 `users`：之后删 `a` 找不到后继 `c`，`c` 的依赖残留 `a`，`validate` 抛 `KeyError`。
- `add_rule` 不校验依赖存在：未知名字被当成节点排最前，执行时 `KeyError`。

**追问。**
- 想收集所有失败而不是第一个？：用 `prepare()` / `get_ready()` / `done()` 逐层处理，前驱失败的规则跳过不执行。
- 同层规则并发执行？：`get_ready()` 一次给出所有可执行规则，丢进线程池，完成后逐个 `done()`。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1462 课程表 IV、LC 1136 并行课程
