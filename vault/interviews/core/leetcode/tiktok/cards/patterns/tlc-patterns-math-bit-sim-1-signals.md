---
id: tlc-patterns-math-bit-sim-1-signals
node: patterns.math-bit-sim
type: qa
step: 1
---
## Q
**数学、位运算与模拟｜信号**

什么样的题面指向数论、位运算、矩阵模拟或逐位运算？这类题的难点通常在哪里？

## A
这一类题没有统一的"算法"，考的是**细节与边界**。按信号分：

**数论（Number Theory）：**
- 「最大公约数 / 最小公倍数 / 整除」：LC 1071、365；题面出现"能得到多少升水""循环节"时想 `gcd`（例：LC 1071 字符串的最大公因子；高频：LC 365 水壶问题）。
- 「质数」「范围 `10^6`」：埃氏筛（例：LC 204 计数质数）。
- 「取模 `10^9 + 7`」「幂」：快速幂，每步取模（例：LC 50 Pow(x, n)）。
- 「整数平方根」：二分（LC 69）或 `math.isqrt`（例：LC 69 x 的平方根）。

**位运算：**
- 「只出现一次的数」「成对抵消」：异或 `^`（例：LC 136 只出现一次的数字）。
- 「集合 / 子集 / 状态」且元素数 `<= 20`：用一个整数的二进制位表示集合（位掩码）（例：LC 1239 串联字符串的最大长度）。
- 「数 1 的个数」「是不是 2 的幂」：`n & (n - 1)` 清掉最低位的 1；`n & -n` 取出最低位的 1，用来把两个只出现一次的数分到两组（例：LC 260 只出现一次的数字 III）。
- 「值域是 `1..n` 且要 `O(1)` 空间」：用正负号或下标原地标记（例：LC 442 数组中重复的数据）。

**矩阵与模拟：**
- 「螺旋」「旋转」「蛇形」：维护四个边界或用转置加反转（LC 54、48）（例：LC 54 螺旋矩阵）。
- 「按规则一步一步变化」：机器人、内存泄漏——直接模拟，先估算步数（例：LC 1860 增长的内存泄露；高频：LC 1041 困于环中的机器人）。
- 「大数加法 / 乘法」「文本排版」：逐位模拟（LC 415、43、68）（例：LC 415 字符串相加）。

**难点**：边界（空、单行、单列、进位、前导零）、整数范围、方向表示。

**近似信号：**
- 步数达到 `10^9` 级别的模拟 ⇒ 要找规律或数学公式，不能硬模拟：指令重复无限次，模拟一轮后看位置和朝向就能判定（例：LC 1041 困于环中的机器人）。
- 要找最优 ⇒ 贪心 / DP，而非模拟（例：LC 122 买卖股票的最佳时机 II；高频：LC 134 加油站）。

**例题：** LC 1071 字符串的最大公因子

对于字符串 `s` 和 `t`，只有 `s = t + t + … + t`（`t` 自身连接一次或多次）时，才说 `t` 能除尽 `s`。给定 `str1` 和 `str2`，返回最长的字符串 `x`，使得 `x` 能同时除尽 `str1` 和 `str2`；不存在就返回 `""`。`1 <= str1.length, str2.length <= 1000`，字符串由大写英文字母组成。

```python
from math import gcd


def gcd_of_strings(str1: str, str2: str) -> str:
    if str1 + str2 != str2 + str1:         # 有公因子串 <=> 两种拼接顺序结果一致
        return ""
    return str1[:gcd(len(str1), len(str2))]
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

**例题：** LC 50 Pow(x, n)

实现 `pow(x, n)`，计算浮点数 `x` 的整数 `n` 次幂。`-100.0 < x < 100.0`，`-2^31 <= n <= 2^31 - 1`，`n` 是整数；要么 `x` 不为零，要么 `n > 0`；结果满足 `-10^4 <= x^n <= 10^4`。

```python
def my_pow(x: float, n: int) -> float:
    if n < 0:                      # x^-n = (1/x)^n，先把指数变成非负
        x, n = 1 / x, -n
    result = 1.0
    while n:                       # 不变量：答案 = result * x^n
        if n & 1:                  # 当前二进制位为 1：把这一份 x 乘进结果
            result *= x
        x *= x                     # 底数平方，对应下一个二进制位
        n >>= 1
    return result
