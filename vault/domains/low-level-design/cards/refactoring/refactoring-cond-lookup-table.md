---
id: refactoring-cond-lookup-table
node: refactoring.conditionals
type: qa
step: 3
---
## Q
一个长长的 `if kind == "a": ... elif kind == "b": ...` 链，每个分支只是返回一个数或调用一个函数。什么时候把它换成字典？什么情况下不能换？

## A
**分支只是“键 → 值或函数”的映射时，换成表：新增一种只加一行**

- **数据表**：`RATES = {"basic": 5, "pro": 9}`，查表代替比较；
- **函数表**：`HANDLERS = {"csv": to_csv, "json": to_json}`，`HANDLERS[kind](data)`；
- **未知的键要显式处理**：用 `d[k]` 会抛 `KeyError`，通常正是想要的；`d.get(k, default)` 悄悄回退，只有规格允许默认值时才用；
- **顺序有意义时不能用字典**：`if x > 100 ... elif x > 10 ...` 靠“第一个满足的”决定，用列表 `[(阈值, 结果), ...]` 按顺序扫描；
- **分支里有多行逻辑、互相依赖时**：别硬塞进表；拆成函数再放进表，或保留 `if`。

```python
RATES = {"basic": 5, "pro": 9}

def rate(kind):
    try: return RATES[kind]
    except KeyError: raise ValueError(f"未知套餐 {kind!r}") from None   # 未知就报错

TIERS = [(100, "large"), (10, "medium"), (0, "small")]               # 顺序有意义：用列表

def size(n): return next(label for floor, label in TIERS if n >= floor)

print(rate("pro"), size(150), size(50), size(3))      # 9 large medium small
```

**知识点：**简化条件（Simplifying Conditionals）
