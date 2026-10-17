# 02 · 双指针 / 滑动窗口（Two pointers & sliding window）

双指针（two pointers）和滑动窗口（sliding window）靠一个事实把 O(n²) 降到 O(n)：指针只前进不回退，每个元素最多被两个指针各经过一次。同向窗口用于「最长 / 最短的满足条件的连续段」，相向指针用于「有序数组里找一对」或「从两端向中间收缩」。每一步丢掉的那一半候选必须有正确性证明，面试里要能口述。下面按「最笨解法 → 慢在哪 → 模板 → 五道题」展开。

覆盖的题目：LC 3 Longest Substring Without Repeating Characters · 42 Trapping Rain Water（Hard）· 15 3Sum · 11 Container With Most Water · 76 Minimum Window Substring（Hard）


## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 3：求字符串里「不含重复字符的最长子串」。最笨的做法：枚举所有子串 `s[i..j]`（O(n²) 个），每个再检查有没有重复（O(n)），总共 O(n³)。就算检查用 `set` 优化到 O(n)，枚举本身也是 O(n²)。n = 10⁵ 时是 10¹⁰。

### 1.2 慢在哪里

枚举 `s[i..j]` 和 `s[i..j+1]` 时，**前者的信息被丢掉了**：`s[i..j]` 已经确认无重复，往右加一个字符只需要看「新字符在不在里面」，却被我们重新扫了一遍。
更重要的是：如果 `s[i..j]` 里已经有重复，那么**所有以 `i` 开头、比它更长的子串必然也重复**——它们根本不用看。

> 因果链：有效性具有「单调性」（窗口一旦无效，再变大也无效）→ 一旦发现无效就只需要收缩左端 → 左右指针都只向前走，各最多走 n 步 → O(n)。

### 1.3 两种家族

| 家族 | 指针怎么走 | 什么时候用 | 例题 |
|---|---|---|---|
| **滑动窗口**（sliding window，同向） | `right` 每轮 +1，`left` 在窗口无效时追上来 | 求「满足条件的最长 / 最短连续子数组/子串」，且条件对窗口有单调性 | 3、76 |
| **相向双指针**（opposite-end two pointers） | `lo` 从左、`hi` 从右，每轮根据比较结果**丢弃一端** | 数组有序（或评分有单调性），要找一对/一组 | 15、11、42 |

### 1.4 相向双指针为什么正确（以 LC 11 为例，资深面试官要你口述证明）

面积 = 宽 × min(左高, 右高)。现在 `lo`、`hi` 两堵墙，假设 `height[lo] < height[hi]`。

- 任何以 `lo` 为左墙、右墙在 `hi` 左边的容器：宽更小，而高度仍被 `height[lo]` 限制（`min ≤ height[lo]`），所以面积 ≤ 当前面积。
- 因此「以 `lo` 为左墙」的所有候选都已被考虑，**可以安全丢弃 `lo`**，`lo += 1`。

每一步丢掉一个下标，n 步结束，O(n)。**证明的结构**就是「丢弃的东西不可能比已经看到的更好」——所有双指针题都用同一个模板去证明。

## 2. 模板与逐行讲解

```python
# Template S: variable-size sliding window ("longest/shortest window that is valid")
def longest_window(seq, is_valid_after_add, add, remove):
    left = best = 0
    for right, x in enumerate(seq):
        add(x)                                   # 1. grow: take seq[right] into the window
        while not is_valid_after_add():          # 2. repair: shrink from the left until valid again
            remove(seq[left])
            left += 1
        best = max(best, right - left + 1)       # 3. record: window seq[left..right] is valid here
    return best

# instance: at most 2 distinct values in the window
counts = {}
def add(x): counts[x] = counts.get(x, 0) + 1
def remove(x):
    counts[x] -= 1
    if counts[x] == 0:
        del counts[x]
assert longest_window([1, 2, 1, 3, 3], lambda: len(counts) <= 2, add, remove) == 3

# Template P: opposite-ends two pointers on a SORTED array (or a monotone score)
def pair_with_sum(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    while lo < hi:
        s = sorted_nums[lo] + sorted_nums[hi]
        if s == target:
            return lo, hi
        if s < target:
            lo += 1                              # sum too small: only a bigger left value can help
        else:
            hi -= 1                              # sum too big: only a smaller right value can help
    return None

assert pair_with_sum([1, 3, 4, 6, 9], 10) == (0, 4)
assert pair_with_sum([1, 3, 4, 6, 9], 100) is None
```

