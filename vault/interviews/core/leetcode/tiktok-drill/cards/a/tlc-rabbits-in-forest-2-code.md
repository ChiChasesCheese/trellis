---
id: tlc-rabbits-in-forest-2-code
node: a.rabbits-in-forest
type: qa
step: 2
---
## Q
**LC 781 森林中的兔子**｜写出 Python 实现

整数数组 `answers`（长度 `1..1000`，元素 `0..999`），`answers[i]` 是第 `i` 只被问到的兔子对「还有多少只其它兔子和你同色」的回答。返回森林中兔子的最少数量。

## A
**思路。** 用 `Counter` 数出每个回答值 `x` 的人数 `count`。回答 `x` 的兔子，每个颜色组共 `x + 1` 只，需要 `ceil(count / (x + 1))` 个组，对应兔子数 `组数 * (x + 1)`。把所有回答值的结果相加。

```python
from collections import Counter


def num_rabbits(answers: list[int]) -> int:
    total = 0
    for x, count in Counter(answers).items():   # 回答 x 的兔子：同色一组，每组最多 x + 1 只
        groups = -(-count // (x + 1))           # 向上取整：需要几种颜色
        total += groups * (x + 1)               # 每组都按满员 x + 1 只计（没回答的也算进去）
    return total
```

**运行。** `[1,1,2]` → `5`；`[10,10,10]` → `11`；`[0]` → `1`；`[0,0,0]` → `3`；`[1,1,1]` → `4`；`[2,2,2,2]` → `6`；`[999] * 1000` → `1000`。

**复杂度。** 时间 `O(n)`；空间 `O(k)`（`k` 为不同回答值个数，`k <= n`）。

**写法要点。** `Counter(answers).items()` 直接给出（回答值，人数）对；`-(-count // (x + 1))` 是整数向上取整的惯用写法，全程不碰浮点数（`math.ceil(count / (x + 1))` 在数很大时可能被浮点精度坑）；变量 `x` 既是回答也是「同色其余只数」，`x + 1` 才是组大小，写在注释里避免混淆。
