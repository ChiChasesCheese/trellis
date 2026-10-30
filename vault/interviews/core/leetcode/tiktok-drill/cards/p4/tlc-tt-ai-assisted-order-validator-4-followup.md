---
id: tlc-tt-ai-assisted-order-validator-4-followup
node: p4.tt-ai-assisted-order-validator
type: qa
step: 4
---
## Q
**OrderValidator（规则 DAG）**｜追问

面试官接着问：（1）要收集所有失败的规则，而不是遇到第一个就停；（2）同一层互不依赖的规则想并发执行；（3）测试应该覆盖哪些情形？

## A
1. **收集所有失败**：用 `prepare()` / `get_ready()` / `done()` 逐层推进。前驱失败或已被跳过的规则不执行，只把真正失败的规则记下来。

```python
from graphlib import TopologicalSorter


def failures(deps: dict[str, set[str]], rules: dict, order: dict) -> list[str]:
    sorter = TopologicalSorter(deps)
    sorter.prepare()
    bad: set[str] = set()                    # 失败或被跳过的规则
    failed: list[str] = []
    while sorter.is_active():
        for name in sorter.get_ready():
            if deps[name] & bad:
                bad.add(name)                # 前驱出了问题：跳过，不执行
            elif not rules[name](order):
                bad.add(name)
                failed.append(name)
            sorter.done(name)
    return sorted(failed)
```

四条规则（`ship` 依赖 `stock` 和 `price`，两者依赖 `auth`），外加独立的 `audit`：订单让 `stock` 和 `audit` 失败 → `['audit', 'stock']`（`ship` 因 `stock` 失败被跳过）；让 `auth` 失败 → `['auth']`。
2. **并发**：`get_ready()` 一次返回所有已满足依赖的规则，把它们提交线程池，全部完成后逐个调用 `done()`，再取下一批。规则是纯函数、相互独立时才安全。
3. **测试清单**：空图；单规则通过与失败；菱形依赖（`ship` 在 `stock`、`price` 之后）；失败短路（失败规则之后的规则不执行）；删除中间规则后可达关系不变；删除不存在的规则抛 `KeyError`；重复名、未知依赖抛 `ValueError`；删除后再次添加同名规则；规则很多（链长 `10^4`）时不递归。

**Python 提醒**：`TopologicalSorter` 的 `prepare()` 在图有环时抛 `graphlib.CycleError`；同一个实例只能 `prepare()` 一次，每次验证都要新建；`get_ready()` 返回的是元组，处理完每个节点必须调用 `done()`，否则后继永远不会就绪。
