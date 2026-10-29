---
id: tlc-search-insert-position-3-why
node: b.search-insert-position
type: qa
step: 3
---
## Q
**LC 35 搜索插入位置**｜正确性

在升序数组里用 `lo, hi = 0, len(nums)`、`while lo < hi`、`nums[mid] < target` 时 `lo = mid + 1`、否则 `hi = mid`，循环结束返回 `lo`。这个循环维持着什么不变量，为什么 `lo` 就是插入位置？把 `hi` 初值写成 `len(nums) - 1`、或把比较改成 `<=`，各会错成什么样？

## A
**不变量。** 每一轮开始时，`nums[:lo]` 里的元素全部 `< target`，`nums[hi:]` 里的元素全部 `>= target`（空段自然成立）。`nums[mid] < target` 时 `mid` 属于「小于」那一段，所以 `lo = mid + 1` 保持不变量；否则 `mid` 属于「大于等于」那一段，`hi = mid` 保持不变量。区间 `[lo, hi)` 每轮严格缩小，终止时 `lo == hi`，左段全 `< target`、右段全 `>= target`，所以 `lo` 就是第一个 `>= target` 的下标：`target` 在数组里就是它的位置，不在就是应插入的位置。

**反例一：`hi` 写成 `len(nums) - 1`。** 答案可能是 `len(nums)`（插到末尾），而 `lo` 永远不超过 `hi`，取不到它。`nums = [1,3,5,6]`、`target = 7`：`lo` 走到 `3` 就停，返回 `3`，正确是 `4`。

**反例二：比较写成 `nums[mid] <= target`。** 相等时也往右排除，找到的是第一个**大于** `target` 的位置。`nums = [1,3,5,6]`、`target = 5`：返回 `3`，正确是 `2`（`5` 自己就在下标 `2`）。

**反例三：区间约定混用。** 半开区间的 `hi = mid` 配上闭区间的 `while lo <= hi`：当 `lo == hi` 时 `mid == lo`，若 `nums[mid] >= target` 则 `hi = mid` 不变，循环永不结束。
