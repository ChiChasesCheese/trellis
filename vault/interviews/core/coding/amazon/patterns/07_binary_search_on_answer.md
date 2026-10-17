# 07 · 二分查找（含「对答案二分」）（Binary search & binary search on the answer）

> 本讲覆盖：LC 875 Koko Eating Bananas · 33 Search in Rotated Sorted Array · 4 Median of Two Sorted Arrays（Hard）· 410 Split Array Largest Sum（Hard）
> 前置：整数除法 `//`、循环不变量（loop invariant）的概念（本讲会讲）。相关：LC 1011 Capacity To Ship Packages 与 875 是同一个模板。
> 读完你应该能：(1) 把「有序数组查找」推广为「单调谓词的第一个 True」；(2) 写出不会死循环、不会少一位的二分；(3) 认出「最小化最大值 / 最大化最小值」类题可以对答案二分。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 875：Koko 有若干堆香蕉 `piles`，每小时选一堆吃掉最多 `speed` 根（不足就吃完这堆，这一小时剩余时间浪费），要在 `h` 小时内吃完，求最小的整数速度 `speed`。

最笨的做法：从 `speed = 1` 开始试，对每个速度计算需要多少小时（O(n)），第一个能在 `h` 小时内吃完的就是答案。最坏要试到 `max(piles)`，总共 O(n · max)。`max` 是 10⁹ 时是 10⁹ 次试探。

### 1.2 慢在哪里

我们把速度一个个试了，却没有利用一个明显的事实：**速度越大，所需小时数只会不增。** 也就是说「这个速度够不够」这个判断随速度单调变化：

```text
speed:   1  2  3  4  5  6 ...
够不够:  F  F  F  T  T  T ...      <- 单调：F...F T...T
```

> 因果链：判断函数 `ok(x)` 对 x 单调 → 试探点 `mid` 的结果可以**一次丢掉一半**候选（`ok(mid)` 为真就丢掉 mid 右边，为假就丢掉 mid 左边及自己）→ 区间每次减半，从 10⁹ 到 1 只要约 30 步 → O(n log max)。

这就是二分查找（binary search）的本质：**不是「在有序数组里找数」，而是「在单调的 F…F T…T 序列里找第一个 T」。** 在有序数组里找 `target` 只是特例：`ok(i) = a[i] >= target`。

### 1.3 两类用法

| 类型 | 区间是什么 | 谓词是什么 | 例题 |
|---|---|---|---|
| 在数据上二分 | 下标区间 `[0, n]` | `a[i] >= target`，或「旋转数组中某一半有序」的判断 | 33、4 |
| **对答案二分**（binary search on the answer） | 答案的取值区间（速度、容量、最大子数组和…） | `feasible(x)`：用 x 能不能完成任务（通常是一个 O(n) 的贪心检查） | 875、1011、410 |

识别信号：题目问「**最小的 x 使得…** / **最大的 x 使得…**」，并且「x 越大任务越容易（或越难）」。**把『求最优』转换成『判定是否可行』**，判定往往是简单的贪心。

## 2. 模板与逐行讲解

```python
# Template: "first True" binary search on a monotone predicate  (False False False True True True)
def first_true(lo, hi, ok):
    """Smallest x in [lo, hi] with ok(x) True; assumes ok(hi) is True and ok is monotone."""
    while lo < hi:
        mid = (lo + hi) // 2            # lower middle: never equals hi, so hi = mid always shrinks
        if ok(mid):
            hi = mid                    # mid might be the answer: keep it
        else:
            lo = mid + 1                # mid is too small: discard it
    return lo

# classic use: leftmost index of target in a sorted array (insertion point)
def lower_bound(a, target):
    lo, hi = 0, len(a)                  # hi = len(a) means "not found / insert at the end"
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo

# binary search ON THE ANSWER: smallest integer square root ceiling
def ceil_sqrt(n):
    return first_true(0, n, lambda x: x * x >= n)

import bisect
assert lower_bound([1, 2, 2, 2, 5], 2) == 1 == bisect.bisect_left([1, 2, 2, 2, 5], 2)
assert lower_bound([1, 2, 5], 9) == 3
assert ceil_sqrt(10) == 4 and ceil_sqrt(16) == 4 and ceil_sqrt(0) == 0
```

逐行讲解：

