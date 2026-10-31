---
id: tlc-binary-search-3-why
node: b.binary-search
type: qa
step: 3
---
## Q
**LC 704 二分查找**｜正确性

这套「左闭右开」写法每一步保持了什么不变量？为什么不会死循环？把区间写成闭区间、或者忘记 `+ 1`，会在什么输入上出错？

## A
**不变量。** 任何时刻，所有下标 `< lo` 的元素都 `< target`，所有下标 `>= hi` 的元素都 `>= target`。因此第一个 `>= target` 的位置（若存在）一定在 `[lo, hi]` 内。初始 `lo = 0`、`hi = n`，条件空真成立。

**每步保持。** `nums[mid] < target`：由有序，`[lo, mid]` 全都小于 `target`，所以 `lo = mid + 1` 保持"左侧都小"。否则 `nums[mid] >= target`：`[mid, hi)` 全都不小于 `target`，所以 `hi = mid` 保持"右侧都不小"。

**为什么终止。** `lo < hi` 时 `mid` 满足 `lo <= mid < hi`：`lo = mid + 1` 使 `lo` 严格增大，`hi = mid` 使 `hi` 严格减小，区间长度严格缩小，最终 `lo == hi`。退出时 `lo` 就是第一个 `>= target` 的位置，再检查它是否等于 `target`。

**反例 1：闭区间却写 `hi = mid`。**
```text
lo, hi = 0, len(nums) - 1
while lo <= hi:
    ...
    hi = mid          # 闭区间应该是 mid - 1
```
- `nums = [5]`、`target = 2`：`lo = hi = 0`，`mid = 0`，`nums[0] > 2` 令 `hi = 0`，区间没变，永远循环。

**反例 2：左闭右开却写 `lo = mid`。**
- `nums = [1, 2]`、`target = 2`：`lo = 0`、`hi = 2`，`mid = 1`，`nums[1] = 2` 不小于 `2`，`hi = 1`；`mid = 0`，`nums[0] = 1 < 2`，`lo = mid = 0`，区间不变，死循环。

**反例 3：不检查边界。** `nums = [5]`、`target = 9`：循环结束 `lo = 1 = len(nums)`，直接读 `nums[lo]` 会 `IndexError`。
