---
slug: first-bad-version
---
## Q
**LC 278 第一个错误的版本**｜Easy

版本 `1..n` 里从某个版本起全是坏的。用接口 `isBadVersion(v)` 找出第一个坏版本，调用尽量少。

## A
**一句话。** 序列形如「好…好坏…坏」，二分保持第一个坏版本一定在 `[lo, hi]` 内。

```python
def first_bad_version(n):
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if isBadVersion(mid):
            hi = mid        # mid 可能就是答案
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 好版本时写 `lo = mid`：`lo=1, hi=2` 时 `mid=1` 为好，`lo` 不变，死循环。
- `hi = mid` 配了 `while lo <= hi`：`lo == hi` 且 `mid` 为坏时 `hi` 不再变小，死循环；两套写法不能混用。
- C++ / Java 写 `(lo + hi) / 2`：`n` 接近 `2^31 - 1` 时溢出，要写 `lo + (hi - lo) / 2`。

**追问。**
- 为什么是 `lo < hi` 而不是 `lo <= hi`？：区间收缩到一个点时它就是答案，不需要再判断。
- 一般化的二分模板？：对任意单调的「好 / 坏」判定，找第一个「坏」，同 LC 35、LC 34。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 153 寻找旋转排序数组中的最小值、LC 162 寻找峰值
