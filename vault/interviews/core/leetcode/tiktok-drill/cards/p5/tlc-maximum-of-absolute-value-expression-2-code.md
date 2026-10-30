---
id: tlc-maximum-of-absolute-value-expression-2-code
node: p5.maximum-of-absolute-value-expression
type: qa
step: 2
---
## Q
**LC 1131 绝对值表达式的最大值**｜写出 Python 实现

两个长度相等的整数数组 `arr1`、`arr2`（长度 `2` 到 `40000`，元素在 `-10^6` 到 `10^6`）。返回 `|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|` 在所有 `0 <= i, j < n` 上的最大值。要求 `O(n)`。

## A
**思路。** 对 `arr1`、`arr2` 的符号 `(p, q)` 各取 `±1` 共 `4` 种组合，计算 `f(i) = p * arr1[i] + q * arr2[i] + i`（`i` 项符号固定为 `+`）；这一组合下的最大表达式值是 `max f - min f`。四种组合取最大。

```python
from itertools import product


def max_abs_val_expr(arr1: list[int], arr2: list[int]) -> int:
    ans = 0
    for p, q in product((1, -1), repeat=2):          # 拆绝对值：|x| = max(x, -x)，i 项的符号可固定为 +
        vals = [p * a + q * b + i for i, (a, b) in enumerate(zip(arr1, arr2))]
        ans = max(ans, max(vals) - min(vals))
    return ans
```

运行：`[1,2,3,4]`、`[-1,4,5,6]` → `13`；`[1,-2,-5,0,10]`、`[0,-2,-1,-7,-4]` → `20`；`[5,5]`、`[5,5]` → `1`；`[-1,0]`、`[0,-1]` → `3`。

**复杂度。** 时间 `O(n)`：`4` 轮，每轮构造一个长度 `n` 的列表并各扫一遍求最大最小；空间 `O(n)`。

**写法要点。** `product((1, -1), repeat=2)` 一次产生 `(p, q)` 的四种符号，比两层嵌套循环更直接；`enumerate(zip(arr1, arr2))` 的解包 `i, (a, b)` 同时拿到下标和两个值；先建 `vals` 再调用 `max`、`min`，两次扫描都在 C 层完成；`ans = 0` 作为初值安全，因为 `max f - min f >= 0`。
