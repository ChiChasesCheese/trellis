---
id: tlc-patterns-math-bit-sim-9-problems
node: patterns.math-bit-sim
type: qa
step: 9
---
## Q
**数学、位运算与模拟｜本组用到数学、位运算或模拟的题**

按变形分类，这个题组里哪些题属于这一类？

## A
**数论**
- LC 365 水壶问题
- LC 69 x 的平方根
- LC 204 计数质数（高频）

**位运算 / 原地标记**
- LC 78 子集（位掩码写法）
- LC 31 下一个排列（从右向左找第一个降序的位置）
- LC 136 只出现一次的数字（高频）

**矩阵与方向模拟**
- LC 54 螺旋矩阵
- LC 48 旋转图像
- LC 1041 困于环中的机器人
- LC 867 转置矩阵（高频）

**按规则模拟**
- LC 2502 设计内存分配器
- LC 1360 日期之间隔几天（高频）

**逐位运算 / 排版**
- LC 415 字符串相加
- LC 43 字符串相乘
- LC 68 文本左右对齐
- LC 189 轮转数组（三次反转，`k %= n`）
- LC 151 反转字符串中的单词（高频）

**随机 / 概率**
- LC 470 用 Rand7() 实现 Rand10()（高频）

**奇偶 / 配对计数**
- LC 1247 交换字符使得字符串相同（高频）

**TikTok 变体**
- 螺旋矩阵：O(1) 额外空间且不修改输入（上下左右四条边界逐圈向里收）

提示：先问数据范围（能否直接模拟）、边界（空 / 单行 / 进位 / 前导零）、整数规则（取模、除法截断）；能用内置（`gcd`、`pow`、`bit_count`、`isqrt`）就先用，再被要求时手写。

**例题：** LC 365 水壶问题

有容量 `x`、`y`（`<= 10^3`）的两个水壶，水源无限，可以装满、清空、互相倾倒；判断能否使两壶水量之和恰好为 `target`。

```python
from math import gcd
def can_measure_water(x: int, y: int, target: int) -> bool:
    return target <= x + y and target % gcd(x, y) == 0
```

**例题：** LC 69 x 的平方根

给非负整数 `x`（`0 <= x <= 2^31 - 1`），返回 `x` 的算术平方根向下取整的整数部分，不得使用内置指数函数或运算符。

```python
def my_sqrt(x: int) -> int:
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**例题：** LC 78 子集

同 LC 78，用位掩码枚举：第 `mask` 个子集取 `mask` 二进制里为 1 的位对应的元素（`nums` 互不相同，长度 `<= 10`，共 `2^n` 个子集）。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
```

**例题：** LC 31 下一个排列

给数组 `nums`（长度 `<= 100`，元素可重复），原地改成字典序的下一个排列；已是最大排列则改成最小排列，只用常数额外空间。

```python
def next_permutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    lo, hi = i + 1, n - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo, hi = lo + 1, hi - 1
```

**例题：** LC 54 螺旋矩阵