```

**例题：** LC 69 x 的平方根

给非负整数 `x`，返回 `x` 的算术平方根，结果只保留整数部分（向下取整）。不允许使用内置的指数函数和运算符，如 `pow(x, 0.5)` 或 `x ** 0.5`。`0 <= x <= 2^31 - 1`。

```python
def my_sqrt(x: int) -> int:
    lo, hi = 0, x                                  # 答案 m 满足 m*m <= x，找最大的这样的 m
    while lo < hi:
        mid = (lo + hi + 1) // 2                   # 向上取整，否则 lo = mid 时区间不缩小会死循环
        if mid * mid <= x:
            lo = mid                               # mid 可行：答案至少是 mid
        else:
            hi = mid - 1
    return lo
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

**例题：** LC 1239 串联字符串的最大长度

给字符串数组 `arr`。从中选出若干个字符串（保持原有顺序）连接成字符串 `s`，要求 `s` 中**所有字母各不相同**。返回所有可行的 `s` 中最长的长度（什么都不选时 `s` 为空串，长度 `0`）。`1 <= arr.length <= 16`，`1 <= arr[i].length <= 26`，`arr[i]` 只含小写字母。

```python
def max_length(arr: list[str]) -> int:
    masks = {0}                                  # 所有"字母互不重复"的拼接能得到的字母集合
    best = 0
    for s in arr:
        if len(set(s)) < len(s):                 # 自己内部就有重复字母：永远不能选
            continue
        cur = 0
        for ch in s:
            cur |= 1 << (ord(ch) - 97)
        for m in list(masks):                    # 对旧集合拍快照，别边遍历边加
            if m & cur == 0:                     # 和 s 没有公共字母：可以拼上
                masks.add(m | cur)
                best = max(best, (m | cur).bit_count())
    return best
```

**例题：** LC 260 只出现一次的数字 III

整数数组 `nums` 里恰好有**两个**元素只出现一次，其余所有元素都恰好出现两次。找出这两个元素，顺序任意。要求线性时间、常数额外空间。`2 <= nums.length <= 3 * 10^4`，`-2^31 <= nums[i] <= 2^31 - 1`。

```python
def single_number_iii(nums: list[int]) -> list[int]:
    both = 0
    for x in nums:
        both ^= x                                    # both == a ^ b，且 a != b 所以 both != 0
    low = both & -both                               # 最低位的 1：a、b 在这一位不同
    a = 0
    for x in nums:
        if x & low:                                  # 只异或这一位为 1 的那一组
            a ^= x
    return [a, both ^ a]                             # 另一个由 a ^ b ^ a 得到，不用再扫一遍
```

**例题：** LC 442 数组中重复的数据

给长度为 `n` 的整数数组 `nums`，其中每个整数都在 `[1, n]` 内，且每个整数出现**一次或两次**。找出所有出现两次的整数，以数组形式返回。必须设计 `O(n)` 时间、**仅用常量额外空间**（不含输出）的算法。`n == nums.length`，`1 <= n <= 10^5`，`1 <= nums[i] <= n`。

```python
def find_duplicates(nums: list[int]) -> list[int]:
    res: list[int] = []
    for x in nums:
        i = abs(x) - 1                         # 值 x 对应的「标记位置」；x 可能已被前面的标记取负
        if nums[i] < 0:
            res.append(abs(x))                 # 这个位置已经被标记过：x 是第二次出现
        else:
            nums[i] = -nums[i]                 # 第一次出现：把 nums[i] 取负做记号
    return res
```

**例题：** LC 54 螺旋矩阵

给一个 `m` 行 `n` 列的矩阵 `matrix`，按**顺时针螺旋顺序**返回矩阵中的所有元素。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 10`，`-100 <= matrix[i][j] <= 100`。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    result: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        result.extend(matrix[top][left : right + 1])                       # 上边：左 -> 右
        result.extend(row[right] for row in matrix[top + 1 : bottom + 1])  # 右边：上 -> 下
        if top < bottom and left < right:          # 还剩至少两行两列，下边和左边才不会重复走
            result.extend(reversed(matrix[bottom][left:right]))            # 下边：右 -> 左
            result.extend(matrix[r][left] for r in range(bottom - 1, top, -1))  # 左边：下 -> 上
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return result
```

**例题：** LC 1860 增长的内存泄露

