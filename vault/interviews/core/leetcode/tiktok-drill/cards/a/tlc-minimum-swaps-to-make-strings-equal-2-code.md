---
id: tlc-minimum-swaps-to-make-strings-equal-2-code
node: a.minimum-swaps-to-make-strings-equal
type: qa
step: 2
---
## Q
**LC 1247 交换字符使得字符串相同**｜写出 Python 实现

两个等长字符串 `s1`、`s2`（长度 `1` 到 `1000`），只含 `'x'` 和 `'y'`。每次只能交换 `s1[i]` 与 `s2[j]`（跨字符串），求使两串相同的最少交换次数，做不到返回 `-1`。

## A
**思路。** 遍历每个位置，若 `s1[i] != s2[i]`，按 `s1[i]` 是 `x` 还是 `y` 记入 `xy` 或 `yx` 计数。总数为奇数返回 `-1`；否则同类两两配对各一次，剩一个 `xy` 和一个 `yx` 时再加两次。

```python
def minimum_swap(s1: str, s2: str) -> int:
    xy = yx = 0                                  # xy：s1 是 x、s2 是 y 的位置数；yx 反之
    for a, b in zip(s1, s2):
        if a != b:
            if a == "x":
                xy += 1
            else:
                yx += 1
    if (xy + yx) % 2:                            # 不同位置总数为奇数：x 的总数是奇数，永远分不成两串相等
        return -1
    return xy // 2 + yx // 2 + 2 * (xy % 2)      # 同类两两一次；剩下一对 xy 和一对 yx 要两次
```

运行：`("xx", "yy")` → `1`；`("xy", "yx")` → `2`；`("xx", "xy")` → `-1`；`("x", "x")` → `0`；`("xyx", "yxx")` → `2`。

**复杂度。** 时间 `O(n)`：一趟扫描；空间 `O(1)`：两个计数。

**写法要点。** `zip(s1, s2)` 同时遍历两个字符串，不用下标；只用两个计数器就足以表达全部信息，不需要保存位置；`xy % 2` 与 `yx % 2` 在可行时必然相等，所以只用 `xy % 2` 判断是否剩一对异类，`2 * (xy % 2)` 是它们要额外花的两次交换；`//` 是整除，不会得到浮点数。