1. `first_true(lo, hi, ok)` 的**不变量**：答案始终在 `[lo, hi]` 内，且 `ok(hi)` 为真。循环条件 `lo < hi` 表示区间里至少还有两个候选。
2. `mid = (lo + hi) // 2`（取**下中位**）：保证 `mid < hi`。因此 `hi = mid` 一定缩小区间。如果写成 `lo = mid`（不加 1）就会死循环——`lo + 1 == hi` 时 `mid == lo`。**规则：`hi = mid` 配下中位，`lo = mid + 1`。**
3. `if ok(mid): hi = mid`：`mid` 可能就是答案，所以**保留**它；`else: lo = mid + 1`：`mid` 确定不是，丢弃。
4. 循环结束 `lo == hi`，即第一个 True。
5. `lower_bound` 里 `hi = len(a)` 而不是 `len(a) - 1`：允许「所有元素都小于 target」时返回 `len(a)`（插入点）。这与 `bisect.bisect_left` 一致。
6. `ceil_sqrt`：对答案二分的最小例子——「最小的 x 使 x² ≥ n」。

> 其他写法（`while lo <= hi`，`mid ± 1` 两头都动）也对，但容易写错。**选一种写法并只用这一种**，面试里就不会在边界上卡壳。

## 3. 完整手算（Worked trace）

LC 875，`piles = [3, 6, 7, 11]`，`h = 8`。区间 `[1, 11]`：

```python
def koko_trace(piles, h):
    def hours(speed):
        return sum((p + speed - 1) // speed for p in piles)
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        need = hours(mid)
        verdict = "ok -> hi=mid" if need <= h else "too slow -> lo=mid+1"
        print(f"lo={lo:>2} hi={hi:>2} mid={mid:>2} hours={need:>2} (limit {h})  {verdict}")
        if need <= h:
            hi = mid
        else:
            lo = mid + 1
    print(f"lo==hi=={lo}")
    return lo

assert koko_trace([3, 6, 7, 11], 8) == 4
```

```text
lo= 1 hi=11 mid= 6 hours= 6 (limit 8)  ok -> hi=mid
lo= 1 hi= 6 mid= 3 hours=10 (limit 8)  too slow -> lo=mid+1
lo= 4 hi= 6 mid= 5 hours= 8 (limit 8)  ok -> hi=mid
lo= 4 hi= 5 mid= 4 hours= 8 (limit 8)  ok -> hi=mid
lo==hi==4
```

读法：第一行 `mid = 6`，需要 1+1+2+2 = 6 小时 ≤ 8，可行，所以答案 ≤ 6，`hi = 6`；第二行 `mid = 3`，需要 1+2+3+4 = 10 小时 > 8，不可行，答案 > 3，`lo = 4`；……最后 `lo == hi == 4`。每一行区间大小都大约减半。

## 4. 题目

### 4.1 LC 875 · Koko Eating Bananas（Medium，频率 75）

```python
# solutions/875_koko_eating_bananas.py
def min_eating_speed(piles, h):
    def hours(speed):
        return sum((p + speed - 1) // speed for p in piles)    # ceil(p / speed) without floats

    lo, hi = 1, max(piles)                  # answer is in [1, max]; speed max always works (if h >= len)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:                 # feasible: try slower
            hi = mid
        else:                               # too slow: must go faster
            lo = mid + 1
    return lo
```

- **一句话洞见**：对速度二分，`hours(speed)` 单调不增；`ceil(p / s)` 用整数写成 `(p + s - 1) // s`，避免浮点误差。
- **复杂度**：时间 O(n log max(piles))，空间 O(1)。
- **同模板**：LC 1011（运输包裹的最小运力）把 `hours` 换成「按顺序装载需要的天数」，下界是 `max(weights)`，上界是 `sum(weights)`。

**资深追问**

- **规模 ×1000**：`n` 变成 10⁹ 堆：`hours` 的计算是一次可并行的归约（map-reduce 求和），每次二分步骤各机器算局部和再汇总，总共约 30 轮通信。
- **流式输入**：`piles` 不断变化时无法复用结果；若只是增删少量堆，可以维护排序结构，对相同速度增量更新总小时数。
- **内存**：O(1)，只需要遍历。
- **并发**：每次判定是只读的归约，可以并行；二分步骤之间有依赖，串行。
- **接口 / 边界**：`h < len(piles)` 无解——返回 −1 还是抛异常？有 0 根的堆？`speed` 是否必须是整数（本题是）？溢出（`sum` 在 Java/C++ 需要 `long`）？
- **测试**：`h == len(piles)`（答案是 `max`）、单堆、巨大数值、`h` 很大（答案是 1）；与逐个速度试探的暴力对拍（文件里已有）。