给 `m x n` 矩阵（`m, n <= 10`），按顺时针螺旋顺序返回所有元素。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    result: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        result.extend(matrix[top][left : right + 1])
        result.extend(row[right] for row in matrix[top + 1 : bottom + 1])
        if top < bottom and left < right:
            result.extend(reversed(matrix[bottom][left:right]))
            result.extend(matrix[r][left] for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return result
```

**例题：** LC 48 旋转图像

给 `n x n` 矩阵（`n <= 20`），原地顺时针旋转 `90` 度，不允许另开矩阵。

```python
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
```

**例题：** LC 1041 困于环中的机器人

机器人从原点面朝北出发，无限循环执行指令串 `instructions`（长度 `<= 100`，`G` 前进一步、`L`/`R` 左右转 `90` 度），判断它是否会被困在某个环里。

```python
def is_robot_bounded(instructions: str) -> bool:
    x = y = 0
    dx, dy = 0, 1
    for ch in instructions:
        if ch == "G":
            x, y = x + dx, y + dy
        elif ch == "L":
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
    return (x, y) == (0, 0) or (dx, dy) != (0, 1)
```

**例题：** LC 2502 设计内存分配器

实现 `Allocator(n)`（`n <= 1000`）：`allocate(size, mID)` 在最左侧找 `size` 个连续空闲单元并标记为 `mID`，返回起始下标或 `-1`；`freeMemory(mID)` 释放 `mID` 的所有单元并返回个数。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n
    def allocate(self, size: int, mID: int) -> int:
        run = 0
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size
                return start
        return -1
    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:
                self.mem[i] = 0
                freed += 1
        return freed
```

**例题：** LC 415 字符串相加

给两个字符串形式的非负整数 `num1`、`num2`（长度 `<= 10^4`，无前导零），返回它们的和（字符串），不能直接转成整数，也不能用大整数库。

```python
from itertools import zip_longest
def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```

**例题：** LC 43 字符串相乘

给两个字符串形式的非负整数 `num1`、`num2`（长度 `<= 200`），返回乘积（字符串），不能直接转成整数，也不能用大整数库。

```python
def multiply(num1: str, num2: str) -> str:
    a = [int(c) for c in reversed(num1)]
    b = [int(c) for c in reversed(num2)]
    res = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y
    carry = 0
    for k in range(len(res)):
        carry, res[k] = divmod(res[k] + carry, 10)
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return "".join(map(str, reversed(res)))
```

**例题：** LC 68 文本左右对齐

给单词数组 `words` 和宽度 `maxWidth`（`<= 100`），贪心地每行放尽量多的单词，排成每行恰好 `maxWidth` 个字符的两端对齐文本：空格尽量均匀，多出的空格给左侧；最后一行和只含一个单词的行左对齐。

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    lines: list[str] = []
    i, n = 0, len(words)
    while i < n:
        j, used = i + 1, len(words[i])
        while j < n and used + 1 + len(words[j]) <= max_width:
            used += 1 + len(words[j])
            j += 1
        line = words[i:j]
        if j == n or len(line) == 1:
            lines.append(" ".join(line).ljust(max_width))
        else:
            gaps = len(line) - 1
            spaces = max_width - sum(map(len, line))
            q, r = divmod(spaces, gaps)
            parts = [w + " " * (q + (k < r)) for k, w in enumerate(line[:-1])]
            lines.append("".join(parts) + line[-1])
        i = j
    return lines
```

**例题：** LC 189 轮转数组

给整数数组 `nums`（长度 `<= 10^5`）和 `k`（`0 <= k <= 10^5`），原地把数组向右轮转 `k` 个位置。

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    def reverse(i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

**例题：** LC 204 计数质数

给非负整数 `n`，返回**严格小于** `n` 的质数的个数。`0 <= n <= 5 * 10^6`。

```python
from math import isqrt

def count_primes(n: int) -> int:
    if n < 3:
        return 0                                     # n <= 2 时没有小于 n 的质数
    is_prime = bytearray([1]) * n                    # is_prime[i] == 1 表示 i 目前仍是质数候选
    is_prime[0] = is_prime[1] = 0
    for i in range(2, isqrt(n - 1) + 1):             # 只需筛到 sqrt(n-1)
        if is_prime[i]:
            # 从 i*i 开始：更小的倍数 i*k (k<i) 已被更小的质因子划掉
            is_prime[i * i::i] = bytes(len(range(i * i, n, i)))
    return sum(is_prime)
```

**例题：** LC 136 只出现一次的数字

非空整数数组 `nums` 里，除了一个元素只出现一次，其余每个元素都恰好出现两次。找出那个只出现一次的元素。要求**线性时间、常数额外空间**。`1 <= nums.length <= 3 * 10^4`，`-3 * 10^4 <= nums[i] <= 3 * 10^4`。

```python
def single_number(nums: list[int]) -> int:
    ans = 0
    for x in nums:
        ans ^= x                                     # a ^ a == 0，0 ^ x == x，与顺序无关
    return ans
```

**例题：** LC 867 转置矩阵

给一个二维整数数组 `matrix`，返回它的转置矩阵：沿主对角线翻转，行下标和列下标互换，即结果的 `res[j][i] = matrix[i][j]`。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 1000`，`1 <= m * n <= 10^5`，`-10^9 <= matrix[i][j] <= 10^9`。

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]     # zip(*rows) 把第 j 列收成一个元组
```

**例题：** LC 1360 日期之间隔几天

编写程序计算两个日期之间隔了多少天。日期以字符串 `YYYY-MM-DD` 给出，保证是 `1971` 年到 `2100` 年之间的有效日期。

```python
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def days_between_dates(date1: str, date2: str) -> int:
    def is_leap(y: int) -> bool:
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    def to_days(s: str) -> int:                       # 距 1970-12-31 的天数
        y, m, d = map(int, s.split("-"))
        days = sum(365 + is_leap(k) for k in range(1971, y))     # 整年
        days += sum(MONTH_DAYS[:m - 1]) + (m > 2 and is_leap(y)) # 整月，闰年 2 月多一天
        return days + d

    return abs(to_days(date1) - to_days(date2))
