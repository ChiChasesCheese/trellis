---
id: craft-default-forms-3-next-default
node: craft.idioms.default-forms
type: qa
step: 3
---
## Q
**省掉标志变量 · `next((x for x in xs if cond), None)` 好在哪，什么时候是陷阱**｜写法

计费引擎要给规则做依赖排序：每轮找“第一个依赖都已完成的规则”，找不到就说明依赖成环。可以用一行 `next(生成器, None)` 完成。它相对 `for + break + 标志变量` 好在哪？什么时候反而不行？

## A
**要点。** `next(it, default)` 取迭代器的下一个元素，耗尽时返回 `default` 而不抛 `StopIteration`。配生成器表达式，就是“找第一个满足条件的元素”，且**惰性**：找到就停，不会扫完整个序列。「找不到」直接成了一个可以判断的值，成环的判定就是 `if ready is None`。

```python
RULES = {"base": [], "tax": ["base"], "fee": ["base"], "rebate": ["tax", "fee"]}
CYCLIC = {"a": ["b"], "b": ["a"], "c": []}

def order(rules: dict[str, list[str]]) -> list[str]:
    pending, done, out = list(rules), set(), []
    while pending:
        # 找第一个依赖都已完成的; 找不到就返回 None
        ready = next((r for r in pending if all(d in done for d in rules[r])), None)
        if ready is None:                       # 剩下的每个都在等别的剩下的 = 有环
            raise ValueError(f"成环: {pending}")
        pending.remove(ready)
        done.add(ready)
        out.append(ready)
    return out

print(order(RULES))
try:
    order(CYCLIC)
except ValueError as e:
    print(e)

# 陷阱: 想找的值本身可能是 None / 0 / "" 时, next(..., None) 分不清「没找到」
vals = [0, None, 3]
hit = next((v for v in vals if v is None), None)
miss = next((v for v in vals if v == 99), None)
print("找到 None  ->", hit)
print("没找到 99  ->", miss, "<- 两种情况返回值相同")
MISSING = object()                                # 用专属哨兵区分
print("哨兵版 找到 None:", next((v for v in vals if v is None), MISSING) is not MISSING)
print("哨兵版 没找到 99:", next((v for v in vals if v == 99), MISSING) is not MISSING)
```

实际输出：

```
['base', 'tax', 'fee', 'rebate']
成环: ['a', 'b']
找到 None  -> None
没找到 99  -> None <- 两种情况返回值相同
哨兵版 找到 None: True
哨兵版 没找到 99: False
```

**陷阱一：值本身可能是 None。** 要找的元素可能就是 `None`、`0`、`""` 时，`next(..., None)` 分不清“没找到”和“找到了 None”。用一个专属哨兵对象（`MISSING = object()`）当默认值。

**陷阱二：可读性。** 条件复杂、嵌套两三层 `all(... for ...)` 的一行 `next` 比循环更难读。条件超过一个表达式时拆成一个有名字的小函数，或者用普通循环。

**为什么成环判定成立。** 每轮只会取走“依赖都满足”的规则，如果还剩规则却一个都取不出来，剩下的每个都在等别的剩下的，这正是环。
