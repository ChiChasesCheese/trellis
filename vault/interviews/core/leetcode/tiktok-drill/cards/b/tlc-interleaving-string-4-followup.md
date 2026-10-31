---
id: tlc-interleaving-string-4-followup
node: b.interleaving-string
type: qa
step: 4
---
## Q
**LC 97 交错字符串**｜追问

面试官接着问：（1）自顶向下的记忆化写法？（2）要输出一种具体的交错方案？（3）题目的进阶：只用 `O(len(s2))` 额外空间？（4）字符串很长（比如各 `10^4`）时 `O(mn)` 太慢，有什么办法？

## A
1. **记忆化搜索**：`go(i, j)` 表示 `s1[i:]` 与 `s2[j:]` 能否交错成 `s3[i + j:]`，用 `functools.cache` 缓存：

```python
from functools import cache


def is_interleave_memo(s1: str, s2: str, s3: str) -> bool:
    if len(s1) + len(s2) != len(s3):
        return False

    @cache
    def go(i: int, j: int) -> bool:        # s1[i:] 与 s2[j:] 能否交错成 s3[i + j:]
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        return (i < len(s1) and s1[i] == s3[k] and go(i + 1, j)) or (
            j < len(s2) and s2[j] == s3[k] and go(i, j + 1))

    return go(0, 0)
```
   递归深度最多 `m + n <= 200`，不会触到 Python 的深度上限；状态数同样是 `O(mn)`。
2. **输出方案**：完整的二维布尔表就是回溯的依据，从 `(m, n)` 回溯：若 `i > 0` 且 `dp[i-1][j]` 且 `s1[i-1] == s3[i+j-1]`，这个字符来自 `s1`，退到 `(i-1, j)`；否则来自 `s2`，退到 `(i, j-1)`。
3. **进阶：只用 `O(len(s2))` 额外空间**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
4. **规模很大**：`O(mn)` 是标准做法的复杂度。可以先用廉价的必要条件提前返回：长度之和不等、`Counter(s1) + Counter(s2) != Counter(s3)`（字符多重集不同）就直接 `False`；通过这两个检查后再跑 DP，最坏复杂度不变。

**Python 提醒**：`@cache` 把参数当哈希键，`(i, j)` 这样的小整数键没问题；在函数外保存的 `cache` 会跨测试用例保留，若 `go` 定义在函数内（如上）则每次调用都是新缓存，不会串数据。
