---
id: tlc-closest-prime-numbers-in-range-0-whole
node: b.closest-prime-numbers-in-range
type: qa
---
## Q
**LC 2523 范围内最接近的两个质数**｜Medium · LC TikTok 全时段热度 62/100

给两个正整数 `left`、`right`，在 `[left, right]` 内找两个质数 `num1 < num2`，使 `num2 - num1` 最小；差相同时取 `num1` 最小的一对；区间内凑不出两个质数就返回 `[-1, -1]`。`1 <= left <= right <= 10^6`。例：`left = 10, right = 19` → `[11, 13]`（`[17, 19]` 差也是 2，但 `11 < 17`）；`left = 4, right = 6` → `[-1, -1]`（只有一个质数 5）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用埃氏筛（Sieve of Eratosthenes）一次筛出 `[2, right]` 内所有质数，最优的一对一定是**相邻**质数，按从小到大扫一遍取差最小者，并列时取先出现的。`O(R log log R)`，`R = right`。

**识别。** 「范围内的质数」加上界 `10^6`，是筛法的信号：逐个试除判质是 `O(R√R)`，约 `10^9`，超时；筛法把「判质」摊成对倍数的批量划除。「差最小的一对」是排序后只看相邻的信号：`p < q < r` 三个质数里，`(p, r)` 的差一定比 `(p, q)` 大，夹着第三个数的一对不可能最优。

**推导。** 暴力：对区间每个数试除到 `√x`，`O(R√R)`。浪费：每个数都在重复找同样的小因子。洞察：从 `2` 开始，每遇到一个还没被划掉的数 `p`（它必是质数），把 `p², p²+p, …` 全部划掉，每个合数只会被它的最小质因子划一次，总共 `O(R log log R)`。筛完质数天然有序，答案只可能在相邻对里；`min` 在并列时返回先遇到的那一对，而先遇到的 `num1` 更小，恰好满足并列规则。

```python
from itertools import pairwise
from math import isqrt


def closest_primes(left: int, right: int) -> list[int]:
    sieve = bytearray([1]) * (right + 1)       # sieve[i] == 1 表示 i 目前被认为是质数
    sieve[:2] = b"\x00\x00"                    # 0 和 1 不是质数
    for p in range(2, isqrt(right) + 1):
        if sieve[p]:
            # 从 p*p 起，p 的倍数全部划掉；切片赋值在 C 层完成，比 Python 循环快一个量级
            sieve[p * p :: p] = bytes(len(range(p * p, right + 1, p)))
    primes = [p for p in range(left, right + 1) if sieve[p]]
    if len(primes) < 2:
        return [-1, -1]
    # min 遇到并列的最小差时返回第一个，也就是 num1 最小的那一对
    a, b = min(pairwise(primes), key=lambda pair: pair[1] - pair[0])
    return [a, b]
```

**运行。** `closest_primes(10, 19)` → `[11, 13]`；`(4, 6)` → `[-1, -1]`；`(1, 1)` → `[-1, -1]`；`(1, 3)` → `[2, 3]`；`(1, 10**6)` → `[2, 3]`；`(999995, 10**6)` → `[-1, -1]`。

**复杂度。** 时间 `O(R log log R)`；空间 `O(R)`，`bytearray` 每个数 1 字节，`R = 10^6` 时约 1 MB。

**易错点。**
- 忘了清掉 `0` 和 `1`：`left = 1, right = 3` 会把 `1` 当质数，返回 `[1, 2]`，正确答案是 `[2, 3]`。
- 划倍数要从 `p * p` 起、外层只跑到 `isqrt(right)`；从 `2p` 起结果也对，但多做大量重复划除。
- 区间里质数不足两个时返回 `[-1, -1]`，不是空列表。

**追问。**
- `right` 到 `10^12` 但 `right - left` 不大：分段筛，只开 `right - left + 1` 的数组，用不超过 `√right` 的数当筛子。
- 同一上界下查询很多次：预处理一次质数表，用 `bisect` 切出 `[left, right]` 的那一段，只扫相邻对。
- 提前返回：`(2, 3)` 的差是 1，其余质数对的差至少是 2；扫描时一旦得到差 `<= 2` 的一对，后面不可能更好，直接返回。

**同模式。** LC 204 计数质数、LC 762 二进制表示中质数个数的数字、LC 866 回文质数、LC 1175 质数排列。