### 4.2 LC 33 · Search in Rotated Sorted Array（Medium，频率 75）

```python
# solutions/33_search_in_rotated_sorted_array.py
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                       # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                           # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

- **一句话洞见**：把有序数组旋转后，任取 `mid`，`[lo..mid]` 和 `[mid..hi]` 中**至少有一半是有序的**；判断 `target` 是否落在有序那一半里，落在就在那半找，否则去另一半。
- **复杂度**：时间 O(log n)，空间 O(1)。

**资深追问**

- **规模 ×1000**：O(log n) 本来就几乎不随 n 增长；数据在磁盘上时，每次二分对应一次随机读（B-tree 把它变成几次页读取）。
- **含重复元素（LC 81）**：`nums[lo] == nums[mid] == nums[hi]` 时无法判断哪半有序，只能 `lo += 1; hi -= 1`，最坏退化到 O(n)——要能说出为什么。
- **内存 / 流式**：不适用（需要随机访问）。
- **并发**：只读，天然线程安全；多个查询可以并行。
- **接口**：找不到返回 −1；有重复时返回哪个下标？旋转点未知；数组为空？
- **测试**：对所有旋转量枚举（文件里随机生成「有序数组 + 旋转」并与 `list.index` 对拍）；两个元素（`nums[lo] <= nums[mid]` 里的 `=` 号）、单元素、目标不在数组中、目标在最小 / 最大值。

### 4.3 LC 4 · Median of Two Sorted Arrays（Hard，频率 77）

```python
# solutions/4_median_of_two_sorted_arrays.py
def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a                                       # binary search over the shorter one
    m, n = len(a), len(b)
    half = (m + n + 1) // 2                               # size of the combined left part
    lo, hi = 0, m
    inf = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2                                # take i from a ...
        j = half - i                                      # ... and j from b into the left part
        a_left = a[i - 1] if i > 0 else -inf
        a_right = a[i] if i < m else inf
        b_left = b[j - 1] if j > 0 else -inf
        b_right = b[j] if j < n else inf
        if a_left > b_right:                              # took too many from a
            hi = i - 1
        elif b_left > a_right:                            # took too few from a
            lo = i + 1
        else:                                             # a valid split: left <= right on both sides
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
    raise ValueError("inputs must be sorted")
```

- **一句话洞见**：不要合并。在较短的数组 `a` 上二分「取 `i` 个放进左半」，那么 `b` 里该取 `j = half - i` 个。划分合法 ⟺ `a_left <= b_right` 且 `b_left <= a_right`；合法时中位数由这四个数决定。
- **哨兵**：越界时用 `-inf` / `+inf` 代替，避免特判。
- **复杂度**：时间 O(log min(m, n))，空间 O(1)。
- **先说基线**：双指针归并到中间 O(m + n)；再优化到 O(log)。

**资深追问**

- **规模 ×1000**：两个数组分别在不同机器上：划分二分只需要读取 `a[i-1], a[i], b[j-1], b[j]` 四个值，每轮 O(1) 次远程读取，总共 O(log) 次通信。更一般的 k 个有序分片求第 p 分位数：对「值」二分，每轮让各分片统计「≤ x 的个数」并求和。
- **流式**：两个流不能提前知道中位数；需要双堆（第 05 讲 LC 295）或分位数草图。
- **内存**：O(1)，不需要合并。
- **并发**：只读；二分步骤串行。
- **接口**：两个都为空是非法输入；偶数个元素返回 `float`；元素为整数还是浮点；`-inf/+inf` 哨兵对整数数组仍然有效。
- **测试**：一个数组为空、长度悬殊、全相同、不重叠（一个数组全小于另一个）、奇偶总长；与「合并后排序取中位数」的暴力对拍（文件里已有 500 组）。

### 4.4 LC 410 · Split Array Largest Sum（Hard，频率 52）

```python
# solutions/410_split_array_largest_sum.py
def split_array(nums, k):
    def pieces_needed(limit):                     # greedy: pack as much as possible into each piece
        pieces, cur = 1, 0
        for x in nums:
            if cur + x > limit:
                pieces += 1
                cur = 0
            cur += x
        return pieces

    lo, hi = max(nums), sum(nums)                 # limit can't be below the biggest item; sum always works
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(mid) <= k:               # feasible with <= k pieces (fewer can always be split more)
            hi = mid
        else:
            lo = mid + 1
    return lo