逐行讲解：

1. 模板 S 的 `left = best = 0`：窗口是 `seq[left..right]`（闭区间），空窗口 `left > right` 的情况在这里不出现，因为每轮先加入再修复。
2. `add(x)`：把 `seq[right]` 放进窗口并更新「窗口状态」（计数、和、不同元素个数……）。**状态更新只能是 O(1)**，否则就不是 O(n)。
3. `while not is_valid(): remove(seq[left]); left += 1`：窗口无效就一直缩。用 `while` 不是 `if`——可能要缩多次。
4. `best = max(best, right - left + 1)`：此刻窗口一定有效（因为单个元素的窗口总有效，`while` 最终会停）。求**最短**窗口时，记录发生在 `while` 循环**内部**（窗口还有效的时候）。
5. 模板 P 的 `while lo < hi`：两端相遇就结束。`s < target: lo += 1`——和太小，只有换更大的左值才有希望，所以丢弃 `lo`；反之丢弃 `hi`。这就是 1.4 的证明模板。

## 3. 完整手算（Worked trace）

LC 3，输入 `"pwwkew"`。窗口是 `s[left..right]`；`last[ch]` 记录字符最近一次出现的下标。

```python
def window_trace(s):
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        note = ""
        if ch in last and last[ch] >= left:
            note = f"dup of index {last[ch]} inside window -> left {left} -> {last[ch] + 1}"
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
        print(f"right={right} ch={ch!r} window={s[left:right + 1]!r:<9} len={right - left + 1} best={best}  {note}")
    return best

assert window_trace("pwwkew") == 3
```

```text
right=0 ch='p' window='p'       len=1 best=1  
right=1 ch='w' window='pw'      len=2 best=2  
right=2 ch='w' window='w'       len=1 best=2  dup of index 1 inside window -> left 0 -> 2
right=3 ch='k' window='wk'      len=2 best=2  
right=4 ch='e' window='wke'     len=3 best=3  
right=5 ch='w' window='kew'     len=3 best=3  dup of index 2 inside window -> left 2 -> 3
```

重点看第 3 行（`right=2`）：新来的 `w` 在窗口里出现过（下标 1），所以 `left` 直接跳到 `1 + 1 = 2`——**不是一步一步缩，而是一次跳到重复字符之后**。最后一行同理。
`last[ch] >= left` 这个条件很关键：旧的出现位置在窗口**左边**时，它不算重复（见常见 bug）。

再看 LC 42 的相向双指针，输入 `[3, 0, 2, 0, 4]`：

```python
def trap_trace(height):
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    print("heights:", height)
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            add = left_max - height[left]
            water += add
            print(f"L={left} R={right} h[L]={height[left]} < h[R]={height[right]}: left_max={left_max}, +{add} (cell {left})  water={water}")
            left += 1
        else:
            right_max = max(right_max, height[right])
            add = right_max - height[right]
            water += add
            print(f"L={left} R={right} h[L]={height[left]} >= h[R]={height[right]}: right_max={right_max}, +{add} (cell {right})  water={water}")
            right -= 1
    return water

assert trap_trace([3, 0, 2, 0, 4]) == 7
```

