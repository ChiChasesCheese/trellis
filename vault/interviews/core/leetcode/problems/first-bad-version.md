---
slug: first-bad-version
---
## Q
**LC 278 第一个错误的版本（First Bad Version）**｜Easy

你是产品经理，团队开发的新产品最新版本没有通过质量检测。由于每个版本都基于之前的版本开发，错误版本之后的所有版本都是错的。假设有 `n` 个版本 `[1, 2, ..., n]`，找出导致之后所有版本出错的第一个错误版本。你可以调用 `bool isBadVersion(version)` 接口判断版本号 `version` 是否出错，应尽量减少调用次数。`1 <= bad <= n <= 2^31 - 1`。例：`n = 5`，`bad = 4` → `4`（调用 `isBadVersion(3)` 为 `false`，`isBadVersion(4)` 为 `true`）；`n = 1`，`bad = 1` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二分查找（binary search）找第一个满足条件的位置（lower bound）。

**一句话。** 版本序列形如 `好 好 ... 好 坏 坏 ... 坏`，用二分在 `[lo, hi]` 里保持「第一个坏版本一定在区间内」，每次根据 `mid` 好坏砍掉一半。

**识别。** 「前一段都不满足、后一段都满足」的单调谓词，求边界：二分。`n` 可达 `2^31 - 1`，线性扫描调用次数太多；调用次数要尽量少，二分最多约 31 次。

**推导。** 从 1 开始逐个调用，最多 `n` 次。谓词单调，所以每次问中点：中点是坏的，答案在中点及其左边（中点本身可能就是答案，所以 `hi = mid`）；中点是好的，答案在右边（`lo = mid + 1`）。`lo == hi` 时就是第一个坏版本。

```python
def first_bad_version(n: int) -> int:
    lo, hi = 1, n                       # 不变式：第一个坏版本一定在 [lo, hi] 内
    while lo < hi:
        mid = (lo + hi) // 2            # Python 整数不会溢出；C++/Java 要写 lo + (hi - lo) // 2
        if isBadVersion(mid):
            hi = mid                    # mid 是坏的：答案在 [lo, mid]，mid 本身可能就是
        else:
            lo = mid + 1                # mid 是好的：答案在 (mid, hi]
    return lo
```

运行：`n = 5`，`bad = 4` → `4`（依次调用 `isBadVersion(3)`、`isBadVersion(4)`）；`n = 1`，`bad = 1` → `1`（零次调用）；`n = 2147483647`，`bad = 1702766719` → `1702766719`。

**复杂度。** 时间 `O(log n)` 次接口调用（至多 31 次），空间 `O(1)`。

**拓展优化。**
- 标准库：`bisect_left` 支持 `key`（Python 3.10+），`range` 按需取值不占内存，序列相当于 `[False, ..., False, True, ..., True]`。

```python
from bisect import bisect_left


def first_bad_version_bisect(n: int) -> int:
    # range 支持按下标取值且不占内存；key 把版本号映射成 False/True，序列因此是 [False..False, True..True]
    return bisect_left(range(1, n + 1), True, key=isBadVersion) + 1
```

**易错点。**
- 好版本时写 `lo = mid`（不加 1）：`lo = 1`，`hi = 2`，`mid = 1` 为好，`lo` 永远不变，死循环。
- 循环条件和收缩方式配错：`hi = mid` 必须搭配 `while lo < hi`；写成 `while lo <= hi` 时，`lo == hi` 且 `mid` 为坏，`hi` 不再变小，死循环。`hi = mid - 1` 才能搭配 `lo <= hi`，两套写法不能混用。
- C++/Java 用 `(lo + hi) / 2`：`n` 接近 `2^31 - 1` 时 `lo + hi` 溢出，必须写 `lo + (hi - lo) / 2`。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 153 寻找旋转排序数组中的最小值、LC 162 寻找峰值。
