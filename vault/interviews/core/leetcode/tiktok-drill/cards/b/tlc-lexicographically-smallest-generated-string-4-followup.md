---
id: tlc-lexicographically-smallest-generated-string-4-followup
node: b.lexicographically-smallest-generated-string
type: qa
step: 4
---
## Q
**LC 3474 字典序最小的生成字符串**｜追问

面试官接着问：（1）`m` 涨到 `10^5`，`O(n·m)` 太慢怎么办？（2）如何自己快速验证答案是对的？（3）这个题到底有哪几种无解的情形？

## A
1. **大 `m`。** 瓶颈是「窗口是否等于 `str2`」的比较，可以换成 Z 函数或滚动哈希（rolling hash）做 `O(1)` 判断；改动一位后，只需更新覆盖该位的那些窗口的哈希值。
2. **验证。** 在 `n + m - 1 <= 8` 的小数据上，按字典序枚举所有字符串，第一个满足全部窗口条件的就是答案；用来对照贪心的结果。
3. **无解的情形。** 只有两种：两个 `'T'` 窗口在重叠处要求不同的字母；或者某个 `'F'` 窗口里的位置全部被 `'T'` 钉死，而它们拼出来恰好等于 `str2`（如 `("TFT", "aa")`）。

**Python 提醒**：`for … else` 的 `else` 在循环**没有** `break` 时执行；这里 `else: return ""` 表示「窗口内没找到自由位」。另外 `res[i : i + m] == list(str2)` 比较的是两个列表；若 `res` 是列表而 `str2` 是字符串，直接 `==` 永远是 `False`，必须把 `str2` 转成列表，或把 `res` 的切片 `"".join` 后再比较。