```text
heights: [3, 0, 2, 0, 4]
L=0 R=4 h[L]=3 < h[R]=4: left_max=3, +0 (cell 0)  water=0
L=1 R=4 h[L]=0 < h[R]=4: left_max=3, +3 (cell 1)  water=3
L=2 R=4 h[L]=2 < h[R]=4: left_max=3, +1 (cell 2)  water=4
L=3 R=4 h[L]=0 < h[R]=4: left_max=3, +3 (cell 3)  water=7
```

读法：每一步比较两端；较矮的一端当前的「水位上限」就是它自己这一侧的历史最高（因为另一侧有更高的墙兜底），所以可以立刻结算那一格的水量，然后这端指针向内走。

## 4. 题目

```python
from collections import Counter
```

### 4.1 LC 3 · Longest Substring Without Repeating Characters（Medium）

```python
# solutions/3_longest_substring_without_repeating.py
def length_of_longest_substring(s):
    last = {}                       # char -> most recent index
    left = 0                        # window is s[left..right]
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # duplicate INSIDE the window
            left = last[ch] + 1               # jump left just past the old copy
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

- **一句话洞见**：用 `last[ch]` 记下每个字符最近的下标，遇到窗口内的重复就让 `left` 一步跳到它后面。
- **复杂度**：时间 O(n)，空间 O(min(n, 字符集大小))。

**资深追问**

- **规模 ×1000**：本身 O(n)，瓶颈变成 I/O。流式读取块，状态只有 `left`、`last`、`best`。
- **流式输入**：天然在线——每来一个字符 O(1) 更新；注意下标会一直增长，用 Python int 不会溢出（C++/Java 用 `long`）。
- **内存**：`last` 的大小受字符集限制（ASCII 128，Unicode 约 110 万）；如果需要返回子串本身，额外记 `best_start`。
- **并发**：把文本切块并行时，跨块边界的窗口会被切断。因为最长无重复子串长度 ≤ 字符集大小 `A`，每块多读 `A` 个字符的重叠区即可保证不漏。
- **接口 / 边界**：「字符」是什么——字节、Unicode 码点、还是字形簇（emoji + 变音符号）？大小写是否区分？返回长度还是子串？空串返回 0。
- **测试**：`"abba"`（`left` 不能回退）、全相同、全不同、空串、与 O(n²) 暴力随机对拍。

### 4.2 LC 42 · Trapping Rain Water（Hard）

```python
# solutions/42_trapping_rain_water.py
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            # the right wall is already taller than height[left], so left_max alone decides this cell
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

- **一句话洞见**：每格水量 = `min(左侧最高, 右侧最高) - 自身高度`；相向双指针时，较矮一侧的上限已经确定，可以先结算。
- **说出三种解法再选**：(1) 前缀最大 / 后缀最大数组，O(n) 时间 O(n) 空间，最直观；(2) 单调栈，一次扫描，按「凹槽」结算（见第 04 讲）；(3) 双指针，O(n) 时间 O(1) 空间——面试里先讲 (1) 再优化到 (3)。
- **复杂度**：时间 O(n)，空间 O(1)。

**资深追问**

- **规模 ×1000**：已经是线性，O(1) 空间；数据在磁盘（`mmap`）上时，双指针从两端各一个顺序读流，I/O 友好。
- **流式输入**：双指针需要知道右端，不适合纯流式；改用单调栈——从左到右处理，水量在遇到更高的右墙时结算，空间 O(栈深)。
- **内存**：前缀数组 O(n) → 双指针 O(1)，这是典型的「状态压缩」。
- **并发**：把数组分成 P 块，每块求局部最大值，再做一次并行前缀最大（parallel prefix max）得到每块左右两侧的全局上限，然后各块独立结算。
- **接口**：高度非负整数？可以是浮点吗？返回水的体积；2D 版本（LC 407）要换成「最小堆 + BFS 从边界向内」。
- **测试**：谷（valley）、平台（plateau）、单调递增 / 递减（0 水）、空数组、与 `O(n²)` 公式对拍。

### 4.3 LC 15 · 3Sum（Medium）

