---
id: tlc-assign-cookies-2-code
node: a.assign-cookies
type: qa
step: 2
---
## Q
**LC 455 分发饼干**｜写出 Python 实现

胃口数组 `g`（长度 `1` 到 `3 * 10^4`）和饼干尺寸数组 `s`（长度 `0` 到 `3 * 10^4`），值在 `[1, 2^31 - 1]`。每个孩子最多一块饼干，`s[j] >= g[i]` 才能满足。求最多满足几个孩子。

## A
**思路。** 两组都从小到大排序。按尺寸从小到大看每块饼干：能满足当前胃口最小的未满足孩子，就配对，孩子指针前进；不能就扔掉这块。孩子指针的位置就是满足的人数。

```python
def find_content_children(g: list[int], s: list[int]) -> int:
    greed = sorted(g)                      # 胃口从小到大
    child = 0                              # 下一个待满足的孩子；也等于已满足的人数
    for size in sorted(s):                 # 饼干从小到大
        if child < len(greed) and size >= greed[child]:
            child += 1                     # 这块饼干给当前胃口最小的孩子
        # 否则这块饼干连最小的胃口都满足不了，丢掉
    return child
```

运行：`g = [1,2,3], s = [1,1]` → `1`，`g = [1,2], s = [1,2,3]` → `2`，`g = [5], s = []` → `0`，`g = [1,2], s = [2,1]` → `2`。

**复杂度。** 时间 `O(n log n + m log m)`：排序主导；空间 `O(n + m)`：两个排好序的新列表。

**写法要点。** 用 `sorted(g)` 而不是 `g.sort()`，不改调用方传进来的列表；`for size in sorted(s)` 直接迭代值，不需要下标；`child` 一个变量同时当指针和计数；`child < len(greed)` 放在 `and` 左边，短路保证不越界。
