---
id: amz-closest-store-stage1-closest-with-bisect
node: amazon.amz-closest-store
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计的第 1 关，已经升序排好一个列表 `xs`，用 `bisect` 写出 `closest(xs, target)`，平局取较小的值。

## A
最近的数只可能是 target 的前驱（不大于它的最大值）或后继（不小于它的最小值），比较这两个候选即可：

```python
import bisect

def closest(xs: list[int], target: int) -> int:
    if not xs:
        raise ValueError("empty")
    i = bisect.bisect_left(xs, target)   # 第一个 >= target 的位置
    if i == 0:
        return xs[0]
    if i == len(xs):
        return xs[-1]
    lower, higher = xs[i - 1], xs[i]
    return lower if target - lower <= higher - target else higher
```

例：xs=[10, 40, 70]，target=44 → i=2，候选 40 与 70，返回 40。