```python
# solutions/15_three_sum.py
def three_sum(nums):
    nums = sorted(nums)
    out = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:     # same first number -> same triples
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # skip duplicate second numbers
                    lo += 1
    return out
```

- **一句话洞见**：排序后固定第一个数，剩下就是「有序数组里找和为 `-nums[i]` 的一对」，用相向双指针；去重靠「跳过相同的值」。
- **复杂度**：时间 O(n²)（排序 O(n log n) 不是瓶颈），额外空间 O(1)（不计输出）。

**资深追问**

- **规模 ×1000**：O(n²) 在 n = 10⁵ 时已经是 10¹⁰，不可行。要先问：值域是否有界？答案个数是否可能本身就是 Θ(n²)（那输出就是下界）？值域小可以用计数 + bitset；一般 3SUM 没有已知的显著优于 n² 的算法（3SUM 猜想）。
- **流式**：不适合；若必须在线，维护已见集合的哈希，每个新元素 `x` 在已见集合里找满足 `a + b = -x` 的一对，代价 O(已见数)。
- **内存**：`sorted()` 会复制，允许修改输入就用 `nums.sort()` 做到 O(1) 额外空间。
- **并发**：外层 `i` 之间互不依赖（排序后数组只读），可以按 `i` 分段并行；由于「第一个数不同」，结果天然无重复，合并只需拼接。
- **接口**：返回三元组的顺序？是 `list` 还是 `tuple`？不足 3 个元素返回 `[]`；推广到 kSum / 目标值 ≠ 0 时，把 `0` 参数化。
- **测试**：`[0,0,0,0]`（不能重复输出）、没有解、全正数、含大量重复、与 `set(combinations)` 暴力对拍。

### 4.4 LC 11 · Container With Most Water（Medium）

```python
# solutions/11_container_with_most_water.py
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:      # the shorter wall limits the area; only moving it can help
            lo += 1
        else:
            hi -= 1
    return best
```

- **一句话洞见**：移动较矮的那堵墙——移动较高的墙，宽度减小而高度仍被矮墙限制，不可能变好（1.4 的证明）。
- **复杂度**：时间 O(n)，空间 O(1)。

**资深追问**

- **规模 ×1000 / 内存**：线性、O(1) 空间，不需要改；重点是被问到「为什么贪心正确」时能口述 1.4 的证明。
- **流式**：相向双指针要知道右端，不适合；在线版本要换结构（如维护单调的候选墙集合）。
- **并发**：串行依赖（每步取决于上一步的比较），难以并行；要并行就换算法（分治：左半、右半、跨中线的最优）。
- **接口**：至少 2 堵墙；高度可以为 0；返回面积还是下标对？有并列最优时返回哪一个？
- **测试**：`[1,1]`、递减 / 递增、两端最高、与 O(n²) 暴力对拍。

### 4.5 LC 76 · Minimum Window Substring（Hard）

```python
# solutions/76_minimum_window_substring.py
def min_window(s, t):
    need = Counter(t)
    missing = len(t)                            # how many required chars are still uncovered
    best_l, best_len = 0, float("inf")
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                           # may go negative: surplus copies
        if missing == 0:                        # window valid: shrink while it stays valid
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1                  # drop s[left] to start looking for the next window
            missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_l:best_l + best_len]
```

- **一句话洞见**：用 `need` 计数 + `missing`（还缺几个字符）判断窗口是否「覆盖了 t」；有效就尽量缩左端，同时记录最短窗口。`need[ch]` 变成负数表示窗口里这个字符有富余。
- **与 LC 3 的区别**：LC 3 找最长，记录在 `while` 之后；LC 76 找最短，记录在窗口有效的时候（`while` 内部的语义）。
- **复杂度**：时间 O(|s| + |t|)，空间 O(字符集)。

**资深追问**

