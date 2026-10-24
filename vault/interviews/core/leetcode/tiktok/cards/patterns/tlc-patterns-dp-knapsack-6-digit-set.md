---
id: tlc-patterns-dp-knapsack-6-digit-set
node: patterns.dp-knapsack
type: qa
step: 6
---
## Q
**动态规划：背包与计数｜数位计数：最大为 N 的数字组合（LC 902）**

用给定的数字集合能写出多少个不超过 `n` 的正整数？为什么不能枚举到 `n`，而要按位计数？

## A
`n` 最大 `10^9`，不能逐个检查。把数分成两类：

1. **位数比 `n` 少**：每一位都可以任选，`d` 个数字时，长度 `i` 的有 `d^i` 个，全部合法。
2. **位数和 `n` 相同**：从最高位起**贴着 `n` 的前缀**走：这一位选比 `n` 的当前位小的数字，后面各位任选；或者选等于当前位的数字，继续看下一位。

```python
def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    s = str(n)
    L, d = len(s), len(digits)
    total = sum(d ** i for i in range(1, L))      # 位数比 n 少的：任意组合都合法
    for i, ch in enumerate(s):
        smaller = sum(1 for x in digits if x < ch)
        total += smaller * d ** (L - i - 1)       # 这一位比 n 小，后面的位任选
        if ch not in digits:
            return total                          # 贴不住了：后面都不可能再等于 n 的前缀
    return total + 1                              # 每一位都贴住了：n 本身也能写出来
print(at_most_n_given_digit_set(["1", "3", "5", "7"], 100), at_most_n_given_digit_set(["1", "4", "9"], 10**9), at_most_n_given_digit_set(["7"], 8))   # 20 29523 1
```

- 时间 `O(L · d)`，`L` 是位数（最多 10）。
- 例：数字 `1,3,5,7`、`n = 100`：一位数 `4` 个，两位数 `16` 个，共 `20`；三位数最小是 `111 > 100`，循环到第二位 `'0'` 时不在集合里，立即返回 `20`。
- `x < ch` 是字符比较，对 `'0'..'9'` 与数值比较一致。
- 这类"逐位贴着上界走"的思路叫**数位 DP**（Digit DP）：状态是"当前位、是否仍贴着上界"，更复杂的条件（含某数字、数位和）也用同样的框架，常配记忆化。
