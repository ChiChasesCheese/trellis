---
id: tlc-last-stone-weight-ii-4-followup
node: b.last-stone-weight-ii
type: qa
step: 4
---
## Q
**LC 1049 最后一块石头的重量 II**｜追问

面试官接着问：（1）能不能不写内层循环、用更快的方式表示「可达和」？（2）要输出具体怎么分堆？（3）石头数量到 `100`、重量到 `10^4` 怎么办？

## A
1. **位集（bitset）**：用一个 Python 整数的二进制位表示可达集合，第 `s` 位为 `1` 表示和 `s` 可达。每块石头 `w` 把整个集合平移 `w` 位再并入：

```python
def last_stone_weight_ii_bitset(stones: list[int]) -> int:
    total = sum(stones)
    bits = 1                               # 第 0 位为 1：空集的和为 0
    for w in stones:
        bits |= bits << w                  # 选 w 或不选：整体左移 w 位再合并
    best = max(s for s in range(total // 2 + 1) if bits >> s & 1)
    return total - 2 * best
```
   运行：`[2,7,4,1,8,1]` → `1`，`[31,26,33,21,40]` → `5`。位运算在 C 层按机器字并行处理，整个内层循环变成一次移位或操作。
2. **输出分堆**：保留二维布尔表 `dp[i][s]`（前 `i` 块石头能否凑出 `s`），从 `dp[n][best]` 往回走：若 `dp[i-1][s]` 为真，第 `i` 块不选；否则选，`s -= w`。
3. **规模变大**：背包是伪多项式，容量 `n · max_w / 2` 太大时，可以用折半枚举（meet in the middle）：把石头分成两半，各自枚举所有符号和，排序后用双指针找最接近的组合，`O(2^(n/2) · n)`，适合 `n` 在 `40` 以内、重量很大的情形。

**Python 提醒**：Python 整数没有位宽限制，`bits << w` 可以任意大，位集写法天然可行；`bits >> s & 1` 的优先级是先移位再按位与，必要时加括号写成 `(bits >> s) & 1` 更清楚。