给两个整数 `memory1` 和 `memory2`，分别表示两个内存条剩余可用内存的位数。一个程序每秒消耗递增的内存：在第 `i` 秒（从 `1` 开始），有 `i` 位内存被分配给**剩余内存较多**的那个内存条（两者一样多时分给第一个）。如果两个内存条剩余内存都不足 `i` 位，程序意外退出。返回数组 `[crashTime, memory1crash, memory2crash]`，其中 `crashTime` 是程序退出的时刻（秒），后两项是两个内存条最后剩余的位数。`0 <= memory1, memory2 <= 2^31 - 1`。

```python
def mem_leak(memory1: int, memory2: int) -> list[int]:
    second = 1                                 # 当前要分配的位数，也是秒数
    while max(memory1, memory2) >= second:     # 至少有一条放得下，程序才没崩
        if memory1 >= memory2:                 # 相等时给第一条，所以用 >=
            memory1 -= second
        else:
            memory2 -= second
        second += 1
    return [second, memory1, memory2]
```

**例题：** LC 415 字符串相加

给两个字符串形式的非负整数 `num1` 和 `num2`，计算它们的和，同样以字符串形式返回。不能使用任何内建的处理大整数的库（比如 `BigInteger`），也不能直接把输入的字符串转换为整数。`1 <= num1.length, num2.length <= 10^4`，`num1` 和 `num2` 都只包含数字 `0-9`，且都不含前导零。

```python
from itertools import zip_longest


def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    # 从个位开始配对；短的那个用 "0" 补齐
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)    # 一步同时得到进位和当前位
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```

**例题：** LC 1041 困于环中的机器人

机器人从 `(0, 0)` 面朝北出发，按指令串 `instructions`（只含 `G` 直走、`L` 左转、`R` 右转）**无限循环**执行；判断平面上是否存在一个圆，使机器人永远不离开。`1 <= instructions.length <= 100`。

```python
def is_robot_bounded(instructions: str) -> bool:
    x = y = 0
    dx, dy = 0, 1                      # 方向向量，初始朝北
    for ch in instructions:
        if ch == "G":
            x, y = x + dx, y + dy
        elif ch == "L":
            dx, dy = -dy, dx           # 逆时针转 90 度
        else:
            dx, dy = dy, -dx           # 顺时针转 90 度
    # 只模拟一轮：回到原点，或者不再朝北（转 4 轮后必回原点）
    return (x, y) == (0, 0) or (dx, dy) != (0, 1)
```

**例题：** LC 122 买卖股票的最佳时机 II

整数数组 `prices[i]` 是第 `i` 天的股价，每天可以买入和 / 或卖出，任何时候最多持有一股，返回能获得的最大利润。`1 <= prices.length <= 3 * 10^4`，`0 <= prices[i] <= 10^4`。

```python
def max_profit(prices: list[int]) -> int:
    # 每一段上涨都能吃到：把所有 “后一天比前一天高” 的差额加起来
    return sum(max(today - yesterday, 0) for yesterday, today in pairwise(prices))
```

**例题：** LC 365 水壶问题

有两个容量分别为 `x` 升和 `y` 升的水壶，水源无限。判断能否用这两个壶**恰好**得到 `target` 升水（两个壶里的水加起来是 `target` 即可）。允许的操作：装满任一水壶；清空任一水壶；把一个壶的水倒进另一个，直到接水的壶满或倒水的壶空。`1 <= x, y, target <= 10^3`。

```python
from math import gcd
def can_measure_water(x: int, y: int, target: int) -> bool:
    return target <= x + y and target % gcd(x, y) == 0
```

**例题：** LC 134 加油站

环形路线上有 `n` 个加油站，第 `i` 个加油站有汽油 `gas[i]` 升。你的油箱容量无限，从第 `i` 个加油站开往第 `i + 1` 个加油站要消耗 `cost[i]` 升汽油（最后一个站开往第 `0` 站）。你从其中一个加油站出发，开始时油箱为空。如果能按顺序绕环路行驶一周，返回出发的加油站编号，否则返回 `-1`；如果存在解，保证它**唯一**。`n == gas.length == cost.length`，`1 <= n <= 10^5`，`0 <= gas[i], cost[i] <= 10^4`。

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c
        total += diff
        tank += diff
        if tank < 0:
            start, tank = i + 1, 0
    return start if total >= 0 else -1
```
