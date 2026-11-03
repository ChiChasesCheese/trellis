---
id: craft-dependency-graph-cycle-detection-4-recalc-once
node: craft.patterns.dependency-graph-cycle-detection
type: qa
step: 4
---
## Q
**依赖图与环检测 · 改一个格子后，下游每格恰好重算一次**｜写法

电子表格里 D 读 B 和 C，B、C 又都读 A（菱形）。用户改了 A，最直接的做法是递归地「重算所有读我的格子」。D 会被算几次？更大的表格里这个数字怎么增长？怎样让每格只算一次？

## A
**要点。** 递归传播会沿每条路径各到达一次，菱形越多，重复算的次数成倍增长。正确做法：先收集受影响的格子，按拓扑序（被依赖的在前）排好，每格算一次。收集用一次后序（post-order）DFS，倒过来就是拓扑序：一个格子只有在它所有下游都访问完才入列表，反转后它一定排在所有下游之前。

```python
users = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}   # 谁读了谁；菱形 A -> B, C -> D

def naive(c, count):                  # 朴素：每改一格，递归地把下游全部重算一遍
    count[c] = count.get(c, 0) + 1
    for u in users[c]:
        naive(u, count)

def topo(changed):
    order, seen = [], set()
    def visit(c):
        seen.add(c)
        for u in users[c]:            # users: 谁读了 c
            if u not in seen: visit(u)
        order.append(c)               # 后序：所有下游都已入列
    visit(changed)
    return order[::-1]                # 反转：自己在前，下游在后

n = {}; naive("A", n); print("朴素递归的重算次数：", n)
print("拓扑序：", topo("A"), "每格一次")
```

菱形 A→B、A→C、B→D、C→D 改 A：

```
朴素递归的重算次数： {'A': 1, 'B': 1, 'D': 2, 'C': 1}
拓扑序： ['A', 'C', 'B', 'D'] 每格一次
```

**为什么。** 重复不只是慢：D 第一次算时 C 可能还是旧值，得到的是一个中间结果，如果公式有副作用或有计数（测试里数 `eval_count`），结果还不确定。

**代价。** 这个 DFS 是递归的，依赖链极长（几万格的列）会碰到 Python 的递归深度限制；那时改成显式栈，或者逐层的 Kahn 算法。

**易错。** 范围只能是「被改格子 + 它的下游」，而不是全表；这是电子表格相对「全表重算」的核心收益，也是拓扑序必须从 `users`（反向边）出发的原因。