```

- **一句话洞见**：问「把数组切成 k 段，使最大段和最小」→ 反过来问「**段和上限为 limit 时，最少要切几段**」——这个检查是贪心（能放就放），并且 limit 越大所需段数越少，单调！对 limit 二分。
- **边界**：下界 `max(nums)`（至少一个元素自己一段）、上界 `sum(nums)`（一段）。
- **复杂度**：时间 O(n log(sum))，空间 O(1)。
- **对比 DP**：`dp[i][j]` 前 i 个元素切 j 段的最小最大和，O(k·n²) —— 二分更快更短。

**资深追问**

- **规模 ×1000**：`pieces_needed` 是一次顺序扫描，可以分块并行（块边界需要传递「当前段已累计的和」，用一个小状态机）；二分约 log(sum) 轮。
- **流式 / 内存**：O(1) 内存，每轮顺序读一遍数据；在外存上每轮一次顺序 I/O。
- **并发**：同上；也可以把多个 limit 的候选并行测试（k 路搜索而不是二路）。
- **接口**：`k > n` 非法（或每段至少一个元素）；元素非负（负数破坏单调性，本方法不适用）；返回最小的最大和还是具体切分点（需要在最终 limit 上重放一遍贪心）。
- **测试**：`k = 1`（答案是 sum）、`k = n`（答案是 max）、全相同、一个很大的元素；与「枚举所有切分」的暴力对拍（文件里已有）。

## 5. 常见 bug

1. **死循环**：`lo = mid`（不加 1）并且 `mid` 取下中位。规则：`hi = mid` 配 `lo = mid + 1`。
2. **答案区间不对**：410 的下界写成 0 或 1，导致 `pieces_needed` 在 `limit < max(nums)` 时得到错误的「可行」。
3. **判定函数不单调**就硬上二分：先确认 `ok(x)` 对 x 单调。
4. **浮点 `ceil`**：`math.ceil(p / s)` 在大数上有舍入误差；用 `(p + s - 1) // s`。
5. **33 里忘记 `nums[lo] <= nums[mid]` 的等号**：两个元素时 `lo == mid`，`[lo..mid]` 也是有序的。
6. **用 `(lo + hi) // 2` 在 C++/Java 溢出**：写 `lo + (hi - lo) // 2`（Python 不会溢出，但面试官可能会问）。
7. **4 里对较长的数组二分**：`j = half - i` 可能为负数；先交换保证 `a` 是较短的。

## 6. 自测题

1. 为什么对答案二分的区间是 `[max(nums), sum(nums)]`？
   <details><summary>答案</summary>最大段和至少是最大的单个元素（每个元素必须属于某一段）；最多是整个数组的和（只有一段）。区间外的值要么一定不可行，要么一定不是最小。</details>
2. `while lo < hi` 与 `hi = mid` 的组合为什么要取下中位？
   <details><summary>答案</summary>下中位 `mid < hi` 总成立，所以 `hi = mid` 严格缩小区间；若取上中位，`hi = mid` 在 `lo + 1 == hi` 时 `mid == hi`，区间不变，死循环。</details>
3. 判断一道题能否「对答案二分」，要检查什么？
   <details><summary>答案</summary>(1) 答案取值有明确的上下界；(2) 存在一个能在多项式时间内判定「x 是否可行」的检查；(3) 可行性随 x 单调。</details>
4. 小编程：在有序数组中找 `target` 的第一个和最后一个位置（LC 34）。
   <details><summary>答案</summary>`first = lower_bound(a, target)`；`last = lower_bound(a, target + 1) - 1`（整数）；若 `first == len(a)` 或 `a[first] != target` 返回 `[-1, -1]`。</details>
5. 为什么 LC 33 有重复元素时最坏是 O(n)？
   <details><summary>答案</summary>`[1,1,1,1,1,1,2,1]`：`nums[lo] == nums[mid] == nums[hi]` 时无法判断哪半有序，只能缩一格；整条数组可能都是重复值。</details>
6. 资深追问：一个 10TB 的有序日志按时间戳存储，找某个时刻的第一条记录，怎么做？
   <details><summary>答案</summary>文件内按偏移二分（`seek` 到中点，向后找到记录边界再读时间戳），每步一次磁盘读取，约 log₂(10TB / 记录大小) ≈ 40 步；更好的是稀疏索引（每 N 条记录一个索引项，常驻内存）先二分索引再顺序扫小段——这就是 LSM / B-tree 索引的思想。</details>
