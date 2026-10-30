---
id: tlc-last-stone-weight-ii-4-followup
node: a.last-stone-weight-ii
type: qa
step: 4
---
## Q
**LC 1049 最后一块石头的重量 II**｜追问

面试官接着问：（1）能不能用更快的方式表示「可达和」？（2）空间能不能更小？（3）要输出具体怎么分堆？（4）石头数量到 `100`、重量到 `10^4` 怎么办？

## A
1. **位集（bitset）**：把一整行布尔值存成一个 Python 整数的二进制位，第 `s` 位为 `1` 表示和 `s` 可达；每块石头 `w` 相当于整体左移 `w` 位再并入原值，一次大整数运算替代内层循环，位运算在 C 层按机器字并行。
2. **省空间**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
3. **输出分堆**：主解法的整张表已经在手，从 `dp[n][best]` 往回走：

```python
def last_stone_split(stones: list[int]) -> tuple[int, list[int]]:
    n = len(stones)
    total = sum(stones)
    half = total // 2
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        w = stones[i - 1]
        for s in range(half + 1):
            dp[i][s] = dp[i - 1][s] or (s >= w and dp[i - 1][s - w])
    best = max(s for s in range(half + 1) if dp[n][s])
    chosen, s = [], best
    for i in range(n, 0, -1):                      # 从 dp[n][best] 往回走
        if not dp[i - 1][s]:                       # 不选第 i 块就到不了 s，说明它被选了
            chosen.append(stones[i - 1])
            s -= stones[i - 1]
    return total - 2 * best, chosen
```

   `[2,7,4,1,8,1]` → `(1, [4, 7])`，`[31,26,33,21,40]` → `(5, [40, 33])`。选出的一堆与剩下的一堆重量差就是答案。
4. **规模变大**：背包是伪多项式，容量 `n · max_w / 2` 太大时，可以用折半枚举（meet in the middle）：把石头分成两半，各自枚举所有符号和，排序后用双指针找最接近的组合，`O(2^(n/2) · n)`，适合 `n` 在 `40` 以内、重量很大的情形。

**Python 提醒**：Python 整数没有位宽限制，位集写法里的左移可以任意大，天然可行；`bits >> s & 1` 的优先级是先移位再按位与，必要时加括号写成 `(bits >> s) & 1` 更清楚。