- **规模 ×1000**：线性；对 `s` 很大、`t` 很多（多次查询）的情况，预处理 `s` 的每个字符的位置列表，每次查询只访问 `t` 中出现的字符的位置（"filtered s"）。
- **流式**：窗口是在线维护的；但要输出窗口内容就必须缓存窗口里的字符，内存 O(最长窗口)，可能很大——如果只要位置，不缓存。
- **内存**：`Counter` 对字符集小很便宜；Unicode 时 dict 大小受 t 的不同字符数限制，因为只需要关心 `t` 里出现的字符（其他字符直接忽略）。
- **并发**：窗口长度可能跨整段，切块并行不安全；并行的正确方向是**多个查询并行**，共享只读的位置索引。
- **接口**：`t` 为空返回 `""`；`t` 有重复字符（`"aa"`）要计数；多个最短窗口返回最左的；大小写敏感。
- **测试**：`t` 长于 `s`、`t` 有重复字符、窗口恰为整个 `s`、字符不在 `s` 里；与暴力（枚举所有子串用 `Counter` 判断覆盖）对拍。

## 5. 常见 bug

1. **窗口里没有「`last[ch] >= left`」检查**（LC 3）：`"abba"` 时 `left` 会被旧位置拉回去，窗口变大，答案错成 3。
2. **用 `if` 代替 `while` 缩窗口**：一次只缩一步，窗口仍无效。
3. **最短窗口的记录写在循环外**：窗口已经无效了才记录。
4. **3Sum 去重写错**：只对第一个数去重、不对第二个数去重，会输出重复三元组（`[0,0,0,0]`）；或者去重时用 `nums[i] == nums[i+1]`，把合法的 `(-1,-1,2)` 也跳掉了——应该和**前一个**比较，且在 `i > 0` 时。
5. **相向指针忘记 `lo < hi`**：写成 `<=` 会把同一个元素用两次。
6. **LC 42 比较方向写反**：`height[left] < height[right]` 时结算的是 `left` 侧，不是 `right`。
7. **把窗口当成「必须连续」的结构去套不连续的问题**：子序列（subsequence）不是子数组（subarray），滑动窗口不适用。

## 6. 自测题

1. 滑动窗口为什么是 O(n) 而不是 O(n²)——毕竟里面有 `while`？
   <details><summary>答案</summary>`right` 走 n 步，`left` 也最多走 n 步，每个指针都只前进；`while` 的总迭代次数 ≤ n，所以整体 ≤ 2n 次操作。这叫均摊分析（amortized）。</details>
2. 什么样的题**不能**用滑动窗口？
   <details><summary>答案</summary>窗口的有效性对「扩大 / 缩小」不单调的题。例如有负数时的「和为 k 的子数组」（用前缀和 + 哈希，见第 01 讲）。</details>
3. LC 11 里为什么移动较矮的墙是安全的？
   <details><summary>答案</summary>以较矮墙为一端的容器，其高度被矮墙限制，而宽度只会随着另一端向内移动而变小，所以所有这类候选的面积 ≤ 当前面积，可以整体丢弃。</details>
4. 小编程：有序数组 `a`，原地删除重复元素并返回新长度（LC 26）。
   <details><summary>答案</summary>快慢指针：`w = 1`；`for r in range(1, n): if a[r] != a[w-1]: a[w] = a[r]; w += 1`；返回 `w`。O(n) 时间，O(1) 空间。</details>
5. 3Sum 为什么要先排序？不排序用哈希可以吗？
   <details><summary>答案</summary>排序后相向双指针能在 O(n) 内解决「一对」，且去重简单（相同的值相邻）。不排序用哈希也能做，但去重要用 `set` 存排序后的三元组，常数大且更容易出错。</details>
6. 资深追问：把 LC 3 跑在 10⁹ 字符的文件上，怎么并行？
   <details><summary>答案</summary>分块并行，块间重叠字符集大小 `A` 个字符（最长答案不超过 `A`），每块求局部最优并记录位置，再取全局最大；注意重叠区重复计算但不影响正确性。</details>