```

**例题：** LC 151 反转字符串中的单词

给字符串 `s`，反转其中单词的顺序。单词是由非空格字符组成的串，`s` 里用至少一个空格分隔单词，开头、结尾、单词之间都可能有多余的空格。返回单词顺序颠倒、单词之间只用**一个**空格连接、没有前导或尾随空格的字符串。`1 <= s.length <= 10^4`，`s` 只含英文字母、数字和空格，至少有一个单词。

```python
def reverse_words(s: str) -> str:
    words: list[str] = []
    i = len(s) - 1
    while i >= 0:                          # 从右往左扫描
        if s[i] == " ":
            i -= 1
            continue
        end = i + 1                        # 单词的右开边界
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:end])         # i 停在单词左边的空格（或 -1）
    return " ".join(words)
```

**例题：** LC 470 用 Rand7() 实现 Rand10()

已给等概率返回 `[1, 7]` 的 `rand7()`，只准调用它实现等概率返回 `[1, 10]` 的 `rand10()`；`rand10()` 最多被调用 `10^5` 次。

```python
import random
def rand7() -> int:
    return random.randint(1, 7)
def rand10() -> int:
    while True:
        idx = (rand7() - 1) * 7 + rand7()
        if idx <= 40:
            return (idx - 1) % 10 + 1
```

**例题：** LC 1247 交换字符使得字符串相同

两个等长且只含 `'x'`、`'y'` 的字符串 `s1`、`s2`，每次交换必须是 `s1[i]` 与 `s2[j]`（不能在同一个字符串内部交换），求使两串相同的最少交换次数，做不到返回 `-1`；长度 `<= 1000`。

```python
def minimum_swap(s1: str, s2: str) -> int:
    xy = yx = 0
    for a, b in zip(s1, s2):
        if a != b:
            if a == "x":
                xy += 1
            else:
                yx += 1
    if (xy + yx) % 2:
        return -1
    return xy // 2 + yx // 2 + 2 * (xy % 2)
```

**例题：** 螺旋矩阵：O(1) 额外空间且不修改输入

按顺时针螺旋顺序返回 `m x n` 矩阵的所有元素，额外空间 `O(1)`，不能用 `visited` 数组，也不能修改输入；要处理空矩阵、单行、单列。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out: list[int] = []
    while top <= bottom and left <= right:
        out.extend(matrix[top][c] for c in range(left, right + 1))
        out.extend(matrix[r][right] for r in range(top + 1, bottom + 1))
        if top < bottom:
            out.extend(matrix[bottom][c] for c in range(right - 1, left - 1, -1))
        if left < right:
            out.extend(matrix[r][left] for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return out
```
